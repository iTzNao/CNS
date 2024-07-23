import discord
from discord.ext import commands
import requests
from discord import app_commands
import datetime

class PlayerCount(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="playercount", description="Check the live Steam playercount."
    )
    @app_commands.describe(formatting="Colour formatting")
    async def playercount(self, interaction: discord.Interaction, formatting: bool = True):
        try:
            config = await self.bot.get_config()

            url = "https://api.steampowered.com/ISteamUserStats/GetNumberOfCurrentPlayers/v1?appid=2073850"

            response = requests.get(url)
            response_data = response.json()

            player_count = response_data["response"]["player_count"]

            embed = discord.Embed(
                title="Playercount",
                color=int(config["color"][1:], 16),
            )
            
            if formatting:
                red = "\u001b[0;31m"
                green = "\u001b[0;32m"
                yellow = "\u001b[0;33m"
                purple = "\u001b[0;35m"
                blue = "\u001b[0;34m"
                grey = "\u001b[0;30m"
                bold = "\u001b[0;37m"
                end = "\u001b[0m"
                ansi_code = "ansi"
            else:
                red = ""
                green = ""
                yellow = ""
                purple = ""
                blue = ""
                grey = ""
                bold = ""
                end = ""
                ansi_code = ""
            
            steam_string = f"{red}Steam{end} ┃ {player_count}"
            
            embed.description = f"```{ansi_code}\n{steam_string}\n```"

            embed.set_footer(
                text=config['footer_text'],
                icon_url=f"images/{config['footer_icon']}.png",
            )
            return await interaction.response.send_message(embed=embed)
        
        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(PlayerCount(bot))
