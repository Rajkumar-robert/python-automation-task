import os
import pandas as pd
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()
def find_candidates_excel_file():
    folder_path = os.getenv("XL_FILE_PATH")
    print(folder_path)
    downloads_path = os.path.abspath(folder_path)
    latest_file = None
    latest_time = 0
    
    for filename in os.listdir(downloads_path):
        if 'candidates' in filename.lower() and filename.endswith('.xlsx'):
            file_path = os.path.join(downloads_path, filename)
            file_time = os.path.getctime(file_path)
            if file_time > latest_time:
                latest_file = file_path
                latest_time = file_time
    
    return latest_file

 
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
    collection = db.UserDataTest

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
               
                report_data=existing_doc['report_data']
                if 'UniqueId' in report_data:
                   
                    
                    if report_data['UniqueId'] == doc['UniqueId']:
                        print("same unique id is existing")
                        continue  # Skip if the existing document has the same UniqueId
             
                object_id = ObjectId(existing_doc['_id'])
                if object_id:
                    collection.find_one_and_update({'_id': object_id}, update_record)
                    print("Inserted document successfully!!")
                   
            else:
                print("No document exists with similar id")
                
def delete_file(file_path):
    try:
       # os.remove(file_path)
       pass
    except PermissionError:
        print("File is still being used by another process. Trying again in 3 seconds...")
        time.sleep(3)
        os.remove(file_path)


def main():
    excel_file_path = find_candidates_excel_file()
    if excel_file_path:
        print("Found Excel file with 'candidates' in its name:")
        dict_data = excel_to_json(excel_file_path)
        insert_json_to_mongodb(dict_data)
        delete_file(excel_file_path)
        print("Excel file deleted.")
        
if __name__ == "__main__":
    main()

