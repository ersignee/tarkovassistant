#preventing creation of the __pycache__ folder (HAS TO BE BEFORE THE MODULES IMPORT)
import sys
sys.dont_write_bytecode = True
#imports
from nextcord import Interaction, Embed
#modules
import modules.internal as internal

#help command
async def help(interaction:Interaction):
    await interaction.response.defer()
    embed = Embed(title="Commands List", color=0x2f3136)
    embed.add_field(name="`/ammo [name]`", value="Get ammo details such as damage,armor penetration,weight, etc...", inline= False)
    embed.add_field(name="`/item [name]`", value="Returns item informations such as tier,price,etc...", inline= False)
    embed.add_field(name="`/boss [name]`", value="Obtain boss and guards information.", inline= False)
    embed.add_field(name="`/tiers`", value="Informations on the tiers system.", inline= False)
    embed.add_field(name="`/patchnotes`", value="Get the latest patchnotes.", inline= False)
    embed.add_field(name="`/serverstatus`", value="Check if the servers are having some issues.", inline= False)
    embed.add_field(name="`/bug`", value="Report a bug directly to the developer.", inline= False)
    #embed.add_field(name="`/clear`", value="Clear all channel messages in one click. (ADMIN ONLY)", inline= False)
    await interaction.followup.send(embed=embed)

#patchnotes
async def patchnotes(interaction:Interaction):
    await interaction.response.defer()
    embed = Embed(title="Patch 0.15.2.0", url="https://www.escapefromtarkov.com/news/id/315?lang=en", color=0x2f3136)
    
    patchnotes = "Check out the newest patchnotes [here](https://www.escapefromtarkov.com/news/id/315?lang=en)."
    
    embed.add_field(name = "", value=patchnotes, inline= False)
    embed.set_footer(text = "⌛Last updated: 26/09/2024")
    await interaction.followup.send(embed=embed)

#bosses
boss_list = ['Cultist Priest','Glukhar','Kaban','Killa','Knight','Kollontay','Partisan','Reshala','Sanitar',
             'Shturman','Tagilla','Zryachiy','Big Pipe','Birdeye','Santa Claus']

async def boss(interaction:Interaction, name: str):
    await interaction.response.defer()
    if name == 'Cultist Priest':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/8/84/CultistCloseup.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Cultists"
        info = "Cultists lurk in the shadows in **`groups of 3-5`**, \
        waiting for a player to approach. They silently approach their enemies \
        and stab them using either normal knives or, in case of the priests, \
        the poisoned Cultist knife. **`If fired upon, the Cultists will return fire using firearms and grenades.`** \
        After they attack a player with their knife, they may choose to run off into the woods again \
        and return to the shadows. As the Cultists prefer to ambush players and are extremely well hidden, \
        they almost always have the initiative, so it is important for players to quickly determine \
        exactly where the Cultists are and attempt to regain the initiative. Cultists appear to always \
        have suppressors and stick to cover, so players must be able to quickly spot them in the trees, \
        especially at night. Additionally, **`Cultists have been seen to stalk players`** and open \
        fire on them unprovoked, **`even if they go away from the Marked Circles.`**"
        tips = "Players should be extremely cautious as the Cultists use **`ammo with high-penetrative power`**, \
        yet rarely spawn with grenades. Cultists may spawn with a variety of armor, ranging from no protection to class 6 armor, however, \
        **`they rarely, if at all, use headgear`**, so headshots are certainly a viable option. If stabbed by the Cultist knife, \
        players will be inflicted by the **`Unknown toxin debuff`**, \
        which deals **`gradual damage over time and causes pain`**. The toxin can be cured by the \
        [xTG-12 antidote injector](https://escapefromtarkov.fandom.com/wiki/XTG-12_antidote_injector) or \
        [Augmentin antibiotic pills](https://escapefromtarkov.fandom.com/wiki/Augmentin_antibiotic_pills) otherwise, the player must extract \
        from the raid or they will run out of medication and die."
        loot = '[Cultist knife](https://escapefromtarkov.fandom.com/wiki/Cultist_knife)'
        maps = "Customs\nNight Factory\nShoreline\nWoods"
        health = "850"
        guards = "2-4"
    elif name == 'Glukhar':
        iconUrl = "https://assets.tarkov.dev/glukhar.jpg"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Glukhar"
        info = "Glukhar and his many guards are **`extremely hostile and very accurate`**. It's very unlikely to find success \
        while fighting in any open areas. They will stay near each other at all times and his guards will follow him to wherever \
        he goes. Glukhar has **`5-6 followers with a wide assortment of weapons and gear`**. The Guards have a wide variety of weapons, \
        usually **`Assault rifles`** usually loaded with tracer ammunition, **`Shotguns`**, an occasional \
        Designated **`marksman rifle`**, and **`Submachine guns`**. They typically have **`high-grade Armor vests and helmets`** \
        that sometimes have visors. He will not seek out player Scavs, however will engage low karma level player Scavs who come close to him, \
        keep in mind, guards exist to protect Glukhar so if he is far away or dead you can get as close as you want to guards. \
        **`If you are of a high scav karma level you are free to get as close as you want to him and his guards.`**"
        tips = "Avoid open areas and **`prefer small hallways and closed rooms`**. Avoid aiming for the chest because he can \
        withstand high damage bullets. **`The only effective means of killing Glukhar quickly are headshots.`**"
        loot = '[ASh-12 12.7x55 assault rifle](https://escapefromtarkov.fandom.com/wiki/ASh-12_12.7x55_assault_rifle)'
        maps = "Reserve"
        health = "1010"
        guards = "6"
    elif name == 'Kaban':
        iconUrl = 'https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/e/e3/Kaban_Portrait.png'
        wikiLink = 'https://escapefromtarkov.fandom.com/wiki/Kaban'
        info = "Kaban and his guards defend themselves with an **`extensive array of snipers and emplaced weapons`**, and patrol the area within LexOs. The **`Snipers`** will patrol the **`rooftops of the LexOs dealership and LexOs mechanic area`** and cooperate with each other. The **`Guards`** within LexOs will patrol the **`compound between the dealership and mechanic area`**. **`At each entrance`**, there is an **`AGS-30`** in the watchtowers and an **`NSV`** watching the dangerous chokepoints and entrances of the compound that will often be manned, and a Guard will always man the NSV closest to where PMCs are assaulting from. **`Kaban`** himself **`will stay within the dealership or mechanics building`**. **`If engaged`** by players, **`he will employ accurate, rapid bursts with his primary weapon and may reposition within his building, upstairs, or into the compound.`**"
        tips = "It is recommended to **`approach from the area around Chek 15 in the north`**. **`Avoid the grass and curb leading up to the entrance`**, as proximity-armed claymores will detonate without warning. **`Grenades and Flashbangs can be used to displace Guards on the internal NSVs or in the middle of the compound`**, allowing for an easy kill. It is best to **`bait Kaban's attention from one angle, then simultaneously engage him from another`**. Also, if he's using his PKP, it's recommended to wait out his machinegun bursts, then begin pushing him during his long, and loud, reload process."
        loot = "• [Kalashnikov PKM 7.62x54R machine gun](https://escapefromtarkov.fandom.com/wiki/Kalashnikov_PKM_7.62x54R_machine_gun)\n• [Kalashnikov PKP 7.62x54R infantry machine gun](https://escapefromtarkov.fandom.com/wiki/Kalashnikov_PKP_7.62x54R_infantry_machine_gun)\n• [RPK-16 5.45x39 light machine gun](https://escapefromtarkov.fandom.com/wiki/RPK-16_5.45x39_light_machine_gun)"
        maps = "Streets of Tarkov"
        health = "1300"
        guards = "6 and 2-3 Snipers"
    elif name == 'Killa':
        iconUrl = "https://assets.tarkov.dev/killa.jpg"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Killa"
        info = "**'Killa wears his **`armor class 5 6B13M with a Maska-1SCh bulletproof helmet & faceshield and uses a light machine gun or other automatic weapon to suppress the enemy`**, \
        while lurking from cover to cover'**, getting closer to his target for the final push. During the assault he moves in a \
        zig-zag pattern, **`uses smoke and fragmentation grenades, and relentlessly suppresses enemies with automatic fire`**. \
        **'He will follow his target large distances out of his patrol route'**, so be sure to run very far to get away from him \
        if he has locked onto you. "
        tips = "It is recommended to **`avoid being spotted by Killa`**. He has multiple grenades and is generally accurate with his bursts.\
        It is best to **`attack him with high-penetration ammunition`** such as [5.45x39mm BS gs](https://escapefromtarkov.fandom.com/wiki/5.45x39mm_BS_gs), \
        [5.56x45mm M995](https://escapefromtarkov.fandom.com/wiki/5.56x45mm_M995), or [7.62x51mm](https://escapefromtarkov.fandom.com/wiki/7.62x51mm_NATO). \
        **`Grenades generally won't work`** to kill him, as he is a highly mobile fighter and will rarely be pinned down long enough for a grenade to stop him. \
        If fighting him with a teammate, **`attacking him from two different directions and peeking cover is a sound strategy`**, as he will continue to suppress \
        one of his opponents while the other can safely return fire."
        loot = '• [RPK-16 5.45x39 light machine gun](https://escapefromtarkov.fandom.com/wiki/RPK-16_5.45x39_light_machine_gun)\n• [Maska-1SCh bulletproof helmet & faceshield (Killa)](https://escapefromtarkov.fandom.com/wiki/Maska-1SCh_bulletproof_helmet_(Killa))\n• [6B13 M modified assault armor (Tan)](https://escapefromtarkov.fandom.com/wiki/6B13_M_modified_assault_armor_(Tan))\n• [BlackHawk! Commando chest harness (Black)](https://escapefromtarkov.fandom.com/wiki/BlackHawk!_Commando_chest_harness_(Black))'
        maps = "Interchange"
        health = "890"
        guards = "None"
    elif name == 'Knight':
        iconUrl = "https://assets.tarkov.dev/death-knight.jpg"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Knight"
        info = 'He is the **`commander of the Rogue squad "The Goons"`**, The other members are \
        [Big Pipe](https://escapefromtarkov.fandom.com/wiki/Big_Pipe) and \
        [Birdeye](https://escapefromtarkov.fandom.com/wiki/Birdeye). When a player is spotted by any one of the Goons, \
        **`Big Pipe and Knight both rush the player`**. **`Birdeye will stay behind and wait till the action is over to show himself`**, \
        so in order to get Birdeye to show himself you either can wait for him to push you after you kill Knight and Big Pipe, \
        or you could throw grenades in his direction in order to pinpoint his location.'
        tips = "The best way to deal with the Goons on Customs is to **`gain their attention`**. After that \
        your best choice to kill them would be to **`sit in a room and close the door, as this will create a small time period of them opening the door allowing you to shoot them with no repercussions.`**"
        loot = '• [Death Knight mask](https://escapefromtarkov.fandom.com/wiki/Death_Knight_mask)\n• [Crye Precision CPC plate carrier (Goons Edition)](https://escapefromtarkov.fandom.com/wiki/Crye_Precision_CPC_plate_carrier_(Goons_Edition))'
        maps = "Customs\nLighthouse\nShoreline\nWoods"
        health = "1120"
        guards = "[BigPipe](https://escapefromtarkov.fandom.com/wiki/Big_Pipe), [Birdeye](https://escapefromtarkov.fandom.com/wiki/Birdeye)"
    elif name == 'Kollontay':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/d/d3/Kollontay_Portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Kollontay"
        info = "Kollontay is always protected by **`4 heavily armed and armored guards`** and usually prefers to remain indoors \
        **`holding the hallways on the ground floor while his guards will push towards the player with fast and aggressive movement`**. He roams\
        both sides of the academy, keeping his eye out of the various windows for any unsuspecting PMCs that happen to walk past."
        tips = "Attempting to **`push him from the main door while holding an angle to shoot at his guards behind cover`** is advisable. \
        He has a tendency to hold the far corners of the building, and hide behind the bars in the cells to the left of the entrance, \
        **`don't get too close as he will try and rush you with his baton`** and force-jam your weapon with the [Panic Attack](https://escapefromtarkov.fandom.com/wiki/Health_system#Temporary_status_effects) effect."
        loot = '[PR-Taran police baton](https://escapefromtarkov.fandom.com/wiki/PR-Taran_police_baton)'
        maps = "Streets of Tarkov\nGround Zero(lvl 21+)"
        health = "1055"
        guards = "4"
    elif name == 'Partisan':
        iconUrl = "https://tarkov.dev/images/bosses/partisan-portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Partisan"
        info = "**`Partisan prefers a stealthy approach, taking advantage of the terrain, setting traps in advance, and only then engaging in open combat.`** \
        The process of preparing and exploring a location takes up most of his time, while open confrontations are less frequent. \
        **`When fighting against multiple opponents, he can lure one of the players to his booby-traps which he sets up beforehand.`** \
        He installs tripwires, actively uses grenades, can move quietly through the terrain and track his target for a long time \
        across the whole location. He is more likely to appear in a raid with low karma PMCs."
        tips = "Partisan sets up traps like tripwires in advance to control key positions on the map. Always check corners and entry points carefully\
        to avoid those. **`He moves quietly and avoids open combat until he has the upper hand. Use your ears. He won’t make a sound until it’s too late.`**\
        Also Partisan uses the map’s terrain to stay hidden, ambushing players when they least expect it. Keep an eye on high ground and tight spaces.\
        When fighting with him expect a lot of grenades. He uses them to flush out players and control space. Be ready to move quickly to avoid getting caught."
        loot = "[Partisan's bag](https://escapefromtarkov.fandom.com/wiki/Partisan%27s_bag)"
        maps = "Customs\nWoods\nShoreline\nLighthouse"
        health = "950"
        guards = "None"
    elif name == 'Reshala':
        iconUrl = "https://tarkov.dev/images/bosses/reshala-portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Reshala"
        info = "Reshala is always protected by **`4 heavily armed guards, with tier 2-6 armor vests and tier 3-5 helmets`**. \
        They are often seen in a tight group or formation with Reshala in the middle, \
        and once aggravated Reshala and 1-2 guards will run to cover whilst the rest of the guards will hold their position \
        and fight."
        tips = "To kill Reshala first, the best tactic is to **`find him before being seen`**. He can be easily identified by his \
        brown sweater, unlike his followers who wear blue jackets with white striped cuffs. Before looting it's recommended \
        that you kill all of them as they will usually stay within close proximity to each other and will probably kill you. \
        **`Since they are in close proximity to each other, grenades can be highly effective at stunning or killing multiple of them at once`**, \
        however they also have grenades and will troe them at you even if you are behind cover."
        loot = '[TT-33 7.62x25 TT pistol (Golden)](https://escapefromtarkov.fandom.com/wiki/TT-33_7.62x25_TT_pistol_(Golden))'
        maps = "Customs"
        health = "752"
        guards = "4"
    elif name == 'Sanitar':
        iconUrl = "https://tarkov.dev/images/bosses/sanitar-portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Sanitar"
        info = "When engaged in combat, he will fight alongside his **`2-3 heavily armed and armored guards`**, \
        but may often break away to heal or inject himself. **`He has plenty of meds`**, so a prolonged \
        engagement is possible. When Sanitar and his guards are roaming or in an idle state, \
        Sanitar can often be seen dropping medical items on the floor everywhere he goes. \
        The items he drops includes anything in his bag such as surgery kits or even Vodka. \
        The dropped items are presumably for friendly player or AI Scavs."
        tips = "**`When contact is made with Sanitar and his guards, the player should attempt to kill them without giving them the chance to break-off and heal.`** \
        While the standard scavs that surround Sanitar are not as dangerous as his guards, they may still pose a threat, \
        sneaking up on players and hitting them in vulnerable locations or distracting the players while \
        Sanitar or his guards flank you. Care should be taken to avoid rushing into a large group of scavs \
        in addition to Sanitar and his men. If Sanitar spawns in the **`cottages`**, they are likely to spawn in \
        the yards and use the **`bushes as concealment`**, but will still be able to detect and shoot players \
        through the bushes. **`In resort`**, Sanitar usually spawns on the **`ground floor`** of either the **`west or the east wing`**. \
        **`Watch out for them camping the hole in the wall entrance of the west wing.`**"
        loot = '• [Keycard with a blue marking](https://escapefromtarkov.fandom.com/wiki/Keycard_with_a_blue_marking)\n• [Sanitar bag](https://escapefromtarkov.fandom.com/wiki/Sanitar%27s_bag)'
        maps = "Shoreline"
        health = "1270"
        guards = "2"
    elif name == 'Shturman':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/3/3f/Shturman_Portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Shturman"
        info = "Shturman and his **`2 guards`** will engage the player at a **`long range`** protecting the sawmill area of the woods. \
        **`They prefer to keep their distance, as they are not suited for close quarters combat.`** \
        They also like to take positions between hard cover, or camouflage themselves with the environment. \
        Additionally, it is not unheard of for \
        **`one of the guards to flank or rush the player(s) while Shturman and the other guard hold positions and keep the player(s) pinned down`**. \
        It is also good to note that **`Shturman will fire warning shots (Usually 3-5) before locking onto his target`**, \
        these warning shots only occur **`if the target is far enough away where they pose no immediate threat to Shturman himself`**. \
        When both followers are killed Shturman tends to take shelter in places like wooden barracks."
        tips = "It is recommended that the player(s) **`take the initiative when engaging the Boss`**. \
        As the boss and his guards are often spread out, it is best to **`first recon the area and figure out where they are`**, \
        then **`eliminate one of them, preferably the boss, with a single, well-placed headshot with more than 62 flesh damage`**, \
        anything lower than 62 will take 2 headshots to kill. As neither the boss nor his guards wear helmets, \
        **`headshots are the best way to go`**, given that guards are often decently armored and the boss has high chest health. \
        Also, **`the guards do utilize grenades`**, so one should be as careful as possible when moving up."
        loot = '• [Shturman stash key](https://escapefromtarkov.fandom.com/wiki/Shturman%27s_stash_key)\n• [Red Rebel ice pick](https://escapefromtarkov.fandom.com/wiki/Red_Rebel_ice_pick)'
        maps = "Woods"
        health = "812"
        guards = "2"
    elif name == 'Tagilla':
        iconUrl = "https://tarkov.dev/images/bosses/tagilla-portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Tagilla"
        info = "He is batshit insane and **`will attempt to hammer you down`**. \
        **`However, if you are in a position that he cannot path-find to, such as the rafters, he will use his secondary weapon (usually a shotgun) to kill you from a distance.`** \
        He's active immediately at the start of raid. **`He has no guards, but can set ambushes, open suppressive fire, and breach if needed.`**"
        tips = "**`If you are using high penetrating ammunition, aim for his head, not his thorax.`** \
        **`If you have low pen or high flesh damage, aim for his stomach since his armor only covers the thorax.`** \
        The best plan of action is to **`bait out his swing so he's standing still, then shoot him`**. If you shoot while he's running at you, \
        he'll just charge through it and absolutely murder you, so wait until he swings to shoot. **`Tagillas welding masks does not protect his nape`**, \
        therefore you can try to shoot him there. This strategy requires sneaking up behind him without you being detected, or \
        a teammate that flanks him while he is fighting or chasing you."
        loot = '• [Superfors DB 2020 Dead Blow Hammer](https://escapefromtarkov.fandom.com/wiki/Superfors_DB_2020_Dead_Blow_Hammer)\n• [Tagilla welding mask "UBEY"/"Gorilla"](https://escapefromtarkov.fandom.com/wiki/Tagilla%27s_welding_mask_%22Gorilla%22)\n• [Crye Precision AVS MBAV (Tagilla Edition)](https://escapefromtarkov.fandom.com/wiki/Crye_Precision_AVS_MBAV_(Tagilla_Edition))'
        maps = "Factory\nNight Factory"
        health = "1220"
        guards = "None"
    elif name == 'Zryachiy':
        iconUrl = "https://tarkov.dev/images/bosses/zryachiy-portrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Zryachiy"
        info = "**`Zryachiy and his guards will shoot you upon hitting one of them or walking on the bridge.`** \
        They are **`extremely accurate and hard to spot, usually sitting on the rocks on the peninsula`**. \
        **`Zryachiy himself will be somewhat centered near the rock closest to the Lighthouse itself`**. \
        His followers are spread out, on opposite sides of the island. \
        One sits somewhat high on the peninsula, **`near the rocks next to the house with the small dome on it.`** \
        The other one will sit near or on the **`rock plateau on the right.`** \
        **`Zryachiy's guards will respawn up to 3 times`** in total together as long as Zryachiy is alive. \
        Zryachiy and his guards will only target the most recent player that has damaged any of them."
        tips = "The **`easiest strategy`** to killing Zryachiy and his guards **`requires atleast 3 people`**. \
        This strategy involves having **`one person kill Zryachiy then the other 2 killing both the guards`**. \
        If you do it the other way around the guards will both respawn several times. \
        An alternative method **`if you are by yourself`**, is to `**slow lean around right corners using a high magnification scope`**, \
        and **`trying to pick off the guards along with their respawns and then kill Zyrachiy`**. \
        It is currently possible for player scavs to spawn on the island once all AI are killed."
        loot = '• [Zryachiy balaclava folded/unfolded](https://escapefromtarkov.fandom.com/wiki/Zryachiy%27s_balaclava)\n• [Azimut SS "Khamelion" chest harness (Olive)](https://escapefromtarkov.fandom.com/wiki/Azimut_SS_%22Khamelion%22_chest_harness_(Olive))\n• [Accuracy International AXMC .338 LM bolt-action sniper rifle](https://escapefromtarkov.fandom.com/wiki/Accuracy_International_AXMC_.338_LM_bolt-action_sniper_rifle)'
        maps = "LightHouse"
        health = "1305"
        guards = "2"
    elif name == 'Big Pipe':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/e/ed/BigPipePortrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Big_Pipe"
        info = "When a player is spotted by any one of the Goons, **`Knight and Big Pipe both rush the player.`**"
        tips = "The best way to deal with the Goons on Customs is to **`gain their attention`**. After that \
        your best choice to kill them would be to **`sit in a room and close the door, as this will create a small time period of them opening the door allowing you to shoot them with no repercussions.`**"
        loot = "• [Milkor M32A1 MSGL 40mm grenade launcher](https://escapefromtarkov.fandom.com/wiki/Milkor_M32A1_MSGL_40mm_grenade_launcher)\n• [Big Pipe's smoking pipe](https://escapefromtarkov.fandom.com/wiki/Big_Pipe%27s_smoking_pipe)\n• [Big Pipe's bandana](https://escapefromtarkov.fandom.com/wiki/Big_Pipe%27s_bandana)\n• [S&S Precision PlateFrame plate carrier (Goons Edition)](https://escapefromtarkov.fandom.com/wiki/S%26S_Precision_PlateFrame_plate_carrier_(Goons_Edition))"
        maps = "Customs\nLighthouse\nShoreline\nWoods"
        health = "910"
        guards = "[Knight](https://escapefromtarkov.fandom.com/wiki/Knight), [Birdeye](https://escapefromtarkov.fandom.com/wiki/Birdeye)"
    elif name == 'Birdeye':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/2/27/BirdeyePortrait.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Birdeye"
        info = "Birdeye seems to **`sit back and let Knight and Big Pipe push the opposing enemy first`**. \
        **`If they`** do not succeed and **`die, he seems to rush the player`**. **`His steps are entirely silent.`**"
        tips = "The best way to deal with the Goons on Customs is to **`gain their attention`**. After that \
        your best choice to kill them would be to **`sit in a room and close the door, as this will create a small time period of them opening the door allowing you to shoot them with no repercussions.`**"
        loot = "• [Mystery Ranch NICE COMM 3 BVS frame system](https://escapefromtarkov.fandom.com/wiki/Mystery_Ranch_NICE_COMM_3_BVS_frame_system)\n• [LBT-1961A Load Bearing Chest Rig (Goons Edition)](https://escapefromtarkov.fandom.com/wiki/LBT-1961A_Load_Bearing_Chest_Rig_(Goons_Edition))"
        maps = "Customs\nLighthouse\nShoreline\nWoods"
        health = "795"
        guards = "[Knight](https://escapefromtarkov.fandom.com/wiki/Knight), [Big Pipe](https://escapefromtarkov.fandom.com/wiki/Big_Pipe)"
    elif name == 'Santa Claus':
        iconUrl = "https://static.wikia.nocookie.net/escapefromtarkov_gamepedia/images/5/58/Santa_Claus.png"
        wikiLink = "https://escapefromtarkov.fandom.com/wiki/Santa_Claus"
        info = 'He wanders each map and if he encounters a player, **`will not be hostile (Unless fired upon)`**. \
        If you approach him, **`he will drop a random item`**, gesturing and looking at it until taken.'
        tips = "**`Don't kill him, or else you will lose significant Scav karma (-1)`**, \
        also **`his backpack does not contain the loot he can trade with players`**, \
        only one christmas tree ornament and other loose items. His chest rig can also contain an ornament."
        loot = "[Santa's Bag](https://escapefromtarkov.fandom.com/wiki/Santa%27s_Bag)"
        maps = 'All (Special Events Only)'
        health = '1040'
        guards = "None"
    
    embed = Embed(title=name, url=wikiLink, color=0x202225)
    embed.add_field(name="`Informations📋:`", value=info, inline= False)
    embed.add_field(name="`Tips💡:`", value=tips, inline= False)
    embed.add_field(name="`Loot💰:`", value=loot, inline= False)
    embed.add_field(name="`Maps🗺️ & Spawn Rate🎲:`", value=maps, inline= True)
    embed.add_field(name="`Health❤️:`", value=health, inline= True)
    embed.add_field(name="`Guards🥷🏼:`", value=str(guards), inline= True)
    embed.set_thumbnail(iconUrl)
    
    await interaction.followup.send(embed=embed)

async def boss_autocomplete(interaction:Interaction, name: str):
    try:
        await interaction.response.defer()
        get_near_boss = [bosss for bosss in boss_list if bosss.lower().startswith(name.lower()) or (name.lower() in bosss.lower())][0:25]
        await interaction.response.send_autocomplete(get_near_boss)
    except Exception as e:
        print("[-] boss_autocomplete error:",e)
        print("Caused by:", interaction.user.name)

#tiers
async def tiers(interaction:Interaction):
    await interaction.response.defer()
    embed = Embed(title="Tier List", url="https://tarkov.dev/loot-tier/", color=0x2f3136)
    mythical = "The best items in the game are in this category. If you find one of these items just run for an extract because they are worth __**more than 2,500,000₽**__."
    legendary = "Almost the best items. If you find one you have to extract as quick as possible. These items are worth __**between 500,000₽ and 2,500,000₽**__."
    veryrare = "Not the best of the best, but still very good items to keep in your inventory. They are worth __**between 250,000₽ and 500,000₽**__."
    rare = "Good items to keep in your inventory, especially in the early wipe when you don't have a lot of money. These are worth __**between 100,000₽ and 250,000₽**__."
    great = "Definitely keep this items in your inventory, as you can make some good money by selling them afterwards on the Flea Market. Generally worth __**between 50,000₽ and 100,000₽**__."
    average = "Take it if you find it, especially if you need it for your hideout, but if you find something more valuable don't hesitate to trow them away. Usually worth __**between 10,000₽ and 50,000₽**__."
    poor = "The worst items in the game. You can sell these for __**less than 10,000₽**__ so they are not really worth taking, unless you need them for your hideout."
    embed.add_field(name = "`⬜ Mythical`", value=mythical, inline= False)
    embed.add_field(name = "`🟨 Legendary`", value=legendary, inline= False)
    embed.add_field(name = "`🟪 Very Rare`", value=veryrare, inline= False)
    embed.add_field(name = "`🟧 Rare`", value=rare, inline= False)
    embed.add_field(name = "`🟦 Great`", value=great, inline= False)
    embed.add_field(name = "`🟩 Average`", value=average, inline= False)
    embed.add_field(name = "`🟥 Poor`", value=poor, inline= False)
    await interaction.followup.send(embed=embed)

#serverstatus
async def serverstatus(interaction:Interaction):
    await interaction.response.defer()
    query = '''
            query {
                status {
                    currentStatuses {
                        name
                        message
                        statusCode
                    }
                }
            }'''
    result = internal.search_items(query)
    result_filtered = result['data']['status']['currentStatuses']

    embed = Embed(title=f"Server Status", url="https://status.escapefromtarkov.com/", color=0x2f3136)
    
    status = ""
    for dictionary in result_filtered:
        name = dictionary['name']
        status_code = dictionary['statusCode']
        if status_code == 'OK':
            symbol = '🟢'
        elif status_code == 'Updating':
            symbol = '🔵'
        else:
            symbol = '🟠'
        
        if name != 'Global':
            status += f'`{name}: {symbol}`\n'
        else:
            global_status = symbol

    embed.add_field(name = f"`General Status🗄️: {global_status}`", value=status, inline= False)
    embed.set_footer(text = "🟢 = OK, 🔵 = Updating, 🟠 = Down\n\n⚠️Attention, this is the status of US servers. If you do not live in the USA click the title to get redirected to the official EFT status page and check the server status for your region.⚠️")
    await interaction.followup.send(embed=embed)