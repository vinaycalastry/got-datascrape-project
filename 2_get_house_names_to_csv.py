import requests
from bs4 import BeautifulSoup
import pandas as pd

def house_name(characterName):
    """Requests for the character and gets the reqd info """
    names = characterName.split()
    if len(names) == 1:
        return ""
    else:
        return names[1]



charactersHouseNames = []
with open("characters.csv", "r") as characters:
    for char in characters:
        if char.strip("\t\n\r") == '0':
            pass
        else:
            charName = char.strip("\t\n\r")
            houseName = house_name(charName)

            charactersHouseNames.append((charName, houseName))



dataStr = pd.DataFrame(charactersHouseNames)
dataStr.to_csv("characters_houses.csv", encoding='utf-8', index=False, header=None)




    

