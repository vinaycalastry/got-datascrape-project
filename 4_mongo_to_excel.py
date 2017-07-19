#import addl for mongo, pandas, mongocredentials
from pymongo import MongoClient
import pandas as pd
from creds import *

MONGO_CONNECTION_STRING = MONGO_URI
MONGO_DB_NAME = DB_NAME
MONGO_COLLECTION_NAME = COLLECTION_NAME

def get_data_from_mongo(uri, db, collection):
    charactersList = []
    client = MongoClient(uri)
    database = client[db]
    collection = database[collection]
    for characters in collection.find():
        charactersList.append(characters)
    return charactersList

def create_excelsheet(characters):
    charListforExcel = pd.DataFrame(characters)
    print(charListforExcel)


def main():
    charList = get_data_from_mongo(MONGO_CONNECTION_STRING, MONGO_DB_NAME, MONGO_COLLECTION_NAME)
    create_excelsheet(charList)

if __name__ == '__main__':
    main()
