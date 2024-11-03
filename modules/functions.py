#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#imports
from nextcord import Interaction, Embed, Attachment
from time import strptime, strftime
from datetime import datetime
from aiohttp import ClientSession
from io import BytesIO
from PIL import Image
#modules
import modules.internal as internal
from databases.ammolist import all_ammo_list
from databases.itemslist import items_list

async def ammo(interaction:Interaction, name: str):
    #if the ammo doesnt exist returns error message to the user
    if name not in all_ammo_list:
        await interaction.response.defer(ephemeral=True)
        error = "{0} not found. Make sure to spell the name correctly and if the issue persists use `/bug` to report the issue. Thank you.".format(name)
        embed = Embed(title='**Error: Ammo Not Found**', color=0x2b2d31)
        embed.add_field(name="", value=error, inline= False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        print("Error in ammo(functions.py) caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)
        return
    
    await interaction.response.defer()
    #searching name in the ammo database
    ammoinfo = internal.getdb_ammo(name)
    #info tuple indexing
    ammoname = ammoinfo[0]
    types = ammoinfo[1] #list
    iconLink = ammoinfo[2]
    wikiLink = ammoinfo[3]
    updated = ammoinfo[4]
    sellFor = ammoinfo[5] #list
    tracer = bool(ammoinfo[6]) #bool
    tracerColor = ammoinfo[7]
    damage = int(ammoinfo[8]) #int
    armorDamage = int(ammoinfo[9]) #int
    fragmentationChance = float(ammoinfo[10]) #float
    ricochetChance = float(ammoinfo[11]) #float
    penetrationPower = int(ammoinfo[13]) #int
    accuracyModifier = float(ammoinfo[14]) #float
    recoilModifier = float(ammoinfo[15]) #float
    initialSpeed = int(ammoinfo[16]) #int
    lightBleedModifier = float(ammoinfo[17]) #float
    heavyBleedModifier = float(ammoinfo[18]) #float

    #converting variables from string back to original type
        #types
    types = eval(types)
        #sellFor
    sellFor = eval(sellFor)
        #tracer
    #tracer = eval(tracer.capitalize())
    
    #preparing variables for the embed
        #updated
    updated = strftime("%d/%m/%y %H:%M:%S", strptime(updated, "%Y-%m-%dT%H:%M:%S.%fZ"))
    actual_date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    d1 = datetime.strptime(updated, "%d/%m/%y %H:%M:%S")
    d2 = datetime.strptime(actual_date, "%d/%m/%y %H:%M:%S")
    delta = d2 - d1
    hours = (delta.seconds)//3600
    minutes = (delta.seconds)//60
    if minutes > 60:
        if hours > 1:
            updated = f'⌛Last updated: {hours} hours and {minutes-(hours*60)} minutes ago'
        else:
            updated = f'⌛Last updated: 1 hour and {minutes-(hours*60)} minutes ago'
    else:
        if minutes > 1:
            updated = f'⌛Last updated: {minutes} minutes ago'
        else:
            updated = f'⌛Last updated: 1 minute ago'
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
    
        #fragmentationChance
    fragmentationChance = str("%.0f" % (fragmentationChance*100))+"%"
        #ricochetChance
    ricochetChance = str("%.0f" % (ricochetChance*100))+"%"
        #penetrationPower
    penetrationPower = penetrationPower//10
    if penetrationPower > 6:
        penetrationPower = 6
    elif penetrationPower < 1:
        penetrationPower = 1
        #accuracyModifier
    accuracyModifier = ("+" if accuracyModifier > 0 else "")+str("%.0f" % (accuracyModifier*100))+"%"
        #recoilModifier
    recoilModifier = ("+" if recoilModifier > 0 else "")+str("%.0f" % (recoilModifier*100))+"%"
        #initialSpeed
    initialSpeed = str("%.0f" % initialSpeed)+" m/s"
        #lightBleedModifier
    lightBleedModifier = ("+" if lightBleedModifier > 0 else "")+str("%.0f" % (lightBleedModifier*100))+"%"
        #heavyBleedModifier
    heavyBleedModifier = ("+" if heavyBleedModifier > 0 else "")+str("%.0f" % (heavyBleedModifier*100))+"%"

    #Flea Market Price
    fleaPrice = 0
    flea = False
    if 'noFlea' in types:
        flea = False
    else:
        flea = True
    if flea:
        for vendor_data in sellFor:
            if vendor_data["vendor"]["name"] == 'Flea Market':
                fleaPrice = str(vendor_data["price"])
    else:
        fleaPrice = "You cannot sell this item on the Flea Market"

    #info formatting
    if flea:
        info = f"\n• Sell to the `Flea Market` for `{fleaPrice}₽`\n• Sell to `{vendor_name}` for `{max_sell}₽`"
    elif vendor_name == 'Peacekeeper':
        info = f"\n• Sell to `{vendor_name}` for `{max_sell}$`"
    else:
        info = f"\n• Sell to `{vendor_name}` for `{max_sell}₽`"
    
    if tracer:
        ammo_properties = f"\n• __**Damage**__: `{damage}`\n• __**Armor Damage**__: `{armorDamage}`\n• __**Armor Penetration**__: `Class {penetrationPower}`\n• __**Fragmentation %**__: `{fragmentationChance}`\n• __**Ricochet %**__: `{ricochetChance}`\n• __**Initial Speed**__: `{initialSpeed}`\n• __**Tracer Color**__: `{tracerColor}`"
    else:
        ammo_properties = f"\n• __**Damage**__: `{damage}`\n• __**Armor Damage**__: `{armorDamage}`\n• __**Armor Penetration**__: `Class {penetrationPower}`\n• __**Fragmentation %**__: `{fragmentationChance}`\n• __**Ricochet %**__: `{ricochetChance}`\n• __**Initial Speed**__: `{initialSpeed}`"
    
    modifiers = f"```\n• Accuracy: {accuracyModifier}\n• Recoil: {recoilModifier}\n• Light Bleed: {lightBleedModifier}\n• Heavy Bleed: {heavyBleedModifier}```"

    #embed creation
    embed = Embed(title=name, url=wikiLink, color=0x2b2d31)
    embed.add_field(name="`Informations📋:`", value=info, inline= False)
    embed.add_field(name="`Ammo Properties🪖:`", value=ammo_properties, inline= True)
    embed.add_field(name="ㅤㅤ", value="ㅤ", inline= True)
    embed.add_field(name="`Modifiers📈:`", value=modifiers, inline= True)
    embed.set_thumbnail(iconLink)
    embed.set_footer(text = updated)
    await interaction.followup.send(embed=embed)

async def ammo_autocomplete(interaction:Interaction, name: str):
    try:
        await interaction.response.defer()
        get_near_ammo = [ammoo for ammoo in all_ammo_list if ammoo.lower().startswith(name.lower()) or (name.lower() in ammoo.lower())][0:25]
        await interaction.response.send_autocomplete(get_near_ammo)
    except Exception as e:
        print("[-] ammo_autocomplete(functions.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)

async def item(interaction:Interaction, name: str):
    #if the ammo doesnt exist returns error message to the user
    if name not in items_list:
        await interaction.response.defer(ephemeral=True)
        error = "{0} not found. Make sure to spell the name correctly and if the issue persists use `/bug` to report the issue. Thank you.".format(name)
        embed = Embed(title='**Error: Item Not Found**', color=0x2b2d31)
        embed.add_field(name="", value=error, inline= False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        print("Error in item(functions.py) caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)
        return
    
    await interaction.response.defer()
    #searching name in the item database
    iteminfo = internal.getdb_item(name)
    #info tuple indexing
    name = iteminfo[0]
    if iteminfo[1] != 'None':
        avg24hPrice = int(iteminfo[1])
    else:
        avg24hPrice = 0 #int
    updated = iteminfo[2]
    types = iteminfo[3] #list
    if iteminfo[4] != 'None':
        lastLowPrice = int(iteminfo[4])
    else:
        lastLowPrice = 0
    if iteminfo[5] != 'None':
        changeLast48hPercent = iteminfo[5]
    else:
        changeLast48hPercent = 0
    iconLink = iteminfo[6]
    wikiLink = iteminfo[7]
    width = int(iteminfo[8]) #int
    height = int(iteminfo[9]) #int
    receivedFromTasks = iteminfo[10] #list
    usedInTasks = iteminfo[11] #list
    sellFor = iteminfo[12] #list

    #converting variables from string back to original type
        #types
    types = eval(types)
        #sellFor
    sellFor = eval(sellFor)
        #receivedFromTasks
    receivedFromTasks = eval(receivedFromTasks)
        #usedInTasks
    usedInTasks = eval(usedInTasks)
    #preparing variables for the embed
        #updated
    updated = strftime("%d/%m/%y %H:%M:%S", strptime(updated, "%Y-%m-%dT%H:%M:%S.%fZ"))
    actual_date = datetime.now().strftime("%d/%m/%y %H:%M:%S")
    d1 = datetime.strptime(updated, "%d/%m/%y %H:%M:%S")
    d2 = datetime.strptime(actual_date, "%d/%m/%y %H:%M:%S")
    delta = d2 - d1
    hours = (delta.seconds)//3600
    minutes = (delta.seconds)//60
    if minutes > 60:
        if hours > 1:
            updated = f'⌛Last updated: {hours} hours and {minutes-(hours*60)} minutes ago'
        else:
            updated = f'⌛Last updated: 1 hour and {minutes-(hours*60)} minutes ago'
    else:
        if minutes > 1:
            updated = f'⌛Last updated: {minutes} minutes ago'
        else:
            updated = f'⌛Last updated: 1 minute ago'
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
    else:
        fleaPrice = "You cannot sell this item on the Flea Market"
        #item size
    total_slots = width*height
        #price per slot
    if flea:
        priceXslot = fleaPrice//total_slots
    else:
        priceXslot = max_sell//total_slots
        #changeLast48hPercent
    if changeLast48hPercent == 'None':
        _48hChange = False
    elif float(changeLast48hPercent) != 0:
        _48hChange = True
    else:
        _48hChange = False
    changeLast48hPercent = str(changeLast48hPercent)+"%"
        #usedInTasks
    usedInTaskss = ""
    #usedinTask returns the string with the missions name & wikiLink formatted in the way discord wants to create links
    counter = 1
    for task in usedInTasks[0:6]:
        taskName = task["name"]
        taskLink = task["wikiLink"]
        if counter < len(usedInTasks) and len(usedInTasks) != 1:
            usedInTaskss += f"\n• [{taskName}]({taskLink})"
        elif len(usedInTasks) == 1:
            usedInTaskss += f"• [{taskName}]({taskLink})"
        counter += 1
    if len(usedInTasks) == 0:
        usedInTaskss = "None"
        #recivedFromTasks
    receivedFromTaskss = ""
    counter1 = 1
    for task in receivedFromTasks[0:6]:
        taskName1 = task["name"]
        taskLink1 = task["wikiLink"]
        if counter1 < len(receivedFromTasks) and len(receivedFromTasks) != 1:
            receivedFromTaskss += f"\n• [{taskName1}]({taskLink1})"
        elif len(receivedFromTasks) == 1:
            receivedFromTaskss += f"• [{taskName1}]({taskLink1})"
        counter1 += 1
    if len(receivedFromTasks) == 0:
        receivedFromTaskss = "None"
    if avg24hPrice != 0:
        _24hPrice = True
    else:
        _24hPrice = False
    #itemtier
    if not flea:
        tier = "❌ No Flea ❌"
        embed_color = 0x2f3136
    else:
        if int(fleaPrice) < 10000:
            tier = "🔴 Poor"
            embed_color = 0xf8312f
        elif int(fleaPrice) >= 10000 and int(fleaPrice) < 50000:
            tier = "🟢 Average"
            embed_color = 0x00d26a
        elif int(fleaPrice) >= 50000 and int(fleaPrice) < 100000:
            tier = "🔵 Great"
            embed_color = 0x0074ba
        elif int(fleaPrice) >= 100000 and int(fleaPrice) < 250000:
            tier = "🟠 Rare"
            embed_color = 0xff6723
        elif int(fleaPrice) >= 250000 and int(fleaPrice) < 500000:
            tier = "🟣 Very Rare"
            embed_color = 0x8d65c5
        elif int(fleaPrice) >= 500000 and int(fleaPrice) < 2500000:
            tier = "🟡 Legendary"
            embed_color = 0xfcd53f
        elif int(fleaPrice) >= 2500000:
            tier = "⚪ Mythical"
            embed_color = 0xffffff
    if flea:
        fleaPrice = "{:,}".format(fleaPrice)
        avg24hPrice = ("{:,}".format(int(avg24hPrice)))+"₽"
    priceXslot = "{:,}".format(int(priceXslot))
    max_sell = "{:,}".format(max_sell)
    #info formatting
    if flea:
        info = f"\nItem Tier: `{tier}`\n\n• Sell to the `Flea Market` for `{fleaPrice}₽`\n• Sell to `{vendor_name}` for `{max_sell}₽`"
    elif flea and vendor_name == 'Peacekeeper':
        info = f"\nItem Tier: `{tier}`\n\n• Sell to the `Flea Market` for `{fleaPrice}₽`\n• Sell to `{vendor_name}` for `{max_sell}$`"
    elif vendor_name == 'Peacekeeper':
        info = f"\nItem Tier: `{tier}`\n\n• Sell to `{vendor_name}` for `{max_sell}$`"
    elif (name == "Roubles") or (name == "Euros") or (name == "Dollars") or (len(sellFor) == 0):
        info = f"\nItem Tier: `{tier}`\n\n"
    else:
        info = f"\nItem Tier: `{tier}`\n\n• Sell to `{vendor_name}` for `{max_sell}₽`"
    
    #embed creation
    embed = Embed(title=name, url=wikiLink, color=embed_color)
    embed.add_field(name="`Informations📋:`", value=info, inline= False)
    if flea and _24hPrice:
        embed.add_field(name="`Average Price💸:`", value=avg24hPrice, inline= True)
    if flea and _48hChange:
        embed.add_field(name="`48h Price Change📈:`", value=changeLast48hPercent, inline= True)
    if total_slots > 1:
        embed.add_field(name="`Price per Slot📊:`", value=priceXslot+f"₽ ({total_slots} Slots)", inline= True)
    
    embed.add_field(name="`Needed for Tasks🧭:`", value=usedInTaskss, inline= False)
    embed.add_field(name="`Recived From Tasks🧭:`", value=receivedFromTaskss, inline= False)
    embed.set_thumbnail(iconLink)
    embed.set_footer(text = updated)
    
    await interaction.followup.send(embed=embed)

async def item_autocomplete(interaction:Interaction, name: str):
    try:    
        await interaction.response.defer()
        get_near_item = [itemm for itemm in items_list if itemm.lower().startswith(name.lower()) or (name.lower() in itemm.lower())][0:25]
        await interaction.response.send_autocomplete(get_near_item)
    except Exception as e:
        print("[-] item_autocomplete(functions.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)

async def auto(interaction:Interaction, image:Attachment):
    #checking if image url is not broken
    if len(image.url) == 0:
        await interaction.response.defer(ephemeral=True)
        error = "There was an error while getting the image url. If this keeps happening please report it using `/bug`. Thank you."
        embed = Embed(title='**Error: Invalid Image URL**', color=0x2b2d31)
        embed.add_field(name="", value=error, inline= False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        print("Error in auto(functions.py) caused by:", interaction.user.name,"User ID:",interaction.user.id," with input image:",image.url)
        return
    
    await interaction.response.defer()
    imagePIL = None
    async with ClientSession() as session:
        async with session.get(image.url) as response:
            if response.status == 200:
                image_data = await response.read()
                imagePIL = Image.open(BytesIO(image_data))
    
    if imagePIL is None:
        await interaction.response.defer(ephemeral=True)
        error = "There was an error while opening the image. If this keeps happening please report it using `/bug`. Thank you."
        embed = Embed(title='**Error: Invalid Image**', color=0x2b2d31)
        embed.add_field(name="", value=error, inline= False)
        await interaction.followup.send(embed=embed, ephemeral=True)
        print("Error in auto(functions.py) caused by:", interaction.user.name,"User ID:",interaction.user.id," with input image:",image.url)
        return
    
    binary_image = internal.adjust_auto_image(imagePIL)
    items_to_search = internal.auto_ocr(binary_image)

    total_value = 0
    items = {}
    for itm in items_to_search:
        result = internal.getdb_shortName(itm)
        name, vendor_name, max_sell, flea, fleaPrice, changeLast48hPercent = internal.auto_organize(result)
        shortName = itm
        items[name] = [vendor_name, max_sell, flea, fleaPrice, changeLast48hPercent, shortName]
    for itm in items:
        total_value += (max(items[itm][1], items[itm][3])) * items_to_search[items[itm][5]]
    embed = Embed(title=f"`Total Value: {total_value}₽`", color=0x2f3136)
    for itm in items:
        embed.add_field(name=f"`Name📋:`  {itm} **(x{items_to_search[items[itm][5]]})**", value = f"", inline= False)
        #if flea and fleaprice > max_price
        if items[itm][2] and items[itm][3] > items[itm][1]:
            embed.add_field(name="`Best Vendor🪪:`", value = f"**Flea Market**", inline= True)
            embed.add_field(name="`Price💸:`", value = f"**{items[itm][3]}₽**", inline= True)
            embed.add_field(name="`48h Price Change📈:`", value=f"**{items[itm][4]}%**", inline= True)
        elif items[itm][2] and items[itm][3] < items[itm][1]:
            embed.add_field(name="`Best Vendor:`", value = f"**{items[itm][0]}**", inline= True)
            if items[itm][0] == "Peacekeeper":
                embed.add_field(name="`Price💸:`", value = f"**{items[itm][3]}$**", inline= True)
            else:
                embed.add_field(name="`Price💸:`", value = f"**{items[itm][3]}₽**", inline= True)
            embed.add_field(name="`48h Price Change📈:`", value=f"**{items[itm][4]}%**", inline= True)
        else:
            embed.add_field(name="`Best Vendor:`", value = f"**{items[itm][0]}**", inline= True)
            if items[itm][0] == "Peacekeeper":
                embed.add_field(name="`Price💸:`", value = f"**{items[itm][3]}$**", inline= True)
            else:
                embed.add_field(name="`Price💸:`", value = f"**{items[itm][3]}₽**", inline= True)

    await interaction.followup.send(embed=embed)