
import copy
import os
import pickle
import pandas as pd
import warnings


from .train_utils import load_config, load_dataset, MODELS_REGISTER
from .prediction_tools import confident_predict
from .regex_classifier import DummyTransformer
from .floors import train_higher_floors_model


class SemanticParser:
    UNKNOWN = 'unknown'
    
    def __init__(self, config_filename):
        self.config = load_config(config_filename)
        self.models = None
        self.extractor = None
        self.postprocessors = None
        self.config_filename = config_filename
        self.load_models()

    @property
    def models_dir(self):
        return os.path.join(os.path.dirname(self.config_filename), self.config['models_filename'])
        
    def load_models(self):
        try:
            with open(self.models_dir, 'rb') as f:
                models_and_extractor = pickle.load(f)
            self.models = models_and_extractor['models']
            self.extractor = models_and_extractor['extractor']
            self.postprocessors = models_and_extractor['postprocessors']
        except Exception:
            warnings.warn('The models could not be loaded from {}.'.format(self.config['models_filename']))
        
    def train(self, dataset, data_type=None, dump_models=True):
        if isinstance(dataset, str):
            data = load_dataset(dataset, data_type)
        else:
            data = dataset
        self.extractor, self.models = self.train_models(data)
        self.postprocessors = [
            train_higher_floors_model(data)
        ]
        if dump_models:
            with open(self.models_dir, 'wb') as f:
                pickle.dump({
                    'models': self.models,
                    'extractor': self.extractor,
                    'postprocessors': self.postprocessors
                }, f)
        
    def train_models(self, dataset, models_config=None, y_preprocessor=None, x_preprocessor=None):
        x_name, y_names = self.config['text_name'], self.config['target_names']
        default_model = MODELS_REGISTER[self.config['model_type']]
        if 'extractor_type' in self.config:
            extractor = MODELS_REGISTER[self.config['extractor_type']]()
            
            #print (extractor)
            
        else:
            extractor = DummyTransformer()
        if models_config is None:
            models_config = dict()
        models = dict()
        x = dataset[x_name].fillna('')
        if x_preprocessor is not None:
            x = x_preprocessor(x)
        extractor.fit(x)
        fnames = extractor.get_feature_names()
        x = extractor.transform(x)
        
        # вношу поправки AS01
        import numpy as np
        def save_sparse_csr(filename, array):
            np.savez(filename, data=array.data, indices=array.indices, indptr=array.indptr, shape=array.shape)
        save_sparse_csr("train_matrix", x)
        
       # print (x)
        for y_name in y_names:
            y = dataset[y_name]
            if y_preprocessor is not None:
                y = y_preprocessor(y, target_name=y_name)
            model_maker = models_config.get(y_name, default_model)
            model = model_maker(x, y, y_name, fnames=fnames)
            model.fit(x, y)
            models[y_name] = model
        return extractor, models
           
    def predict(self, texts, to_pandas=True, postprocess=True):
        default_threshold = self.config.get('confidence_threshold', 0.5)
        custom_thresholds = self.config.get('custom_thresholds', {})
        features = self.extractor.transform(texts)
        predictions = {
            y_name: confident_predict(
                self.models[y_name],
                features,
                threshold=custom_thresholds.get(y_name, default_threshold))
            for y_name in self.models
        }
        predictions = [dict(zip(predictions.keys(), c)) for c in zip(*predictions.values())]
        if len(self.postprocessors) > 0 and postprocess:
            for pp in self.postprocessors:
                predictions = [pp.postprocess(text, prediction) for text, prediction in zip(texts, predictions)]
        if to_pandas:
            predictions = pd.DataFrame.from_dict(predictions)
        return predictions
                
    def parse(self, text, keep_unknown=False):
        islist = isinstance(text, list)
        if not islist:
            text = [text]
        parsed = [
            {k: v for k, v in item.items() if v != self.UNKNOWN or keep_unknown}
            for item in self.predict(text, to_pandas=False)
        ]
        if not islist:
            parsed = parsed[0]
        return parsed
        
    def update_properties(self, text, old_properties, rewrite=False, insert_unknowns=False):
        new_properties = copy.copy(old_properties)
        for k, v in self.parse(text).items():
            if (k not in old_properties or rewrite) and (insert_unknowns or v != self.UNKNOWN):
                new_properties[k] = v
        return new_properties
