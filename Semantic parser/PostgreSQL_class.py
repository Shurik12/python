# Import libreries:

import psycopg2 as ps
from psycopg2.extras import DictCursor
from start import start_parser # исполняемый файл с парсером
import codecs

# Establish a connection with PostgreSQL
class PostgreSQLconnection(object):
    # конструктор класса
    def __init__(self, dbname, user, password, host, port):
        connection = ps.connect(
                                dbname = dbname, 
                                user = user, 
                                password = password, 
                                host = host, 
                                port = port
                               )
        self.cursor = connection.cursor(cursor_factory = DictCursor)
        
    def get_columns_names(self, name_table):
        self.cursor.execute("SELECT * FROM %s LIMIT {size}".format(size=0) % name_table)
        return [desc[0] for desc in self.cursor.description]
    
    # получить название бд
    def get_db_name(self):
        self.cursor.execute("SELECT version();")
        return self.cursor.fetchone()
    
    # получить размер бд
    def get_db_size(self):
        self.cursor.execute("SELECT pg_database_size('sas_db')")
        return self.cursor.fetchone()[0]
    
    # получить имена всех таблицам
    def get_tables_names(self):
        self.cursor.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN            
          ('information_schema','pg_catalog')
        """)   
        return self.cursor.fetchall()
    def cursor_close(self):
        self.cursor.close()
        self.close()
        
    def conn_commit(self):
        self.commit()
    
def Parser_Postgre(conn, cursor, table):
    i=0
    columns  = ["entrance",                                      
                "entrance_type",
                "hasshopwindows",                                
                "houselinetype",                                 
                "conditiontype",                                 
                "isbuildingliving",                              
                "communal_included",
                "vattype",                                       
                "floornumber"                                    
               ]
    """tables = ["buildings" ,"buildings_lease", "businesses", "placements5", "businesses_lease", "garages", "garages_lease",
              "industrials", "industrials_lease", "livings", "offices", "offices_lease", "livings_mo", 
              "commercial_requests_histrory", "placements_clean", "placements_depr", "placements_depr_lease", 
              "shoppings_lease", "zkh", "shoppings", "warehouses_lease", "warehouses", "residential_real_estate_history", 
              "alembic_version"
             ]"""
    tables = [
              'businesses', 'businesses_lease', 'floor_objects', 'garages', 'garages_lease', 
              'buildings_offices_shoppings_free_lease', 'warehouses', 'warehouses_lease', 
              'buildings_industrials_warehouses_lease', 'placements_depr', 'placements_depr_lease', 'buildings', 
              'buildings_lease', 'analogs', 'placements_lease', 'commercial_requests_histrory', 'property', 
              'shoppings_lease', 'shoppings', 'sas_commercial_requests', 'placements', 
              'industrials_warehouses', 'сommercial_requests', 'industrials_warehouses_lease', 
              'offices_lease', 'offices', 'industrials', 'garages_lease1', 
              'buildings_industrials_warehouses', 'lands', 'industrials_lease',
              'commercial_property', 'buildings_offices_shoppings_free', 'relevant_property'
             ]
    #array = [[0] * 9 for i in range(24)]
    array = [0] * 7
    try:
        print (table + ": start!")                
            
        # Обработка таблиц "businesses", "businesses_lease", "garages_lease1"
        if table in ["businesses", "businesses_lease", "garages_lease1"]:
            SQL = """SELECT id, description, floornumber, vattype, semantic
                     FROM %s 
                     WHERE (floornumber is Null or vattype is Null) and semantic is Null and
                     description is NOT Null"""

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data) 
                if string['floornumber'] == None:
                    field = result.iloc[0]["floornumber"]
                    if field != "unknown":
                        array[0] += 1
                        if type(field) == str:
                            field = 999
                        SQL1 = "UPDATE %s SET floornumber = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))
                
                # Field Vat type
                if string['vattype'] == None:
                    field = result.iloc[0]["vattype"]
                    if field != "unknown":
                        array[1] += 1
                        SQL1 = "UPDATE %s SET vattype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
                 
                
        # Обработка таблиц ... 
        elif table in ["placements", "offices", "offices_lease", "placements_clean", 
                       "placements_depr", "placements_depr_lease", "shoppings_lease",
                       "shoppings", "garages", "garages_lease", "buildings_offices_shoppings_free_lease", 
                       "buildings_industrials_warehouses_lease", "buildings", "buildings_lease",
                       "analogs", "placements_lease", "property", "industrials_warehouses", 
                       "industrials_warehouses_lease", "buildings_industrials_warehouses",
                       "commercial_property", "buildings_offices_shoppings_free", "relevant_property"
                      ]:
            SQL = """SELECT id, description, floornumber, conditiontype, entrance, hasshopwindows, 
                                houselinetype, isbuildingliving, vattype, semantic
                     FROM %s 
                     WHERE (floornumber is Null or conditiontype is Null or entrance is Null or 
                     hasshopwindows is Null or houselinetype is Null or isbuildingliving is Null or
                     vattype is Null) 
                     and (semantic is Null and description is NOT Null)
                  """

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data)
                
                # На каком этаже находится
                if string['floornumber'] == None:
                    field = result.iloc[0]["floornumber"]
                    if field != "unknown":
                        array[0] += 1
                        if type(field) == str:
                            field = 999
                        SQL1 = "UPDATE %s SET floornumber = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))
               
                # Condition type
                if string['conditiontype'] == None:
                    field = result.iloc[0]["conditiontype"]
                    if field != "unknown":
                        array[1] += 1
                        SQL1 = "UPDATE %s SET conditiontype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))
                    
                # Entrance
                if string['entrance'] == None:
                    field = result.iloc[0]["entrance"]
                    if field != "unknown":
                        array[2] += 1 
                        SQL1 = "UPDATE %s SET entrance = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))
                    
                # Витринные окна
                if string['hasshopwindows'] == None:
                    field = result.iloc[0]["hasshopwindows"]
                    if field == "no_display_window":
                        window = False
                    elif field == "display_window":
                        window = True
                    if field != "unknown":
                        array[3] += 1
                        SQL1 = "UPDATE %s SET hasshopwindows = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, window, string["id"]))
        
                # Линия застройки
                if string['houselinetype'] == None:
                    field = result.iloc[0]["houselinetype"]
                    if field != "unknown":
                        array[4] += 1
                        SQL1 = "UPDATE %s SET houselinetype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))

                # Жилое/не жилое
                if string['isbuildingliving'] == None:
                    field = result.iloc[0]["isbuildingliving"]
                    if field == "non_residential":
                        live = False
                    elif field == "residential":
                        live = True
                    if field != "unknown":
                        array[5] += 1
                        SQL1 = "UPDATE %s SET isbuildingliving = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, live, string["id"]))
                    
                # Vat type
                if string['vattype'] == None:
                    field = result.iloc[0]["vattype"]
                    if field != "unknown":
                        array[6] += 1
                        SQL1 = "UPDATE %s SET vattype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"]))         
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
                conn.commit()
                

        # Обработка таблиц "lands"
        elif table in ["lands"]:
            SQL = """SELECT id, description, vattype, semantic
                     FROM %s 
                     WHERE (vattype is Null) 
                     and (semantic is Null and description is NOT Null)
                  """

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data)
                
                # Vat type
                if string['vattype'] == None:
                    field = result.iloc[0]["vattype"]
                    if field != "unknown":
                        array[0] += 1
                        SQL1 = "UPDATE %s SET vattype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))            
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
                
        # Обработка таблиц "sas_commercial_requests", "сommercial_requests"
        elif table in ["sas_commercial_requests", "сommercial_requests"]:
            SQL = """SELECT id, description, isbuildingliving, semantic
                     FROM %s 
                     WHERE (isbuildingliving is Null) 
                     and (semantic is Null and description is NOT Null)
                  """

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data)
                # Жилое/не жилое
                if string['isbuildingliving'] == None:
                    field = result.iloc[0]["isbuildingliving"]
                    if field == "non_residential":
                        live = False
                    elif field == "residential":
                        live = True
                    if field != "unknown":
                        array[5] += 1
                        SQL1 = "UPDATE %s SET isbuildingliving = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, live, string["id"]))
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
        
        
        # Обработка таблиц industrials, industrials_lease, warehouses_lease, warehouses
        elif table in ["industrials", "industrials_lease", "warehouses_lease", "warehouses"]:
            SQL = """SELECT id, description, floornumber, conditiontype, vattype, semantic
                     FROM %s 
                     WHERE (floornumber is Null or conditiontype is Null or vattype is Null) 
                     and (semantic is Null and description is NOT Null)
                  """

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data)
                
                # На каком этаже находится
                if string['floornumber'] == None:
                    field = result.iloc[0]["floornumber"]
                    if field != "unknown":
                        array[0] += 1
                        if type(field) == str:
                            field = 999
                        SQL1 = "UPDATE %s SET floornumber = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))
               
                # Condition type
                if string['conditiontype'] == None:
                    field = result.iloc[0]["conditiontype"]
                    if field != "unknown":
                        array[1] += 1
                        SQL1 = "UPDATE %s SET conditiontype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))
                
                if string['vattype'] == None:
                    field = result.iloc[0]["vattype"]
                    if field != "unknown":
                        array[2] += 1
                        SQL1 = "UPDATE %s SET vattype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
                

        # Обработка таблиц commercial_requests_histrory
        elif table == "commercial_requests_histrory":
            SQL = """SELECT id, description, floornumber, conditiontype, entrance, hasshopwindows, 
                                houselinetype, isbuildingliving, semantic
                     FROM %s 
                     WHERE (floornumber is Null or conditiontype is Null or entrance is Null or 
                     hasshopwindows is Null or houselinetype is Null or isbuildingliving is Null) 
                     and (semantic is Null and description is NOT Null)
                  """

            cursor.execute(SQL % table)
            batch = cursor.fetchall()
            for string in batch:
                i+=1
                if i % 1000 == 0:
                    print ("String", i, "done!")
                data = string['description']
                result = start_parser(data)
                
                # На каком этаже находится
                if string['floornumber'] == None:
                    field = result.iloc[0]["floornumber"]
                    if field != "unknown":
                        array[0] += 1
                        if type(field) == str:
                            field = 999
                        SQL1 = "UPDATE %s SET floornumber = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))

                # Condition type
                if string['conditiontype'] == None:
                    field = result.iloc[0]["conditiontype"]
                    if field != "unknown":
                        array[1] += 1
                        SQL1 = "UPDATE %s SET conditiontype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))

                # Entrance
                if string['entrance'] == None:
                    field = result.iloc[0]["entrance"]
                    if field != "unknown":
                        array[2] += 1
                        SQL1 = "UPDATE %s SET entrance = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))
                    
                # Витринные окна
                if string['hasshopwindows'] == None:
                    field = result.iloc[0]["hasshopwindows"]
                    if field == "no_display_window":
                        window = False
                    elif field == "display_window":
                        window = True
                    if field != "unknown":
                        array[3] += 1
                        SQL1 = "UPDATE %s SET hasshopwindows = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, window, string["id"], ))
        
                # Линия застройки
                if string['houselinetype'] == None:
                    field = result.iloc[0]["houselinetype"]
                    if field != "unknown":
                        array[4] += 1
                        SQL1 = "UPDATE %s SET houselinetype = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, field, string["id"], ))
                    
                # Жилое/не жилое
                if string['isbuildingliving'] == None:
                    field = result.iloc[0]["isbuildingliving"]
                    if field == "non_residential":
                        live = False
                    elif field == "residential":
                        live = True
                    if field != "unknown":
                        array[5] += 1
                        SQL1 = "UPDATE %s SET isbuildingliving = '%s' WHERE id = %s"
                        cursor.execute(SQL1 % (table, live, string["id"], ))
                SQL1 = "UPDATE %s SET semantic = 'true' WHERE id = %s"
                cursor.execute(SQL1 % (table, string["id"]))
                

        print (table + ": done!")
    except Exception as e:
        print(e)   
    
    return array
        