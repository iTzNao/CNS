# os.date("%H:%M:%S",(time)/comp:GetPrefs("Comp.FrameFormat.Rate")).."."..string.format("%03d",(time)%comp:GetPrefs("Comp.FrameFormat.Rate")*1000/comp:GetPrefs("Comp.FrameFormat.Rate"))
# TTK = IF((BODY_DAMAGE > HEALTH), (0), (IF((ROUNDUP((HEALTH / BODY_DAMAGE)) > MAGAZINE_SIZE), (ROUND((ROUNDUP((HEALTH / BODY_DAMAGE)) / (RPM / 60) + RELOAD_SPEED), 2)), (ROUND(ROUNDUP((HEALTH / BODY_DAMAGE)) / (RPM / 60), 2)))))

import discord
from discord.ext import commands
import json
import math
from discord import app_commands
from typing import List
import json
import datetime


class Weapon(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def weapons_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        if "weapon" in interaction.namespace:
            weapon_one = interaction.namespace["weapon"]

        with open("databases/weapondata.json", "r", encoding="utf-8") as f:
            json_data = json.load(f)
            
        weapons = [weapon["name"] for weapon in json_data]


        if weapon_one in weapons:
            weapons.remove(weapon_one)

        return [
            app_commands.Choice(name=weapon, value=weapon)
            for weapon in weapons
            if current.lower() in weapon.lower()
        ][:25]

    @app_commands.command(name="weapon", description="Get information on a weapon.")
    @app_commands.autocomplete(weapon=weapons_autocomplete)
    @app_commands.autocomplete(compare_weapon=weapons_autocomplete)
    @app_commands.describe(weapon="Weapon to get stats on")
    @app_commands.describe(compare_weapon="Compare with the other weapon")
    @app_commands.describe(formatting="Colour formatting")
    async def weapon(self, interaction: discord.Interaction, weapon: str, compare_weapon: str = None, formatting: bool = True):
        try:
            config = await self.bot.get_config()

            with open("databases/weapondata.json", "r", encoding="utf-8") as f:
                json_data = json.load(f)

            weapon_one = weapon
            weapon_two = compare_weapon

            if weapon_one == None:
                return await self.bot.embed_error(interaction, "Please provide a weapon to search.")

            weapon_one_matching_items = [
                weapon for weapon in json_data if weapon_one.lower() == weapon["name"].lower()
            ]

            if not weapon_one_matching_items:
                return await self.bot.embed_error(interaction, f"No weapon named `{weapon_one}` found.")
            
            weapon_one_data = weapon_one_matching_items[0]
            
            if weapon_two != None:
                weapon_two_matching_items = [
                    weapon for weapon in json_data if weapon_two.lower() == weapon["name"].lower()
                ]
                
                weapon_two_data = weapon_two_matching_items[0]

            embed = discord.Embed(color = int(config["color"][1:], 16))
            
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
                
            for key, value in weapon_one_data.items():
                if value is None:
                    weapon_one_data[key] = f"N/A"
                    
            notes_string = ""
            
            if weapon_one and weapon_two:
                for key, value in weapon_two_data.items():
                    if value is None:
                        weapon_two_data[key] = f"N/A"
                    
                embed.set_author(
                    name=weapon_one_data["name"] + " vs " + weapon_two_data["name"],
                    icon_url=f"images/icon_VS.png",
                )

                max_length_one = (max(len(str(value)) for value in [value for key, value in weapon_one_data.items() if key != "recoil_pattern" and key != "additional_notes"]))
                                
                name_string             = f"{red}Name{end}            ┃ {weapon_one_data['name']           }{' ' * (max_length_one - len(str(weapon_one_data['name'])))} ┃ {weapon_two_data['name']}{end}"
                build_string            = f"{red}Build{end}           ┃ {weapon_one_data['build']          }{' ' * (max_length_one - len(str(weapon_one_data['build'])))} ┃ {weapon_two_data['build']}{end}"
                type_string             = f"{red}Type{end}            ┃ {weapon_one_data['type']           }{' ' * (max_length_one - len(str(weapon_one_data['type'])))} ┃ {weapon_two_data['type']}{end}"
                rpm_string              = f"{red}RPM{end}             ┃ {weapon_one_data['rpm']            }{' ' * (max_length_one - len(str(weapon_one_data['rpm'])))} ┃ {weapon_two_data['rpm']}{end}"
                mag_size_string         = f"{red}Magazine Size{end}   ┃ {weapon_one_data['mag_size']       }{' ' * (max_length_one - len(str(weapon_one_data['mag_size'])))} ┃ {weapon_two_data['mag_size']}{end}"
                body_damage_string      = f"{red}Body Damage{end}     ┃ {weapon_one_data['body_damage']    }{' ' * (max_length_one - len(str(weapon_one_data['body_damage'])))} ┃ {weapon_two_data['body_damage']}{end}"
                crit_multiplier_string  = f"{red}Crit Multiplier{end} ┃ {weapon_one_data['crit_multiplier']}{' ' * (max_length_one - len(str(weapon_one_data['crit_multiplier'])))} ┃ {weapon_two_data['crit_multiplier']}{end}"
                crit_damage_string      = f"{red}Crit Damage{end}     ┃ {weapon_one_data['crit_damage']    }{' ' * (max_length_one - len(str(weapon_one_data['crit_damage'])))} ┃ {weapon_two_data['crit_damage']}{end}"
                damage_per_mag_string   = f"{red}Damage per Mag{end}  ┃ {weapon_one_data['damage_per_mag'] }{' ' * (max_length_one - len(str(weapon_one_data['damage_per_mag'])))} ┃ {weapon_two_data['damage_per_mag']}{end}"
                damage_per_sec_string   = f"{red}Damage per Sec{end}  ┃ {weapon_one_data['damage_per_sec'] }{' ' * (max_length_one - len(str(weapon_one_data['damage_per_sec'])))} ┃ {weapon_two_data['damage_per_sec']}{end}"
                stk_light_string        = f"{red}STK Light{end}       ┃ {weapon_one_data['stk_light']      }{' ' * (max_length_one - len(str(weapon_one_data['stk_light'])))} ┃ {weapon_two_data['stk_light']}{end}"
                body_ttk_light_string   = f"{red}Body TTK Light{end}  ┃ {weapon_one_data['body_ttk_light'] }s{' ' * ((max_length_one - len(str(weapon_one_data['body_ttk_light']))) - 1)} ┃ {weapon_two_data['body_ttk_light']}s{end}"
                crit_ttk_light_string   = f"{red}Crit TTK Light{end}  ┃ {weapon_one_data['crit_ttk_light'] }s{' ' * ((max_length_one - len(str(weapon_one_data['crit_ttk_light']))) - 1)} ┃ {weapon_two_data['crit_ttk_light']}s{end}"
                stk_medium_string       = f"{red}STK Medium{end}      ┃ {weapon_one_data['stk_medium']     }{' ' * (max_length_one - len(str(weapon_one_data['stk_medium'])))} ┃ {weapon_two_data['stk_medium']}{end}"
                body_ttk_medium_string  = f"{red}Body TTK Medium{end} ┃ {weapon_one_data['body_ttk_medium']}s{' ' * ((max_length_one - len(str(weapon_one_data['body_ttk_medium']))) - 1)} ┃ {weapon_two_data['body_ttk_medium']}s{end}"
                crit_ttk_medium_string  = f"{red}Crit TTK Medium{end} ┃ {weapon_one_data['crit_ttk_medium']}s{' ' * ((max_length_one - len(str(weapon_one_data['crit_ttk_medium']))) - 1)} ┃ {weapon_two_data['crit_ttk_medium']}s{end}"
                stk_heavy_string        = f"{red}STK Heavy{end}       ┃ {weapon_one_data['stk_heavy']      }{' ' * (max_length_one - len(str(weapon_one_data['stk_heavy'])))} ┃ {weapon_two_data['stk_heavy']}{end}"
                body_ttk_heavy_string   = f"{red}Body TTK Heavy{end}  ┃ {weapon_one_data['body_ttk_heavy'] }s{' ' * ((max_length_one - len(str(weapon_one_data['body_ttk_heavy']))) - 1)} ┃ {weapon_two_data['body_ttk_heavy']}s{end}"
                crit_ttk_heavy_string   = f"{red}Crit TTK Heavy{end}  ┃ {weapon_one_data['crit_ttk_heavy'] }s{' ' * ((max_length_one - len(str(weapon_one_data['crit_ttk_heavy']))) - 1)} ┃ {weapon_two_data['crit_ttk_heavy']}s{end}"
                
            else:
                embed.set_author(
                    name=weapon_one_data["name"],
                    icon_url=f"images/icon_{weapon_one_data['name'].replace(' ', '_')}.png",
                )
                
                name_string             = f"{red}Name{end}            ┃ {weapon_one_data['name']}"
                build_string            = f"{red}Build{end}           ┃ {weapon_one_data['build']}"
                type_string             = f"{red}Type{end}            ┃ {weapon_one_data['type']}"
                rpm_string              = f"{red}RPM{end}             ┃ {weapon_one_data['rpm']}"
                mag_size_string         = f"{red}Magazine Size{end}   ┃ {weapon_one_data['mag_size']}"
                body_damage_string      = f"{red}Body Damage{end}     ┃ {weapon_one_data['body_damage']}"
                crit_multiplier_string  = f"{red}Crit Multiplier{end} ┃ {weapon_one_data['crit_multiplier']}"
                crit_damage_string      = f"{red}Crit Damage{end}     ┃ {weapon_one_data['crit_damage']}"
                damage_per_mag_string   = f"{red}Damage per Mag{end}  ┃ {weapon_one_data['damage_per_mag']}"
                damage_per_sec_string   = f"{red}Damage per Sec{end}  ┃ {weapon_one_data['damage_per_sec']}"
                stk_light_string        = f"{red}STK Light{end}       ┃ {weapon_one_data['stk_light']}"
                body_ttk_light_string   = f"{red}Body TTK Light{end}  ┃ {weapon_one_data['body_ttk_light']}s"
                crit_ttk_light_string   = f"{red}Crit TTK Light{end}  ┃ {weapon_one_data['crit_ttk_light']}s"
                stk_medium_string       = f"{red}STK Medium{end}      ┃ {weapon_one_data['stk_medium']}"
                body_ttk_medium_string  = f"{red}Body TTK Medium{end} ┃ {weapon_one_data['body_ttk_medium']}s"
                crit_ttk_medium_string  = f"{red}Crit TTK Medium{end} ┃ {weapon_one_data['crit_ttk_medium']}s"
                stk_heavy_string        = f"{red}STK Heavy{end}       ┃ {weapon_one_data['stk_heavy']}"
                body_ttk_heavy_string   = f"{red}Body TTK Heavy{end}  ┃ {weapon_one_data['body_ttk_heavy']}s"
                crit_ttk_heavy_string   = f"{red}Crit TTK Heavy{end}  ┃ {weapon_one_data['crit_ttk_heavy']}s"
                
                try:
                    if weapon_one_data["additional_notes"] != "N/A":
                        notes_list = weapon_one_data["additional_notes"].split("-")
                        notes_string = (
                            f"```{ansi_code}\n"
                            + (f"\n{red}-{end}".join([note.strip() for note in notes_list]))
                            + "\n```"
                        )
                except:
                    pass
                
                if weapon_one_data['recoil_pattern'] == None:
                    embed.set_image(url=f"images/recoil_NONE.png")
                else:
                    embed.set_image(url=f"images/recoil_{weapon_one_data['name'].replace(' ', '_')}.png")

            embed.description = (
                f"```{ansi_code}\n"
                f"{name_string}\n"
                f"{build_string}\n"
                f"{type_string}\n"
                f"{rpm_string}\n"
                f"{mag_size_string}\n"
                f"{body_damage_string}\n"
                f"{crit_multiplier_string}\n"
                f"{crit_damage_string}\n"
                f"{damage_per_mag_string}\n"
                f"{damage_per_sec_string}\n"
                f"{stk_light_string}\n"
                f"{body_ttk_light_string}\n"
                f"{crit_ttk_light_string}\n"
                f"{stk_medium_string}\n"
                f"{body_ttk_medium_string}\n"
                f"{crit_ttk_medium_string}\n"
                f"{stk_heavy_string}\n"
                f"{body_ttk_heavy_string}\n"
                f"{crit_ttk_heavy_string}\n"
                f"```\n{notes_string}"
            )
            
            embed.set_footer(text = config["footer_text"], icon_url=f"images/{config['footer_icon']}.png")

            return await interaction.response.send_message(embed=embed)

        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Weapon(bot))
