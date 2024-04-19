import os
import pandas as pd
from pymongo import MongoClient
from bson.objectid import ObjectId

        
# CONVERTING EXCEL TO DICTIONARY
def excel_to_json(excel_file):
    # Read Excel file
    excel_data = pd.read_excel(excel_file)
    
    # Replace NaN values with empty strings
    excel_data.fillna("", inplace=True)
    
    # Convert DataFrame to dictionary
    dict_data = excel_data.to_dict(orient='records')

    return dict_data

# INSERTING DATA INTO DATABASE
def insert_json_to_mongodb(dict_data):
    client = MongoClient(os.getenv("MONGODB_URL"))
    db = client.userdb
    collection = db.newUserData

    for doc in dict_data:
    # Extract tag values
        tags = [str(doc[f'tag{i}']) for i in range(1, 4) if doc.get(f'tag{i}') is not None]

        if tags[0] != "":
        # Assigning tag values to variables
            tag1 = tags[0] if tags[0] else ''
            tag2_values = tags[1].split(';') if len(tags) > 1 else []
            tag3_values = tags[2].split(';') if len(tags) > 2 else []

            query = {
                'learner_id': ObjectId(tag1),
                'program_id': ObjectId(tag2_values[0]),
                'module_id': ObjectId(tag2_values[1]),
                'activity_id': ObjectId(tag2_values[2]),
                'super_admin': ObjectId(tag3_values[0]),
                'organization_id': ObjectId(tag3_values[1]),
            }
            update_record = {"$set": {"report_data": doc}}
            # Check if a document with matching tags exists
            existing_doc = collection.find_one(query)

            if existing_doc:
                if 'record_data' in existing_doc and existing_doc['record_data.UniqueId'] == doc['UniqueId']:
                    print("same unique id is existing")
                    continue  # Skip if the existing document has the same UniqueId

                object_id = ObjectId(existing_doc['_id'])
                print(object_id)
                collection.find_one_and_update({'_id': object_id}, update_record)
            else:
                print("No document exists with similar id")


excel_file_path = './candidates.xlsx'
dict_data = excel_to_json(excel_file_path)

# print(dict_data)

insert_json_to_mongodb(dict_data)
