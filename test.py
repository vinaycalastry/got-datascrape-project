test1 = ['Tyrion Lannister', 'Lannister', 'Casterly Rock', 'Andal', 'Faith of the Seven', 'The Westerlands', 'House Lannister, House Targaryen', 'Hand of the King, Master of Coin, The Imp, Hand of the Queen', 'Tywin Lannister, Joanna Lannister', 'Cersei Lannister, Tyrion Lannister', 'TRUE', '265 AL', '', 'https://vignette3.wikia.nocookie.net/gameofthrones/images/4/4f/GoT-Sn7_FirstLook_14.jpg/revision/latest?cb=20170612171541', 'http://gameofthrones.wikia.com/wiki/Tyrion_Lannister']

test2 = ['Pypar', '', 'Acorn Hall', '', '', '', 'Night’s Watch', 'Stewards of Gondor', '', '', 'FALSE', '', '', 'https://vignette3.wikia.nocookie.net/gameofthrones/images/e/e6/Pypar-mockingbird.jpg/revision/latest?cb=20161215025708', 'http://gameofthrones.wikia.com/wiki/Pypar']

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



print(create_character_dict(test2))