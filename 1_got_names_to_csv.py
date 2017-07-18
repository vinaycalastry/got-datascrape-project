# Import requests, bs4 and pandas
import requests
from bs4 import BeautifulSoup
from bs4 import NavigableString
import pandas as pd

#Get the page and parse with html parser
page = requests.get("https://en.wikipedia.org/wiki/List_of_Game_of_Thrones_characters#Main_cast")
soup = BeautifulSoup(page.content, "html.parser")

#Find the table containing result
tableMain = list(soup.findAll("table", attrs={ 'class': 'wikitable' }))[:2]


#Loop through table for row and get only 2nd row containing character names
dataList = []
for table in tableMain:
    for items in table.findAll("tr"):
        cells = items.findAll("td")
        #Some are empty, so check before getting 2nd element, List index out of range error
        if len(cells) == 0:
            pass
        else:
            for cell in cells[1]:
                #print(cell)
                try:
                    dataList.append(cell.text)
                except Exception as e:
                    dataList.append(cell)
                
    

#Create a Pandas dataframe and write the result to csv
dataStr = pd.DataFrame(dataList)
dataStr.to_csv("characters.csv", encoding='utf-8', index=False, header=None)


