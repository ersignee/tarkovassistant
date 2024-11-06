from requests import post

def search_items(query):
    response = post('https://api.tarkov.dev/graphql', json={'query': query})
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(response.status_code, query))

def update_file(filename:str, filelistname:str, inputlist:list[str]):
    with open(filename, 'w', encoding='utf-8') as f:
        for i, name in enumerate(all_ammo_list):
            if i + 1 == len(all_ammo_list):
                if "'" in name or '"' in name:
                    f.write(f"'''{name}''']")
                else:
                    f.write(f"'{name}']")
            elif i == 0:
                if "'" in name or '"' in name:
                    f.write(f"{filelistname} = ['''{name}''', ")
                else:
                    f.write(f"{filelistname} = ['{name}', ")
            elif i % 2 == 0:
                if "'" in name or '"' in name:
                    f.write(f"'''{name}''', \n\t")
                else:
                    f.write(f"'{name}', \n\t")
            else:
                if ("'" in name or '"' in name):
                    f.write(f"'''{name}''', ")
                else:
                    f.write(f"'{name}', ")

def formatquery(searchtype:str):
    match searchtype:
        case "ammo":
            search = "type"
            name = searchtype
            getshortName = "shortName"
        case "grenade":
            search = "type"
            name = searchtype
            getshortName = ""
        case "items":
            search = "lang"
            name = "en"
            getshortName = "shortName"
        case _:
            return
    query = """
    query
    {{
        items({0}: {1}){{
                name
                {2}
                }}
    }}""".format(search, name, getshortName)
    return query

# Call API for updated items list
ammo = search_items(formatquery('ammo'))["data"]["items"]
grenades = search_items(formatquery('grenade'))["data"]["items"]
items = search_items(formatquery('items'))["data"]["items"]

# Get items for the /ammo command and update the ammolist.py
all_ammo_list = list({amm0['name'] for amm0 in ammo if amm0 not in grenades})
update_file('./databases/ammolist.py', 'all_ammo_list', all_ammo_list)

# Get items for the /item command and update the itemslist.py
items_list = list({itm['name'] for itm in items if itm not in all_ammo_list})
update_file('./databases/itemslist.py', 'items_list', items_list)

# Get items for the /auto command and update the shortnameslist.py
all_ammo_short_names = [amm0short['shortName'] for amm0short in ammo]
all_short_names_list = list({itm['shortName'] for itm in items if itm['shortName'] not in all_ammo_short_names})
update_file('./databases/shortnameslist.py', 'all_short_names_list', all_short_names_list)