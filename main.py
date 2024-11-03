#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#imports
from nextcord import Intents, Interaction, Attachment, Embed, TextInputStyle, ShardInfo, Activity, ActivityType, Status
from nextcord.ext import commands
from nextcord.ui import Modal, TextInput
from nextcord.errors import HTTPException, LoginFailure
from os import getenv, system
from dotenv import load_dotenv
from time import sleep
from datetime import datetime
import asyncio
#modules
import modules.functions as functions
import modules.informative as informative
import modules.internal as internal


#------------------------------- SETUP ---------------------------------------------------

shards_count = 5

#loading api key from .env
load_dotenv()
TOKEN = getenv("API_TOKEN")
#prefix
intents = Intents.default()
#intents.message_content = True
bot = commands.AutoShardedBot(shard_count=shards_count, intents=intents)
bot.remove_command('help')


#-------------------------------- CLIENT ------------------------------------------------
@bot.event
async def on_ready():
    internal.tclear()
    print(f'Logged in as: {bot.user.name}(#{bot.user.discriminator})')
    print(f'Servers Joined: {len(bot.guilds)}')
    total_members = 0
    for g in bot.guilds:
        if g.member_count:
            total_members += int(g.member_count)
    print(f'Total Users: {total_members}')
    try:
        await bot.sync_all_application_commands()
    except Exception as e:
        print("Error while syncing application commands:",e)
    print("----------------------------- LOGS ---------------------------------")
    
    #update database every 5 minutes
    bot.loop.create_task(internal.updatedb("db_update.py"))

@bot.event
async def on_connect():
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{} connected".format(bot.user.name))

@bot.event
async def on_disconnect():
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{} disconnected".format(bot.user.name))
    all_shards_offline = True
    for shard_id, shard_info in bot.shards.items():
            if shard_info.is_closed() != False:
                all_shards_offline = False
                break
    if all_shards_offline:
        print(dt_string + "All shards are offline. Restarting the bot...")
        await bot.close()
        await asyncio.sleep(10)
        await bot.start(TOKEN, reconnect=True)
        print(dt_string + "Restarted. Sleeping for 10 minute...")
        await asyncio.sleep(600)
        

@bot.event
async def on_resumed():
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{} resumed".format(bot.user.name))

#------------------------- SHARDS ---------------------------------------------------------

@bot.event
async def on_shard_ready(shard_id):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} Shard[{1}] ready".format(bot.user.name, shard_id))

@bot.event
async def on_shard_connect(shard_id):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} Shard[{1}] connected".format(bot.user.name, shard_id))

@bot.event
async def on_shard_disconnect(shard_id):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} Shard[{1}] disconnected".format(bot.user.name, shard_id))
    try:
        print(dt_string + "{0} Shard[{1}] reconnecting".format(bot.user.name, shard_id))
        shard = bot.get_shard(shard_id)
        if shard.is_closed() and not shard.is_ws_ratelimited():
            print(dt_string + f"Shard[{shard_id}] connection is closed but not rate limited. Trying to connect()")
            await shard.reconnect()
            now2 = datetime.now()
            dt_string2 = now2.strftime("[%d/%m - %H:%M:%S] ")
            print(dt_string2 + "Reconnected. Sleeping for 10 minutes...")
            await asyncio.sleep(600)
        elif not shard.is_ws_ratelimited():
            print(dt_string + f"Shard[{shard_id}] connection is not closed nor rate limited. Trying to reconnect()")
            await shard.disconnect()
            await shard.reconnect()
            now2 = datetime.now()
            dt_string2 = now2.strftime("[%d/%m - %H:%M:%S] ")
            print(dt_string2 + "Reconnected. Sleeping for 10 minutes...")
            await asyncio.sleep(600)
    except Exception as e:
        print(dt_string + f"Error while reconnecting Shard[{shard_id}]:",e)
    #finally:
    #    await asyncio.sleep(600)

@bot.event
async def on_shard_resumed(shard_id):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} Shard[{1}] resumed".format(bot.user.name, shard_id))

#--------------------------------- OTHER ----------------------------------------------------------

@bot.event
async def on_http_ratelimit(limit, remaining, reset_after, bucket, scope):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} RATE LIMITED. Retry in {1}".format(bot.user.name, reset_after))

@bot.event
async def on_global_http_ratelimit(retry_after):
    now = datetime.now()
    dt_string = now.strftime("[%d/%m - %H:%M:%S] ")
    print(dt_string + "{0} GLOBAL RATE LIMITED. Retry in {1}".format(bot.user.name, retry_after))

#---------------------------------- FUNCTIONS ------------------------------------------------------------------
@bot.slash_command(name="ammo", description="Get round info such as damage, speed, weight, modifiers etc...")
async def ammo(interaction:Interaction, name: str):
    try:
        await functions.ammo(interaction, name)
    except Exception as e:
        print("[-] ammo(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)
@ammo.on_autocomplete("name")
async def ammo_autocomplete(interaction:Interaction, name: str):
    try:
        await functions.ammo_autocomplete(interaction, name)
    except Exception as e:
        print("[-] ammo_autocomplete(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)

@bot.slash_command(name="item", description="Get item informations such as tier,price,etc...")
async def item(interaction:Interaction, name: str):
    try:
        await functions.item(interaction, name)
    except Exception as e:
        print("[-] item(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)
@item.on_autocomplete("name")
async def item_autocomplete(interaction:Interaction, name: str):
    try:
        await functions.item_autocomplete(interaction, name)
    except Exception as e:
        print("[-] item_autocomplete(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)

@bot.slash_command(name="auto", description="Automatically scans items from an image and returns their price.")
async def auto(interaction:Interaction, image:Attachment):
    try:
        await functions.auto(interaction, image)
    except Exception as e:
        print("[-] auto(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input image:",image.url)

#informative
@bot.slash_command(name="boss", description="Get boss and guards information.")
async def boss(interaction:Interaction, name: str):
    try:
        await informative.boss(interaction, name)
    except Exception as e:
        print("[-] boss(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)
@boss.on_autocomplete("name")
async def boss_autocomplete(interaction:Interaction, name: str):
    try:
        await informative.boss_autocomplete(interaction, name)
    except Exception as e:
        print("[-] boss_autocomplete(main.py) error:",e)
        print("Caused by:", interaction.user.name,"User ID:",interaction.user.id," with input:",name)

@bot.slash_command(name="help", description="Get all the commands description.")
async def help(interaction:Interaction):
   await informative.help(interaction)

@bot.slash_command(name="tiers", description="Informations on the tiers system.")
async def tiers(interaction:Interaction):
    await informative.tiers(interaction)

@bot.slash_command(name="patchnotes", description="Get the latest patchnotes.")
async def patchnotes(interaction:Interaction):
    await informative.patchnotes(interaction)

@bot.slash_command(name="serverstatus", description="Check if the servers are having some issues.")
async def serverstatus(interaction:Interaction):
    await informative.serverstatus(interaction)

@bot.slash_command(name="bug", description="Report a bug.") #if not showing add guild_ids = [1059571834451931188]
async def bug(interaction:Interaction):
    await interaction.response.send_modal(BugModal())

#Bug Report Class
class BugModal (Modal):
    def __init__(self):
        super().__init__(
            "Report a Bug",
        )
        self.emTitle = TextInput(label = "Title", min_length = 2, max_length = 124, required = True, placeholder = "Enter the title here.")
        self.add_item(self.emTitle)

        self.emDesc = TextInput(label = "Description", min_length = 5, max_length = 4000, required = True, placeholder = "Explain what is the bug and how we can replicate it.", style = TextInputStyle.paragraph)
        self.add_item(self.emDesc)
    
    async def callback(self, interaction:Interaction) -> None:
        title  = self.emTitle.value
        desc = self.emDesc.value
        username = f"{interaction.user.name}#{interaction.user.discriminator}"
        embed = Embed(title = title, description = desc)
        embed.set_footer(text = "Reported by: "+username)
        admin_user = await bot.fetch_user(483759864527454238)
        await admin_user.send(embed = embed)
        
        embed1 = Embed(title = "Bug report successful!🪳", description = "Thanks you! This bug will be verified and if it comes out as real you will get the Bug Hunter role in the official server!")
        await interaction.response.send_message(embed=embed1, ephemeral=True)

def runBot():
    try:
        internal.tclear()
        bot.run(TOKEN)
    except LoginFailure:
        print("[-] Invalid token provided, check that you have inserted a valid token in the .env.")
        sys.exit(0)
    except HTTPException as e:
        retry_after = e.response.headers.get('Retry-After')
        if retry_after:
            print(f"ERROR: 429 - BLOCKED BY RATE LIMITS - Retry in {retry_after/60} minutes")
            sleep(retry_after)
        else:
            retry_after = 300
            print(f"ERROR: 429 - BLOCKED BY RATE LIMITS - Retry in {retry_after/60} minutes")
            sleep(retry_after)
    finally:
        exit()

if __name__ == '__main__':
    runBot()