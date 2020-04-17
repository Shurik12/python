import click
import pandas as pd

from semantic_parser import SemanticParser
from semantic_parser.train_utils import load_dataset
from semantic_parser.prediction_tools import report_results

def create_parser(config_file):
    return SemanticParser(config_filename=config_file)


def start_parser(data):
    config = 'config.json'
    #print('Starting prediction...')
    parser = create_parser(config)
    data = [data]
    #with open(in_file, 'r', encoding='utf-8') as f:
    #    lines = f.readlines()
    result = parser.predict(data, to_pandas=True)
    #result.to_csv(out_file, encoding='utf-8', sep='\t')
    #print(result["houselinetype"])
    #print('Prediction completed!')
    return result