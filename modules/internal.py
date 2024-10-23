#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#imports
import sqlite3
import subprocess
from requests import post
from os import system, name
import asyncio, json

from databases.ammolist import all_ammo_list as all_ammo_list_db
from databases.itemslist import items_list as items_list_db

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
    connection = sqlite3.connect("databases/database.db")
    cursor = connection.cursor()
    #creating table
    cursor.execute('''CREATE TABLE IF NOT EXISTS items (name TEXT UNIQUE, avg24hPrice TEXT, updated TEXT, 
                       types TEXT, lastLowPrice TEXT, changeLast48hPercent TEXT, iconLink TEXT, wikiLink TEXT,
                       width TEXT, height TEXT, receivedFromTasks TEXT, usedInTasks TEXT, sellFor TEXT)''')


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
        cursor.execute('''REPLACE INTO items (name, avg24hPrice, updated, types, lastLowPrice, changeLast48hPercent, iconLink, 
                       wikiLink, width, height, receivedFromTasks, usedInTasks, sellFor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                       ''', (str(itm["name"]), str(itm["avg24hPrice"]), str(itm["updated"]), str(itm["types"]), str(itm["lastLowPrice"]), 
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
    connection = sqlite3.connect("databases/database.db")
    cursor = connection.cursor()
    # Creating table
    cursor.execute('''CREATE TABLE IF NOT EXISTS ammo (
                      name TEXT UNIQUE, 
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
                          name, types, iconLink, wikiLink, updated, sellFor, 
                          tracer, tracerColor, damage, armorDamage, 
                          fragmentationChance, ricochetChance, penetrationChance, 
                          penetrationPower, accuracyModifier, recoilModifier, 
                          initialSpeed, lightBleedModifier, heavyBleedModifier) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
            item.get("name", ""),
            json.dumps(item.get("types", [])),  # Convert list to JSON string
            item.get("iconLink", ""),
            item.get("wikiLink", ""),
            item.get("updated", ""),
            json.dumps(item.get("sellFor", [])),  # Convert list to JSON string
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
    connection = sqlite3.connect("databases/database.db")
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
    connection = sqlite3.connect("databases/database.db")
    cursor = connection.cursor()
    #getting wanted item
    cursor.execute("""SELECT * FROM ammo WHERE name = ?""",(ammoname,))
    #fetching
    result = cursor.fetchone()
    connection.close()
    return result

async def updatedb(filename:str):
    while True:
        #execute file
        subprocess.run(["python", filename])
        #sleep 10 minutes
        await asyncio.sleep(600)
    #print("[+] Updating Database")