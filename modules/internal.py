#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#imports
from sqlite3 import connect
from subprocess import run
from requests import post
from os import system, name
from json import dumps
from asyncio import sleep as asyncsleep
from PIL import Image, ImageEnhance
from numpy import array
from cv2 import cvtColor, COLOR_RGB2BGR, COLOR_BGR2GRAY, threshold, THRESH_BINARY
from easyocr import Reader
from re import search
from rapidfuzz import process
#modules
from databases.shortnameslist import all_short_names_list as short_names_db

#clear terminal
def tclear():
    #for windows
    if name == 'nt':
        _ = system('cls')
    #for macOS
    else:
        _ = system('clear')

#search items on the tarkovapi
def search_items(query):
    response = post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def updatedb_items(itemslist:list):
    if not isinstance(itemslist, list):
        raise TypeError("The 'itemslist' argument must be a list.")
    
    #print("Updating Items Database")
    #opening a (new) database
    connection = connect("databases/database.db")
    cursor = connection.cursor()
    #creating table
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (
                   name TEXT UNIQUE, 
                   shortName TEXT, 
                   avg24hPrice TEXT, 
                   updated TEXT, 
                   types TEXT, 
                   lastLowPrice TEXT, 
                   changeLast48hPercent TEXT, 
                   iconLink TEXT, 
                   wikiLink TEXT,
                   width TEXT, 
                   height TEXT, 
                   receivedFromTasks TEXT, 
                   usedInTasks TEXT, 
                   sellFor TEXT)''')


    #formatting string in the GraphQL format for the query
    for i in range(len(itemslist)):
        if "\"" in itemslist[i]:
            itemslist[i] = itemslist[i].replace("\"", "\\\"")
    itemslistformatted = ', '.join(['"{}"'.format(item) for item in itemslist])
    #query
    query = """
            query {{
                items (names: [{0}]) {{
                    name
                    shortName
                    avg24hPrice
                    updated
                    types
                    lastLowPrice
                    changeLast48hPercent
                    iconLink
                    wikiLink
                    width
                    height
                    receivedFromTasks {{
                        name
                        wikiLink
                    }}
                    usedInTasks {{
                        name
                        wikiLink
                    }}
                    sellFor {{
                        price
                        vendor {{
                            name
                        }}
                    }}
                }}
            }}
    """.format(itemslistformatted)
    
    result = search_items(query)
    result = result["data"]["items"]
    #adding items to items table in database.db
    for itm in result:
        cursor.execute('''REPLACE INTO items (name, shortName, avg24hPrice, updated, types, lastLowPrice, changeLast48hPercent, iconLink, 
                       wikiLink, width, height, receivedFromTasks, usedInTasks, sellFor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (str(itm["name"]), str(itm['shortName']), str(itm["avg24hPrice"]), str(itm["updated"]), str(itm["types"]), str(itm["lastLowPrice"]), 
                        str(itm["changeLast48hPercent"]), str(itm["iconLink"]), str(itm["wikiLink"]), str(itm["width"]), str(itm["height"]), 
                        str(itm["receivedFromTasks"]), str(itm["usedInTasks"]), str(itm["sellFor"])))
    #closing items database & cursor
    try:
        connection.commit()
    except:
        connection.rollback()
    finally:
            cursor.close()
            connection.close()

def updatedb_ammo(ammolist: list):
    if not isinstance(ammolist, list):
        raise TypeError("The 'ammolist' argument must be a list.")

    # Opening a (new) database
    connection = connect("databases/database.db")
    cursor = connection.cursor()
    # Creating table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ammo (
                   name TEXT UNIQUE,
                   shortName TEXT,
                   types TEXT, 
                   iconLink TEXT, 
                   wikiLink TEXT, 
                   updated TEXT, 
                   sellFor TEXT, 
                   tracer INTEGER, 
                   tracerColor TEXT, 
                   damage TEXT, 
                   armorDamage TEXT, 
                   fragmentationChance TEXT, 
                   ricochetChance TEXT, 
                   penetrationChance TEXT, 
                   penetrationPower TEXT, 
                   accuracyModifier TEXT, 
                   recoilModifier TEXT, 
                   initialSpeed TEXT, 
                   lightBleedModifier TEXT, 
                   heavyBleedModifier TEXT)''')

    # Formatting string in the GraphQL format for the query
    for i in range(len(ammolist)):
        if "\"" in ammolist[i]:
            ammolist[i] = ammolist[i].replace("\"", "\\\"")
    ammolistformatted = ', '.join(['"{}"'.format(item) for item in ammolist])
    # Query
    query = """
            {{
                items(names: [{0}]) {{
                    properties {{
                        ...ItemProperties
                    }}
                    name
                    shortName
                    types
                    iconLink
                    wikiLink
                    updated
                    sellFor {{
                        price
                        vendor {{
                            name
                        }}
                    }}
                }}
            }}
            fragment ItemProperties on ItemPropertiesAmmo {{
                tracer
                tracerColor
                damage
                armorDamage
                fragmentationChance
                ricochetChance
                penetrationChance
                penetrationPower
                accuracyModifier
                recoilModifier
                initialSpeed
                lightBleedModifier
                heavyBleedModifier
            }}
            """.format(ammolistformatted)

    result = search_items(query)
    result = result["data"]["items"]
    # Removing ammo packs from the list
    resultfiltered = [item for item in result if "ammo" in item["types"] and "ammoBox" not in item["types"]]
    
    for item in resultfiltered:
        properties = item.get("properties", {})
        item.update(properties)
        
        cursor.execute('''REPLACE INTO ammo (
                          name, shortName, types, iconLink, wikiLink, updated, sellFor, 
                          tracer, tracerColor, damage, armorDamage, 
                          fragmentationChance, ricochetChance, penetrationChance, 
                          penetrationPower, accuracyModifier, recoilModifier, 
                          initialSpeed, lightBleedModifier, heavyBleedModifier) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            item.get("name", ""),
            item.get("shortName", ""),
            dumps(item.get("types", [])),  # Convert list to JSON string
            item.get("iconLink", ""),
            item.get("wikiLink", ""),
            item.get("updated", ""),
            dumps(item.get("sellFor", [])),  # Convert list to JSON string
            int(item.get("tracer", 0)),  # Convert boolean to integer
            item.get("tracerColor", ""),
            item.get("damage", ""),
            item.get("armorDamage", ""),
            item.get("fragmentationChance", ""),
            item.get("ricochetChance", ""),
            item.get("penetrationChance", ""),
            item.get("penetrationPower", ""),
            item.get("accuracyModifier", ""),
            item.get("recoilModifier", ""),
            item.get("initialSpeed", ""),
            item.get("lightBleedModifier", ""),
            item.get("heavyBleedModifier", "")
        ))

    # Closing ammo database & cursor
    try:
        connection.commit()
    except:
        connection.rollback()
    finally:
        cursor.close()
        connection.close()


def getdb_item(itemname:str):
    if not isinstance(itemname, str):
        raise TypeError("The 'itemname' argument must be a string.")

    #opening database
    connection = connect("databases/database.db")
    cursor = connection.cursor()
    #getting wanted item
    cursor.execute("""SELECT * FROM items WHERE name = ?""",(itemname,))
    #fetching
    result = cursor.fetchone()
    connection.close()
    return result

def getdb_ammo(ammoname:str):
    if not isinstance(ammoname, str):
        raise TypeError("The 'ammoname' argument must be a string.")

    #opening database
    connection = connect("databases/database.db")
    cursor = connection.cursor()
    #getting wanted item
    cursor.execute("""SELECT * FROM ammo WHERE name = ?""",(ammoname,))
    #fetching
    result = cursor.fetchone()
    connection.close()
    return result

def getdb_shortName(itemname:str):
    if not isinstance(itemname, str):
        raise TypeError("The 'itemname' argument must be a string.")
    
    #opening database
    connection = connect("databases/database.db")
    cursor = connection.cursor()
    #getting wanted item
    #cursor.execute("""SELECT * FROM items WHERE shortName = ?""",(itemname,))
    cursor.execute("""SELECT * FROM items WHERE shortName = ?""", (itemname,))
    #fetching
    result = cursor.fetchone()
    connection.close()
    return result

def adjust_auto_image(image):
    # Upscaling the image
    new_size = (image.width * 2, image.height * 2)
    upscaled_image = image.resize(new_size, Image.LANCZOS)
    #Sharpening the image
    enhancer = ImageEnhance.Sharpness(upscaled_image)
    img = enhancer.enhance(1.5)
    # Convert to OpenCV to further enhance
    img_cv = cvtColor(array(img), COLOR_RGB2BGR)
    # Convert to grayscale
    gray_image = cvtColor(img_cv, COLOR_BGR2GRAY)
    # Binarize the image (thresholding)
    _, binary_image = threshold(gray_image, 130, 255, THRESH_BINARY)
    return binary_image

def auto_ocr(binary_image):
    reader = Reader(['en'],  verbose=False, gpu=False)
    results = reader.readtext(binary_image, allowlist='''abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRTUVWXYZ0123456789-_'()&.,''', blocklist='/S')
    detected_texts = [result[1] for result in results]
    # Define regex patterns
    patterns = [r'\b\d+/\d+\b', r'\b\d+x\d+\b', r'^\d+$|^\(.*|.*\d+\(']
    detected_texts = [
        item for item in detected_texts 
        if not any(search(pattern, item) for pattern in patterns)
    ]
    # Function to find the best match with a threshold
    def find_best_match(text, name_list, threshold=75):
        best_match, score, index = process.extractOne(text, name_list)  # Updated to unpack three values
        return best_match if score >= threshold else None
    # Collect matches
    matches = []
    for detected_text in detected_texts:
        match = find_best_match(detected_text, short_names_db)
        if match:
            matches.append(match)
    # Collecting items to search in a dictionary
    items_to_search = {}
    for item in matches:
        if item not in items_to_search:
            items_to_search[item] = 1
        else:
            items_to_search[item] +=1
    
    return items_to_search

def auto_organize(iteminfo):
    #info tuple indexing
    name = iteminfo[0]
    if iteminfo[6] != 'None':
        changeLast48hPercent = iteminfo[6]
    else:
        changeLast48hPercent = 0
    types = eval(iteminfo[4])
    sellFor = eval(iteminfo[13])

    #sellFor
    max_sell = 0
    vendor_name = ""
    for vendor_data in sellFor:
        #converting dollars to roubles to compare
        if vendor_data["vendor"]["name"] == 'Peacekeeper':
            vendor_data["price"] = vendor_data["price"]*150
        if int(vendor_data["price"]) > max_sell and vendor_data["vendor"]["name"] != "Flea Market":
            max_sell = vendor_data["price"]
            vendor_name = vendor_data["vendor"]["name"]
    if vendor_name == 'Peacekeeper':
        max_sell = max_sell//150
        #flea market
    fleaPrice = 0
    flea = False
    if 'noFlea' in types:
        flea = False
    else:
        flea = True
    if flea:
        for vendor_data in sellFor:
            if vendor_data["vendor"]["name"] == 'Flea Market':
                fleaPrice = vendor_data["price"]
    
    return name, vendor_name, max_sell, flea, fleaPrice, changeLast48hPercent

async def updatedb(filename:str):
    while True:
        #execute file
        run([sys.executable, filename])
        #sleep 10 minutes
        await asyncsleep(600)
    #print("[+] Updating Database")