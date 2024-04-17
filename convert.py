import pandas as pd
from pymongo import MongoClient



def excel_to_json(excel_file):
    excel_data = pd.read_excel(excel_file) 
    json_data = excel_data.to_dict(orient='records')
    print(type(json_data))
    return json_data


def insert_json_to_mongodb(json_data):
    dict_data={
        "name":"abc",
        "age":"23"
    }
    client = MongoClient("mongodb://localhost:27017/")
    db=client.userdb
    collection=db.userdata
    collection.insert_many(json_data)



db_name = 'userdb'
collection_name = 'userdata'

excel_file_path = './candidates.xlsx' 
json_data = excel_to_json(excel_file_path)

print(json_data)

insert_json_to_mongodb(json_data)
    

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