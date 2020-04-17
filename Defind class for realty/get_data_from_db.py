import psycopg2 as ps
from psycopg2.extras import DictCursor
import numpy as np

def get_connection(dbname, user, password, host, port):
    connection = ps.connect(dbname = dbname, user = user, password = password, host = host, port = port)
    cursor = connection.cursor(cursor_factory = DictCursor)
    print("Connection established with", cursor)
    return connection, cursor

def load_offices(cursor, table):
    #streets = np.array([])
    SQL = """SELECT id, price, fulladdress, buildingclass, buildyear, floorscount
             FROM %s 
             WHERE fulladdress Like '%s'
          """
    cursor.execute(SQL % (table, '%Москва%'))
    with open("offices.tsv", "w") as f_w:
        f_w.write('id\tprice\taddress\tclass\tyear\tfloors\n')
        for line in cursor.fetchall(): 
            line_w = ''
            for word in line:
                line_w += str(word) + '\t'
            line_w = line_w.strip() + '\n'
            f_w.write(line_w)
        print ("Data loaded into file %s success" % ("offices.tsv"))
        