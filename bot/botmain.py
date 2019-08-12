import json
import os, sys

from discord.ext.commands import Bot
from bot import reference as ref

with open("config.json", "r") as config:
    data = json.load(config)

bot = Bot(command_prefix=data["prefix"])
bot.remove_command("help")
cogs_dir = "cogs"
print(f"Running Python {sys.version}")

@bot.event
async def on_ready():
    #await bot.change_presence(game=Game(name="with fellow humans"))
    print(f"Logged in as {bot.user.name}")

cogs = os.listdir(cogs_dir)

if __name__ == "__main__":
    for extension in [f.replace('.py', '') for f in os.listdir(cogs_dir) if os.path.isfile(os.path.join(cogs_dir, f))]:
        try:
            bot.load_extension(f"{cogs_dir}.{extension}")
        except Exception as e:
            print(e)
            print(f'Failed to load extension {extension}.')
    bot.run(ref.TOKEN)
