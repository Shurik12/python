import psycopg2 as ps
from psycopg2.extras import DictCursor

def get_connection(dbname, user, password, host, port):
    connection = ps.connect(dbname = dbname, user = user, password = password, host = host, port = port)
    cursor = connection.cursor(cursor_factory = DictCursor)
    print("Connection established with", cursor)
    return connection, cursor

# получить название бд
def get_db_name(cursor):
    cursor.execute("SELECT version();")
    return cursor.fetchone()

# получить размер бд
def get_db_size(cursor):
    cursor.execute("SELECT pg_database_size('sas_db')")
    return cursor.fetchone()[0]

# получить имена всех таблиц
def get_table_names(cursor):
    cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN            
      ('information_schema','pg_catalog')
    """)   
    return cursor.fetchall()
def cursor_close(conn, cursor):
    cursor.close()
    conn.close()

def conn_commit(conn):
    conn.commit()
    
def get_column_names(table, cursor):
    cursor.execute("SELECT * FROM %s LIMIT {size}".format(size=0) % table)
    return [desc[0] for desc in cursor.description]