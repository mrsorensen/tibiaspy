import requests
import re
import sys
import html

# Get (and print) info about character
def getCharacterInfo(charName):
    
    # URL for character info page
    url = "https://www.tibia.com/community/?subtopic=characters&name=" + charName

    # Get html from URL
    html = requests.get(url)

    # Try to find characters level, mainly to verify character name
    try:
        print("Level:          " + getCharacterLevel(html.text))
    except:
        print("Character not found")
    # Print default info
    else:
        print("Gender:         " + getCharacterSex(html.text))
        print("World:          " + getCharacterWorld(html.text))
        print("Vocation:       " + getCharacterVocation(html.text))
        print("Residence:      " + getCharacterResidence(html.text))

        # Try fo find guild info
        try:
            print("Guild:          " + getCharacterGuild(html.text))
        except:
            print("Guild:          None")

        # Try to find comment
        try:
            print("Comment:        " + getCharacterComment(html.text))
        except:
            print("Comment:        None")

        # Online status
        if getCharacterOnlineStatus(getCharacterWorld(html.text), charName) == True:
            print("Status:         Online")
        else:
            print("Status:         Offline")

        # Last login
        print("Last login:     " + getCharacterLastLogin(html.text))

def getCharacterLastLogin(html):

    result = re.search('<td>Last Login:</td><td>(.*?)</td></tr>', html)
    return result.group(1).replace("&#160;", " ")

def getCharacterOnlineStatus(server, charName):
    # Fix name spaces
    charName = charName.replace(" ", "\+")

    # URL to online list for server X
    url = "https://www.tibia.com/community/?subtopic=worlds&world=" + server.capitalize()

    # Store result from get request to URL
    html = requests.get(url)

    # Result of regex search in the plain html code from above
    result = re.search('\?subtopic=characters&name=' + charName + '">', html.text)
    
    # Return true if the result is not "none"
    if result != None:
        return True


def getCharacterComment(html):

    result = re.search('<td valign=top>Comment:<\/td><td>(.*?)<br \/>', html)
    return result.group(1)


def getCharacterGuild(html):

    result = re.search('Guild&#160;Membership:<\/td><td>(.*?)<(.*?)>(.*?)<\/a>', html)
    guildName = result.group(3).replace("&#160;", " ")
    return guildName


def getCharacterResidence(html):

    result = re.search('Residence:<\/td><td>(.*?)<', html)
    return result.group(1)


def getCharacterVocation(html):

    result = re.search('Vocation:<\/td><td>(.*?)<', html)
    return result.group(1)


# Get world of character 
def getCharacterWorld(html):
    
    # Serach the html for world
    result = re.search('World:<\/td><td>(.*?)<', html)
    return result.group(1)


# Get sex of character 
def getCharacterSex(html):
    
    # Serach the html for gender info
    result = re.search('Sex:<\/td><td>(.*?)<', html)
    return result.group(1)


# Get level of character
def getCharacterLevel(html):
    
    # Search the html for level
    result = re.search('td>Level:<\/td><td>(\d+)<\/td>', html)
    return result.group(1)









name = input("Name:           ")
name = name.title()

charInfo = getCharacterInfo(name)


