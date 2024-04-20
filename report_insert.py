import os
import pandas as pd
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv, dotenv_values

load_dotenv()
#find latest excel report
def find_candidates_excel_file():
    downloads_path = os.path.abspath(os.getenv("XL_FILE_PATH"))
    latest_file = None
    latest_time = 0
    
    for filename in os.listdir(downloads_path):
        if 'candidates' in filename.lower() and filename.endswith('.xlsx'):
            file_path = os.path.join(downloads_path, filename)
            file_time = os.path.getctime(file_path)
            if file_time > latest_time:
                latest_file = file_path
                latest_time = file_time
    print(latest_file)
    return latest_file

 
# converting excel to dictionary
def excel_to_json(excel_file):

    excel_data = pd.read_excel(excel_file)
    excel_data.dropna(subset=['tag1'],inplace=True)
    dict_data = excel_data.to_dict(orient='records')
    print(len(dict_data))
    return dict_data

# inserting data into mongodb
def insert_json_to_mongodb(dict_data):
    client = MongoClient(os.getenv("MONGODB_URL"))
    db_name = os.getenv("DATABASE_NAME")
    collection_name= os.getenv("COLLECTION_NAME")
    db = client[db_name]
    collection = db[collection_name]

    for report in dict_data:
    # Extract tag values
        tags = [str(report[f'tag{i}']) for i in range(1, 4) if report.get(f'tag{i}') is not None]
        # Assigning tag values to id
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
        update_record = {"$set": {"report_data": report}}
        
        # Check if a document with matching tags exists
        existing_doc = collection.find(query)
        
        for doc in existing_doc:
            if doc:
                report_data=doc['report_data']
                #checking uniqueId 
                if 'UniqueId' in report_data and report_data['UniqueId'] == report['UniqueId']:
                        print("same uniqueId is detected")
                        continue  # Skip if the existing document has the same UniqueId
                else:
                    #inserting report_data into document
                    object_id = ObjectId(doc['_id'])
                    collection.find_one_and_update({'_id': object_id}, update_record)
                    print("Inserted document successfully!!")
                
            else:
                print("No document exists with similar id")
                
def delete_file(file_path):
    try:
       os.remove(file_path)
    #    pass
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
    else:
        print("No file detected")
        
if __name__ == "__main__":
    main()

