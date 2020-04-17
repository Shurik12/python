# Import libreries:

from sshtunnel import SSHTunnelForwarder
from pymongo import MongoClient
from start import start_parser # исполняемый файл с парсером
import openpyxl as px # работа с  xlsx файлами
import codecs # запись в текстовый формат

# Using functions:

# Establish a connection with Mongodb
def connect_mongodb(MONGO_PORT, MONGO_DB, MONGO_USER, MONGO_PASS, SERVER_HOST, SERVER_PORT):
    server = SSHTunnelForwarder(
                                (SERVER_HOST, SERVER_PORT),
                                ssh_username = MONGO_USER,
                                ssh_password = MONGO_PASS,
                                remote_bind_address = ('localhost', MONGO_PORT)
                               )
    server.start()
    print("Connection established with local bin port: ", server.local_bind_port)
    client = MongoClient('localhost', server.local_bind_port)
    return (client[MONGO_DB])

def Parser_Mongo(db, collection):
    try:
        #for collection in db.collection_names():
        print (collection + ' start!')
        if collection == "building":
            # смотрим коллекцию объявлений где признак null, в нашем случае лучше сделать рекурсию,
            #что бы этот процесс не заканчивался
            for a in db[collection].find({"$and":
                                            [{"pageId": {"$ne": None}}, 
                                                    {"sematic":{"$eq": None}}]}, 
                                                       {"building_house_line_type": 1, 
                                                        "condition_type": 1, 
                                                        "description": 1,
                                                        "vat_type" : 1, 
                                                        "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)   
                if a['building_house_line_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                            {"building_house_line_type": result.iloc[0]["houselinetype"]}})
                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                                {"$set": 
                                                                {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                            {"vat_type": result.iloc[0]["vattype"]}})           
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                            {"sematic": "true"}})

        elif collection == "storage":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                           {"floor_number": 1, 
                                                            "condition_type": 1,
                                                            "description": 1,
                                                            "vat_type" : 1, 
                                                            "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)
                if a['floor_number'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"floor_number": result.iloc[0]["conditiontype"]}})
                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})

        elif collection == "garage":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                           {"vat_type" : 1,
                                                            "description": 1,
                                                            "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)       
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})

        elif collection == "psn": 
            for a in db[collection].find({"$and":
                                          [{"pageId": {"$ne": None}}, 
                                           {"sematic":{"$eq": None}}
                                          ]
                                         },
                                         {"description": 1,
                                          "has_shop_windows": 1, 
                                          "floor_number": 1, 
                                          "condition_type": 1, 
                                          "vat_type": 1,
                                          "pageId": 1
                                         }
                                        ).batch_size(30): 
                data = a['description']
                result = start_parser(data)
                if a['floor_number'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"floor_number": str(result.iloc[0]["floornumber"])}})

                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['has_shop_windows'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"has_shop_windows": result.iloc[0]["hasshopwindows"]}}) 
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})

        elif collection == "tradingArea":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                       {"floor_number": 1, 
                                                        "description": 1,
                                                        "condition_type": 1, 
                                                        "vat_type" : 1, 
                                                        "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)                         
                if a['floor_number'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"floor_number": str(result.iloc[0]["floornumber"])}})                                  
                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})

        elif collection == "production":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                       {"floor_number": 1, 
                                                        "condition_type": 1, 
                                                        "description": 1,
                                                        "vat_type" : 1, 
                                                        "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)    
                if a['floor_number'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"floor_number": str(result.iloc[0]["floornumber"])}})                                
                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})  
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})       
        elif collection == "land":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                         {"vat_type" : 1, 
                                                          "description": 1,
                                                          "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data)       
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})                  
        elif collection == "office":
            for a in db[collection].find({"$and":
                                                        [{"pageId": {"$ne": None}}, 
                                                         {"sematic":{"$eq": None}}]}, 
                                                         {"floor_number": 1, 
                                                          "condition_type": 1,
                                                          "description": 1,
                                                          "vat_type": 1,
                                                          "pageId": 1}).batch_size(30):
                data = a['description']
                result = start_parser(data) 
                if a['floor_number'] == None:
                    res = result.iloc[0]["floornumber"]
                    if res == 0 or res ==-1 or res == 1 or res == 2:
                        db[collection].update_one({"pageId": a["pageId"]},
                                                                {"$set": 
                                                                 {"floor_number": float(res)}})
                    elif res == "unknown":
                        db[collection].update_one({"pageId": a["pageId"]},
                                                                {"$set": 
                                                                 {"floor_number": None}})

                    else:
                        db[collection].update_one({"pageId": a["pageId"]},
                                                                {"$set": 
                                                                 {"floor_number": 999}})

                if a['condition_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"condition_type": result.iloc[0]["conditiontype"]}})
                if a['vat_type'] == None:
                    db[collection].update_one({"pageId": a["pageId"]},
                                                            {"$set": 
                                                             {"vat_type": result.iloc[0]["vattype"]}})
                db[collection].update_one({"pageId": a["pageId"]},
                                                        {"$set": 
                                                        {"sematic": "true"}})
        print (collection + ' done!')   
        #get_urls()   
            #print("1")
    except Exception as e:
        print(e)
        
def save_sematic_info(collection, id):
    collection.update_one({"pageId": id}, {"$set": {" sematic": 'true'}})

