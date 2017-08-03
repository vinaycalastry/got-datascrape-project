from lib.parsewikia import FetchWikiaInfo

def main():
    file_name = 'charURL.csv' 
    with open(file_name) as f:
        for url in f:
            parsedwikidata = FetchWikiaInfo(url.strip())
            wiki_info = parsedwikidata.create_char_list()
            parsedwikidata.create_csv(wiki_info)


if __name__ == '__main__':
    main()