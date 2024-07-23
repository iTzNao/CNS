import os
import json
import random

import datetime
import discord
from discord.ext import commands, tasks
from discord import app_commands
    

class CNS(commands.Bot):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(command_prefix = (), intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild=discord.Object(id=config["test_guild_id"]))
        self.tree.copy_global_to(guild=discord.Object(id=config["test_guild_id"]))
        
        for filename in os.listdir('bot/cogs'):
            if filename.endswith('.py'):
                print(f"🔄️ {filename[:-3]}")
                try:
                    await self.load_extension(f'cogs.{filename[:-3]}')
                    print(f"✅ {filename[:-3]}")
                except Exception as e:
                    print(f"❌ {filename[:-3]}")
                    raise
    
    async def get_config(self):
        with open("config.json", "r") as f:
            config = json.load(f)
            return config
        
    async def embed_error(self, interaction, error):
        embed = discord.Embed(
            title="Error",
            description=error,
            color=int(config["color"][1:], 16),
        )
        embed.set_footer(
            text=config["footer_text"],
            icon_url=f"images/{config['footer_icon']}.png",
        )

        return await interaction.response.send_message(embed=embed)


bot = CNS(intents=discord.Intents.none())


@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")
    
    clear_temp.start()
    status.start()


@tasks.loop(seconds=10)
async def status():
    config = await bot.get_config()
    
    await bot.change_presence(
        activity=discord.CustomActivity(name=random.choice(config["statuses"]))
    )


@tasks.loop(seconds=600)
async def clear_temp():
    directory_to_clear = "temp"
    for filename in os.listdir(directory_to_clear):
        file_path = os.path.join(directory_to_clear, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


if __name__ == "__main__":
    with open("config.json", "r") as f:
        config = json.load(f)
        
    if config["test_mode"] == True:
        bot.run(config["test_token"])
    else:
        bot.run(config["token"])
