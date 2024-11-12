<p align="center">
    <img src="logo/Tarkov%20Assistant%20Logo.png" alt="Tarkov Assistant Logo" width="400"/>
</p>
<p align="center">
    <img src="https://img.shields.io/badge/version-0.15-blue.svg" alt="Version"/>
    <img src="https://img.shields.io/github/license/mashape/apistatus.svg" alt="License"/>
    <img src="https://img.shields.io/badge/Python-3.8%20--%203.12-brightgreen.svg" alt="Python"/>
    <img src="https://img.shields.io/badge/Contributions-Welcome-brightgreen" alt="Contributions"/>
    <a href="https://discord.gg/Gy6QGmajjU">
        <img src="https://img.shields.io/badge/Discord-7289DA?style=flat&logo=discord&logoColor=white" alt="Discord Server"/>
    </a>
</p>

# Tarkov Assistant

Tarkov Assistant is a helpful Discord bot designed to enhance your experience in Escape from Tarkov with a variety of commands that ease your gameplay.

## 🔥・Features

✔ Item information, including prices and usage  
✔ Boss details and strategies  
✔ Server status updates  
✔ Patch notes  
✔ Easy-to-use command interface

---

## 📜・List of Commands

- `/ammo {name}` - Get round info (damage, speed, weight, modifiers).
- `/item {name}` - Get item info (tier, flea price, vendor sell price, usage in tasks).
- `/auto {image}` - Automatically scans items from an image and returns their price and the best vendor to sell them at.
- `/boss {name}` - Get boss info (location, guards, loot, strategies).
- `/serverstatus` - Check EFT server status.
- `/tiers` - Information about the tier system.
- `/patchnotes` - Get the latest patch notes.
- `/bug` - Report bugs directly to developers (special role in Support Server).
- `/help` - View command descriptions.

---

## 🚀・Setup Tarkov Assistant

1. Go to the [Releases](https://github.com/ersignee/tarkovassistant/releases) Tab and download the latest .zip file.
2. Extract the .zip archive.
3. Press SHIFT+RIGHT-CLICK in the extracted folder and open CMD (it should open it by default in the script folder).
4. Install the required pip modules:
   <pre>pip install -r requirements.txt</pre>
5. Setup .env using:
   <pre>API_TOKEN = 'YOUR_BOT_TOKEN'</pre>
5. Run the bot using:
   <pre>python main.py</pre>

---

## 🆕・Upcoming

```diff
・?
```

---

## 💭・ChangeLog

```diff
v0.15・23/10/2024
・New Boss: Partisan
・New items: All new 0.15 items and ammo
・New Command: /auto {image} to automatically check item prices from an image
Fixes:
・Bug that made the database update fail due to a change in type in the item queries, causing the bot to break.
```

## 📄・License

This project is licensed under the MIT License - see the [LICENSE.md](./LICENSE) file for details.
```js
・Permission is granted to use, copy, modify, and distribute this software ("Software") for free, under the following conditions:
・Include the copyright notice and this permission notice in all copies or substantial portions of the Software.
・THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND. The authors are not liable for any claims, damages, or other liabilities arising from the use of the Software.
・Selling this Software is prohibited.
```
