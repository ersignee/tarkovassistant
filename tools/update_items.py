import requests

def search_items(query):
    response = requests.post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

#ammo - used for the command /ammo
query1 = """
query
{
    items(type: ammo) {
        name
        shortName
    }
}
"""

#weapons
query2 = """
query
{
    items(type: gun) {
        name
    }
}
"""

#grenades
query3 = """
query
{
    items(type: grenade) {
        name
    }
}
"""

#all - used for the command /item (have to subtract ammo list from this)
query4 = """
query
{
  	items(lang: en){
    		name
  }
}
"""

#all short names - used for the command /auto
query5 = """
query
{
  	items(lang: en){
    		shortName
  }
}
"""
######### Retrive new Ammo #########

all_ammo_list = []
items_list = []
all_short_names_list = []

ammo = search_items(query1)
ammo = ammo["data"]["items"]
grenades = search_items(query3)
grenades = grenades["data"]["items"]
items = search_items(query4)
items = items["data"]["items"]
shortnames = search_items(query5)
shortnames = shortnames["data"]["items"]

# Get items for the /ammo command and update the ammolist.py
for amm0 in ammo:
    if amm0 not in grenades:
        all_ammo_list.append(amm0['name'])

all_ammo_list = list( dict.fromkeys(all_ammo_list))
counter = 0
with open('./databases/ammolist.py', 'w', encoding='utf-8') as f:
    for i, iteem in enumerate(all_ammo_list):
        if i+1 == len(all_ammo_list):
            f.write("'"+iteem+"']")
        elif i+1 == len(all_ammo_list) and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''']")
        elif i == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("all_ammo_list = ['"+iteem+"', ")
        elif i == 0 and ("'" in iteem or '"' in iteem):
            f.write("all_ammo_list = ['''"+iteem+"''', ")
        elif i % 2 == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("'"+iteem+"', \n\t")
        elif i % 2 == 0 and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''', \n\t")
        else:
            if ("'" in iteem or '"' in iteem):
                f.write("'''"+iteem+"''', ")
            else:
                f.write("'"+iteem+"', ")

# Get items for the /ammo command and update the ammolist.py
for itm in items:
    if itm not in all_ammo_list:
        items_list.append(itm['name'])

items_list = list( dict.fromkeys(items_list))
counter = 0
with open('./databases/itemslist.py', 'w', encoding='utf-8') as f:
    for i, iteem in enumerate(items_list):
        if i+1 == len(items_list):
            f.write("'"+iteem+"']")
        elif i+1 == len(items_list) and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''']")
        elif i == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("items_list = ['"+iteem+"', ")
        elif i == 0 and ("'" in iteem or '"' in iteem):
            f.write("items_list = ['''"+iteem+"''', ")
        elif i % 2 == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("'"+iteem+"', \n\t")
        elif i % 2 == 0 and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''', \n\t")
        else:
            if ("'" in iteem or '"' in iteem):
                f.write("'''"+iteem+"''', ")
            else:
                f.write("'"+iteem+"', ")


# Get items for the /ammo command and update the ammolist.py
all_ammo_short_names = []
for amm0short in ammo:
    all_ammo_short_names.append(amm0short['shortName'])

for shortname in shortnames:
    if shortname['shortName'] not in all_ammo_short_names:
        all_short_names_list.append(shortname['shortName'])

all_short_names_list = list( dict.fromkeys(all_short_names_list))
counter = 0
with open('./databases/shortnameslist.py', 'w', encoding='utf-8') as f:
    for i, iteem in enumerate(all_short_names_list):
        if i+1 == len(all_short_names_list):
            f.write("'"+iteem+"']")
        elif i+1 == len(all_short_names_list) and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''']")
        elif i == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("all_short_names_list = ['"+iteem+"', ")
        elif i == 0 and ("'" in iteem or '"' in iteem):
            f.write("all_short_names_list = ['''"+iteem+"''', ")
        elif i % 2 == 0 and not ("'" in iteem or '"' in iteem):#
            f.write("'"+iteem+"', \n\t")
        elif i % 2 == 0 and ("'" in iteem or '"' in iteem):
            f.write("'''"+iteem+"''', \n\t")
        else:
            if ("'" in iteem or '"' in iteem):
                f.write("'''"+iteem+"''', ")
            else:
                f.write("'"+iteem+"', ")