
import numpy as np
import pandas as pd
import re

from nltk import wordpunct_tokenize
from sklearn.linear_model import LogisticRegression


floors_map = {
    "first": 1,
    "second": 2,
    "basement": -1,
    "ground": 0,
}

w2d = {
    1: 'перв..',
    2: 'втор..',
    3: 'трет(ий|ь..?)',
}


fexp = {
    'right': [
        '(\- )?(([ое]?м|ы?й) )?(мансардн(ом|ый) )?эт(аже?)? ',
        '\/ \d+',
        '\/ \d+ этаж',
        'этажн',
    ],
    'left': [
        '.*\d+ \/$'
    ]
}


wsize = {
    'right': 4,
    'left': 2
}


cnames = ['num', 'num_g_100', 'num_l_3', 'pos']
for context_name, context_expressions in fexp.items():
    for i, expression in enumerate(context_expressions):
        cnames.append('{}__{}'.format(context_name, i))


def normalize_floor(w):
    if isinstance(w, int):
        return w
    elif isinstance(w, float):
        return int(w)
    if w.isdigit():
        return int(w)
    for k, v in w2d.items():
        if re.match(v, w, flags=re.IGNORECASE):
            return k


class SingleFloorModel:
    def __init__(self):
        self.model = None

    def train(self, data, cross_validate=False):
        assert 'description' in data.columns
        assert 'floorscount' in data.columns
        idx, df = self.extract_hypotheses(data)
        # our features are so tough that we are not afraid of overfitting
        lr = LogisticRegression(C=1000, solver='liblinear')
        if cross_validate:
            self.cross_validate(idx, df, lr)
        lr.fit( df.drop('outp', axis=1), df.outp)
        self.model = lr

    def extract_hypotheses(self, data):
        inp = []
        outp = []
        idx = []
        ctx = []

        for ir, r in data.iterrows():
            text = re.sub('(\d)([а-яА-Я])', '\g<1> \g<2>', r['description'])  # insert whitespace between digits and letters
            target = normalize_floor(r.floorscount)
            wpt = wordpunct_tokenize(text)

            for i, w in enumerate(wpt):
                num = normalize_floor(w)
                if num is not None:
                    features = [min(num, 100), int(num > 100), int(num < 3), i]
                    for context_name, context_expressions in fexp.items():
                        if context_name == 'right':
                            context = wpt[(i + 1):(i + wsize[context_name] + 1)]
                        elif context_name == 'left':
                            context = wpt[(i - wsize[context_name]):i]
                        else:
                            context = wpt[(i - wsize[context_name]):(i + wsize[context_name] + 1)]
                        context_text = ' '.join(context)
                        for expression in context_expressions:
                            features.append(int(bool(re.match(expression, context_text, flags=re.IGNORECASE))))
                    inp.append(features)
                    outp.append(int(num == target))
                    idx.append(ir)
                    ctx.append(' '.join(wpt[(i - 3):(i + 4)]))
        df = pd.DataFrame(inp, index=ctx, columns=cnames)
        df['outp'] = outp
        idx = np.array(idx)
        return idx, df

    def cross_validate(self, idx, df, lr):
        unique = np.unique(idx)
        errors = 0
        idx = np.array(idx)
        for i, ix in enumerate(unique):
            df1 = df[idx == ix].copy()
            df2 = df[idx != ix]
            lr.fit(df2.drop('outp', axis=1), df2.outp)
            df1['pred'] = lr.predict_proba(df1.drop('outp', axis=1))[:, 1]
            if not (df1.outp[df1['pred'] == df1['pred'].max()] == 1).all():
                print('error at index {}'.format(ix))
                errors += 1
        print('{} errors out of {} = {}'.format(errors, len(unique), errors / len(unique)))

    def apply(self, text):
        d = pd.DataFrame({'description': [text], 'floorscount': ['0']})
        iii, ddd = self.extract_hypotheses(d)
        ddd['pred'] = self.model.predict_proba(ddd.drop('outp', axis=1))[:, 1]
        return ddd.num[ddd.pred.idxmax()]

    def postprocess(self, text, prediction):
        floor = prediction['floornumber']
        if floor == 'higher':
            floor = self.apply(text)
        else:
            floor = floors_map.get(floor, floor)
        prediction['floornumber'] = floor
        return prediction


def train_higher_floors_model(data):
    data = data[data['floornumber'] == 'higher']
    model = SingleFloorModel()
    model.train(data)
    return model
