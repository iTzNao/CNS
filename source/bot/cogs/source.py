import discord
from discord.ext import commands
from discord import app_commands

class Source(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="source", description="View the original source code by iTz_Nao."
    )
    async def playercount(self, interaction: discord.Interaction):
        try:
            return await interaction.response.send_message("**Source Code**\nThis bot is derived from the very popular Discord bot \"CNS\" made for THE FINALS.\nhttps://github.com/iTzNao/CNS\n-# :gear: BSD 3-Clause License / Copyright (c) 2024, iTz_Nao")
        
        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Source(bot))
