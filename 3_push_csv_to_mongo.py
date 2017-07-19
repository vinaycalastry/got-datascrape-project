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
MONGO_COLLECTION_NAME = COLLECTION_NAME

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


#Function to create a character dict to push to mongo
def create_character_dict(character):
    """ Create and return a character dictionary with required info """
    characterDict = {}
    characterDict["FullName"] = str(character[0])
    characterDict["House"] = str(character[1])
    characterDict["Origin"] = str(character[2])
    characterDict["Culture"] = str(character[3])
    characterDict["Religion"] = [x.strip() for x in str(character[4]).split(',')]
    characterDict["Kingdom"] = str(character[5])
    characterDict["Allegiance"] = [x.strip() for x in str(character[6]).split(',')]
    characterDict["Titles"] = [x.strip() for x in str(character[7]).split(',')]
    characterDict["Parents"] = [x.strip() for x in str(character[8]).split(',')]
    characterDict["Siblings"] = [x.strip() for x in str(character[9]).split(',')]
    characterDict["Alive"] = bool(str(character[10]))
    characterDict["Birth"] = str(character[11])
    characterDict["Death"] = str(character[12])
    characterDict["Image"] = str(character[13])
    characterDict["WikiPage"] = str(character[14])
    return characterDict

#def move the cast list to mongo

def insert_characterlist_mongo(characterList):
    """Bulk Insert to MongoDB """
    #MONGO_URI, DB_NAME and COLLECTION_NAME is from creds file
    client = MongoClient(MONGO_URI)
    db = client[MONGO_DB_NAME]
    Names = db[MONGO_COLLECTION_NAME]
    result = Names.insert_many(characterList)

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
    rangeName = SPREADSHEET_RANGE #from creds file
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheetId, range=rangeName).execute()
    values = result.get('values', [])


    #Adding list to hold values to hold cast to push to mongo
    cast = []
    
    if not values:
        print('No data found.')
    else:
        try:
            for row in values:
                #Adding dict to hold cast information
                cast.append(create_character_dict(row))
                
            insert_characterlist_mongo(cast)
        except Exception as e:
            print('Error has occurred' + str(e))



if __name__ == '__main__':
    main()