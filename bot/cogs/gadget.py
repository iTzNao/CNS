import discord
from discord.ext import commands
import json
from discord import app_commands
from typing import List
import datetime


class Gadget(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def gadget_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        gadgets = [
            "Breach Charge",
            "Gateway",
            "Glitch Grenade",
            "Smoke Grenade",
            "Sonar Grenade",
            "Stun Gun",
            "Thermal Vision",
            "Tracking Dart",
            "Vanishing Bomb",
            "APS Turret",
            "Data Reshaper",
            "Defibrillator",
            "Explosive Mine",
            "Gas Mine",
            "Glitch Trap",
            "Jump Pad",
            "Zipline",
            "Anti-Gravity Cube",
            "Barricade",
            "C4",
            "Dome Shield",
            "Motion Sensor",
            "Pyro Mine",
            "RPG-7",
            "Flashbang",
            "Frag Grenade",
            "Gas Grenade",
            "Goo Grenade",
            "Pyro Grenade",
        ]
        return [
            app_commands.Choice(name=gadget, value=gadget)
            for gadget in gadgets
            if current.lower() in gadget.lower()
        ][:25]

    @app_commands.command(name="gadget", description="Get information on a gadget.")
    @app_commands.autocomplete(gadget=gadget_autocomplete)
    @app_commands.describe(gadget="Gadget to get stats on")
    @app_commands.describe(formatting="Colour formatting")
    async def gadget(self, interaction: discord.Interaction, gadget: str, formatting: bool = True):
        try:
            config = await self.bot.get_config()

            with open("databases/gadgetdata.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)

            if gadget == None:
                embed = await self.bot.embed_error(
                    interaction, "Please provide a gadget to search."
                )

            matching_items = [
                item for item in json_data if gadget.lower() == item["name"].lower()
            ]

            if not matching_items:
                return await self.bot.embed_error(
                    interaction, f"No gadget named `{gadget}` found."
                )

            item = matching_items[0]

            if len(item["build"]) == 3:
                build_list = "All"
            else:
                build_list = ", ".join([item for item in item["build"]])

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

            name_string = f"{red}Name{end}            ┃ {item['name'] if item['name'] else 'N/A'}"
            build_string = f"{red}Build{end}           ┃ {build_list if build_list else 'N/A'}"
            type_string = f"{red}Type{end}            ┃ {item['type'] if item['type'] else 'N/A'}"
            health_string = f"{red}Health{end}          ┃ {item['health'] if item['health'] else 'N/A'}"
            damage_string = f"{red}Damage{end}          ┃ {item['damage'] if item['damage'] else 'N/A'}"
            cooldown_string = f"{red}Cooldown{end}        ┃ {item['cooldown'] if item['cooldown'] else 'N/A'}s"
            count_string = f"{red}Count{end}           ┃ {item['count'] if item['count'] else 'N/A'}"
            effect_duration_string = f"{red}Effect Duration{end} ┃ {item['effect_duration'] if item['effect_duration'] else 'N/A'}s"

            notes_string = ""
            if not len(item["notes"]) == 0:
                notes_string = (
                    f"```{ansi_code}\n"
                    + (
                        f"{red}-{end} "
                        + f"\n{red}-{end} ".join([note for note in item["notes"]])
                    )
                    + "\n```"
                )

            embed = discord.Embed(
                color=int(config["color"][1:], 16),
            )

            embed.set_author(
                name=item["name"],
                icon_url=f"images/icon_{item['name'].replace(' ', '_')}.png",
            )
            embed.description = f"```{ansi_code}\n{name_string}\n{build_string}\n{type_string}\n{health_string}\n{damage_string}\n{cooldown_string}\n{count_string}\n{effect_duration_string}\n```\n{notes_string}"

            embed.set_footer(
                text=config["footer_text"],
                icon_url=f"images/{config['footer_icon']}.png",
            )

            return await interaction.response.send_message(embed=embed)

        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Gadget(bot))
