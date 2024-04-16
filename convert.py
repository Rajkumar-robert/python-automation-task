import pandas as pd
from pymongo import MongoClient



def excel_to_json(excel_file):
    excel_data = pd.read_excel(excel_file) 
    df = pd.DataFrame(excel_data)
    json_data = df.to_json(orient='records')
    return json_data

excel_file_path = './candidates.xlsx' 
json_data = excel_to_json(excel_file_path)
print(json_data)


def insert_json_to_mongodb(json_data,db_name,collection_name):
    client = MongoClient()
    client = MongoClient("mongodb://localhost:27017/")
    db=client[db_name]
    collection=db[collection_name]
    collection.insert_many(json_data)

db_name = 'userdb'
collection_name = 'userdata'

insert_json_to_mongodb(json_data, db_name, collection_name)
    

# def excel_to_jsonfile(excel_file, json_file):
#     excel_data = pd.read_excel(excel_file) 
#     df = pd.DataFrame(excel_data)
#     json_data = df.to_json(orient='records')
#     with open(json_file, 'w') as f:
#         f.write(json_data)

# excel_file_path = './candidates.xlsx' 
# json_file_path = './candidates.json'

# excel_to_jsonfile(excel_file_path, json_file_path)
# print(f"JSON data saved to '{json_file_path}'")