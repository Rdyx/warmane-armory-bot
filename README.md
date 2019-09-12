# warmane-armory-bot
Discord bot for warmane armory

Based on https://realpython.com/how-to-make-a-discord-bot-python/

This bot is kinda simple and can be used to check if a char status such as:
   - Professions
   - Missing enchant/gem
   - Average Item Level

You can also use it to check a guild status such as:
   - Faction
   - Number of members
   - PVE Points (Warmane related)


# How to install
```bash
# create virtualenv
virtualenv -p python3 venv

# start venv
. venv/bin/activate

# install reqs
pip3 install -r reqs.txt

# start bot
python3 bot.py
```

# How to use
$$help - Show help

$$charsum [charName] [server](default to Icecrown)

$$guildsum [guildName] [server](default to Icecrown)
