import discord
from discord.ext import commands
import requests
from discord import app_commands
from typing import List
import datetime
import string
import random


class Wiki(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def query_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        
        if current is None or current == "" or current == " ":
            sliced_query = random.choice(string.ascii_lowercase)
        elif len(current) > 1:
            sliced_query = current[:-1]
        else:
            sliced_query = current

        url = "https://www.thefinals.wiki/w139/api.php?action=opensearch&format=json&search=" + sliced_query

        response = requests.get(url)

        data = response.json()

        pages = data[1]
        
        unique_pages = []
        added_pages = set()

        for version in pages:
            version_lower = version.lower()
            if version_lower not in added_pages:
                unique_pages.append(version)
                added_pages.add(version_lower)
        
        return [
            app_commands.Choice(name=page, value=page)
            for page in unique_pages
        ][:25]

    @app_commands.command(name="wiki", description="Search the wiki for a page.")
    @app_commands.autocomplete(query=query_autocomplete)
    @app_commands.describe(query="Query to search")
    async def wiki(self, interaction: discord.Interaction, query: str):
        try:
            config = await self.bot.get_config()
            
            if len(query) > 1:
                sliced_query = query[:-1]
            else:
                sliced_query = query
                
            url = "https://www.thefinals.wiki/w139/api.php?action=opensearch&format=json&search=" + sliced_query

            response = requests.get(url)

            data = response.json()
            
            if data == [f"{sliced_query}", [], [], []]:
                return await self.bot.embed_error(interaction, f"No page named found with the query `{query}`.")

            title = data[1][0]
            url = data[3][0]

            embed = discord.Embed(
                title=title,
                description=f"Read More:\n⤷ [` thefinals.wiki/{title.lower().replace(' ', '_')} `]({url})",
                color=int(config["color"][1:], 16),
            )

            embed.set_footer(
                text=config["footer_text"],
                icon_url=f"images/{config['footer_icon']}.png",
            )

            return await interaction.response.send_message(embed=embed)

        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Wiki(bot))
