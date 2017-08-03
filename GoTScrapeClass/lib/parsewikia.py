# Import requests, bs4 and pandas
import requests
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
import os, sys

class FetchWikiaInfo():
    """ To create csv and create list""" 
    def __init__(self, wikia_url):
        self.wikia_url = wikia_url
        self.parsed_wikia_url = requests.get(wikia_url)

    def create_csv(self, dataList):
        if not os.path.isdir('characters'):
            os.makedirs('characters')
            
        filename = str(os.getcwd()) + '/characters/' + str(dataList[0][1]) + '.csv'
        dataStr = pd.DataFrame(dataList)
        dataStr.to_csv(filename, encoding='utf-8', index=None, header=None)
    
    def create_char_list(self):
        """Main stuff here """
        soup = BeautifulSoup(self.parsed_wikia_url.content, "html.parser")
        #Infobox
        infoBox = soup.findAll("aside", attrs={'class': 'portable-infobox pi-background pi-theme-wikia pi-layout-default'})

        infoDict = {}        
        infoList = []

        for info in infoBox:
            infoDict["FullName"] = info.find("", attrs = {'class': 'pi-item pi-item-spacing pi-title'}).text
            
            image = str(info.find("", attrs = {'class': 'pi-image-thumbnail'}))
            infoDict["Image"] = image[image.find('src="')+5 : image.find(' srcset="')-2]
            
            infoDict["URL"] = self.wikia_url
            
            for others in info.findAll("div", attrs = {'class': 'pi-item pi-data pi-item-spacing pi-border-color'}):
                name = str(others.find("h3", attrs = {'class': 'pi-data-label pi-secondary-font'}).text)
                value = str(others.find("div", attrs = { 'class': 'pi-data-value pi-font'}).text)
                infoDict[name] = value
            
        for (key,value) in infoDict.items():
            infoList.append([key, value])


        return infoList
