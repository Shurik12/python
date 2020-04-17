import click
import pandas as pd

from semantic_parser import SemanticParser
from semantic_parser.train_utils import load_dataset
from semantic_parser.prediction_tools import report_results

from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
import json
from start import start_parser
from Parser_Mongo import connect_mongodb, Parser_Mongo
from PostgreSQL_class import PostgreSQLconnection, Parser_Postgre

import psycopg2 as ps
from psycopg2.extras import DictCursor

def create_parser(config_file):
    return SemanticParser(config_filename=config_file)
    
@click.group()

def cli():
    pass


@click.command()
@click.option('--dataset', default='train.pkl')
@click.option('--data-type', default='pickle')
@click.option('--config', default='config.json')
def train(dataset, data_type, config):
    print('Training models...')
    parser = create_parser(config)
    print('Training complete.')


@click.command()
@click.option('--in-file', default='data.txt')
@click.option('--config', default='config.json')
@click.option('--out-file', default='result.tsv')
def predict(in_file, config, out_file):
    print('Starting prediction...')
    parser = create_parser(config)
    with open(in_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    print (lines)
    lin  = [u'dsafe']
    print (lin)
    result = parser.predict(lines, to_pandas=True)
    result.to_csv(out_file, encoding='utf-8', sep='\t')
    print('Prediction completed!')
    
# Команда по запуску парсера на Mongodb, 
# вводим название коллекции, которую хотим обрабатывать; в будущем и параметры соединения
@click.command()
@click.option('--collection', default = 'building')
def predictmongodb(collection):
    
    # устанавливаем соединение с базой
    
    # Объявление переменных
    MONGO_PORT = 55556
    MONGO_DB = "fincase"
    MONGO_USER = "shesterin"
    MONGO_PASS = "sK349Acm9qwD92s"
    SERVER_HOST = '192.168.0.78'
    SERVER_PORT = 22
    
    db = connect_mongodb(MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASS, SERVER_HOST, SERVER_PORT)      
    
    print ('Starting prediction...')
    Parser_Mongo(db, collection)
    print('Prediction completed!')
    
# Команда по запуску парсера на PostgreSQL, 
# вводим название таблицы, которую хотим обрабатывать; в будущем и параметры соединения
@click.command()
@click.option('--table', default = 'building')
def predictpostgresql(table):
    
    # устанавливаем соединение с базой
    
    # Объявление переменных
    dbname = 'sas_test_db' 
    user = 'sas' 
    password = 'sasTESTpassword'
    host = '185.98.83.27'
    port = '29001' 
    
    # Создаем объект класса
    #connection = PostgreSQLconnection(dbname, user, password, host, port)
    connection = ps.connect(
                            dbname = dbname, 
                            user = user, 
                            password = password, 
                            host = host, 
                            port = port
                           )
    cursor = connection.cursor(cursor_factory = DictCursor)
    print ('Starting prediction...')
    print (Parser_Postgre(connection, cursor, table))
    print('Prediction completed!')
    connection.commit()
    cursor.close()
    connection.close()

@click.command()
@click.option('--dataset', default='test.pkl')
@click.option('--data-type', default='pickle')
@click.option('--config', default='config.json')
@click.option('--metrics-file', default='metrics.json')
def evaluate(dataset, data_type, config, metrics_file):
    print('Classification metrics:')
    parser = create_parser(config)
    data = load_dataset(dataset, data_type)
    x = data[parser.config['text_name']].fillna('')
    predictions = parser.predict(x)
    predictions.index = data.index
    ground_truth = data[predictions.columns]
    report_results(ground_truth, predictions)
    # todo: use metric_file to store the results


cli.add_command(train)
cli.add_command(predict)
cli.add_command(predictmongodb)
cli.add_command(predictpostgresql)
cli.add_command(evaluate)

if __name__ == '__main__':
    cli()
