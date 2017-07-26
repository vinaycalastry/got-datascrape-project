from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

#import addl for mongo
from pymongo import MongoClient

#import important info from creds
from creds import *

MONGO_DB_NAME = DB_NAME
MONGO_COLLECTION_NAME = COLLECTION_HOUSE

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


#Function to create a house dict to push to mongo
def create_house_dict(house):
    """ Create and return a house dictionary with required info """
    houseDict = {}
    houseDict["House"] = str(house[0]).strip()
    houseDict["Type"] = str(house[1]).strip()
    houseDict["Status"] = str(house[2]).strip()
    houseDict["Sigil"] = str(house[3]).strip()
    houseDict["Words"] = str(house[4]).strip()
    houseDict["Common Saying"] = str(house[5]).strip()
    houseDict["Allegiance"] = [x.strip() for x in str(house[6]).split(',')]
    houseDict["Founder"] = str(house[7]).strip()
    houseDict["Date Of Founding"] = str(house[8]).strip()
    houseDict["Age"] = str(house[9]).strip()
    houseDict["Religion"] = str(house[10]).strip()
    houseDict["Lord"] = [x.strip() for x in str(house[11]).split(',')]
    houseDict["Ancestral Seat"] = str(house[12]).strip()
    houseDict["Regions"] = [x.strip() for x in str(house[13]).split(',')]
    houseDict["Titles"] = [x.strip() for x in str(house[14]).split(',')]
    houseDict["Vassals"] = [x.strip() for x in str(house[15]).split(',')]
    houseDict["Image"] = str(house[16]).strip()
    houseDict["WikiPage"] = str(house[17]).strip()
    return houseDict

#def move the cast list to mongo

def insert_houseslist_mongo(houseList):
    """Bulk Insert to MongoDB """
    #MONGO_URI, DB_NAME and COLLECTION_NAME is from creds file
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    Names = db[MONGO_COLLECTION_NAME]
    result = Names.insert_many(houseList)

def main():
    """Shows basic usage of the Sheets API.

    Creates a Sheets API service object and prints the names and majors of
    students in a sample spreadsheet:
    https://docs.google.com/spreadsheets/d/1NQhMc0qNt-7snzCHo_hE-pKC0nFqrgwM5lZHmOX5Cwo/edit
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = SPREADSHEET_ID #from creds file
    rangeName = SPREADSHEET_RANGE_HOUSES #from creds file
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])

    #Adding list to hold values to hold cast to push to mongo
    houses = []
    
    if not values:
        print('No data found.')
    else:
        try:
            for row in values:
                #Adding dict to hold cast information
                houses.append(create_house_dict(row)) 
            #insert_houseslist_mongo(houses)
            insert_houseslist_mongo(houses)    
        except Exception as e:
            print('Error has occurred: ' + str(e))



if __name__ == '__main__':
    main()