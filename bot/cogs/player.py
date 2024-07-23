import discord
from discord.ext import commands
import sqlite3
import requests
from discord import app_commands
from typing import List
import datetime
import re
import math


def get_leaderboard_table(leaderboard):
    tables = [
        "cb1",
        "cb2",
        "ob1",
        "s1c",
        "s1s",
        "s1x",
        "s1p",
        "ce1",
        "s2c",
        "s2s",
        "s2x",
        "s2p",
        "ce2",
        "ta",
        "ce3",
    ]
    table = leaderboard[leaderboard.find("[") + 1 : leaderboard.find("]")].lower()

    if table in tables:
        return table
    else:
        return None


def get_table_data(table, player):
    player = re.sub(r"^\d+\.\s+", "", player)
    if table in ["cb1", "cb2", "ob1", "s1c", "s1s", "s1x", "s1p"]:
        with sqlite3.connect("databases/rankdata.sqlite") as conn:
            cursor = conn.cursor()
        cursor.execute(
            f"SELECT rank, username, fame, cashouts FROM {table} WHERE username = ? COLLATE NOCASE",
            (player,),
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    elif table == "ce1":
        with sqlite3.connect("databases/eventdata.sqlite") as conn:
            cursor = conn.cursor()
        cursor.execute(
            f"SELECT rank, username, cashouts FROM ce1 WHERE username = ? COLLATE NOCASE",
            (player,),
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    elif table == "ce2":
        with sqlite3.connect("databases/eventdata.sqlite") as conn:
            cursor = conn.cursor()
        cursor.execute(
            f"SELECT rank, username, distance FROM ce2 WHERE username = ? COLLATE NOCASE",
            (player,),
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data
    
    elif table == "ce3":
        with sqlite3.connect("databases/eventdata.sqlite") as conn:
            cursor = conn.cursor()
        cursor.execute(
            f"SELECT rank, username, kills FROM ce3 WHERE username = ? COLLATE NOCASE",
            (player,),
        )
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data

    elif table == "ta":
        url = "https://storage.googleapis.com/embark-discovery-leaderboard/terminal-attack-leaderboard-discovery-live.json"
        
        response = requests.get(url)
        response_data = response.json()

        matching_items = [
            (item["r"], item["name"], item["s"], item["wg"], item["wr"], item["tr"], item["k"])
            for item in response_data
            if player.lower() == item["name"].lower()
        ]

        if not matching_items:
            return None

        data = matching_items[0]
        return data

    else:
        table_urls = {
            "s2c": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-crossplay-discovery-live.json",
            "s2s": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-steam-discovery-live.json",
            "s2x": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-xbox-discovery-live.json",
            "s2p": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-psn-discovery-live.json",
        }

        url = table_urls[table]

        response = requests.get(url)
        response_data = response.json()

        matching_items = [
            (item["r"], item["name"], item["ri"])
            for item in response_data
            if player.lower() == item["name"].lower()
        ]

        if not matching_items:
            return None

        data = matching_items[0]
        return data


def parse_leaderboard_data(table, data, embed, formatting):
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
    
    if table in ["cb1", "cb2", "ob1", "s1c", "s1s", "s1x", "s1p"]:
        rank, username, fame, cashouts = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string     = f"{red}Rank{end}     ┃ {top_3_emoji}{rank}"
        username_string = f"{red}Username{end} ┃ {username}"
        fame_string     = f"{red}Fame{end}     ┃ {fame}"
        cashouts_string = f"{red}Cashouts{end} ┃ {cashouts}"

        embed.description = f"```{ansi_code}\n{rank_string}\n{username_string}\n{fame_string}\n{cashouts_string}\n```"

    elif table == "ce1":
        rank, username, cashouts = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string     = f"{red}Rank{end}     ┃ {top_3_emoji}{rank}"
        username_string = f"{red}Username{end} ┃ {username}"
        cashouts_string = f"{red}Cashouts{end} ┃ ${cashouts}"

        embed.description = (
            f"```{ansi_code}\n{rank_string}\n{username_string}\n{cashouts_string}\n```"
        )
        embed.set_image(url=f"images/ce1.png")

    elif table == "ce2":
        rank, username, distance = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string     = f"{red}Rank{end}     ┃ {top_3_emoji}{rank}"
        username_string = f"{red}Username{end} ┃ {username}"
        distance_string = f"{red}Distance{end} ┃ {distance} km"

        embed.description = (
            f"```{ansi_code}\n{rank_string}\n{username_string}\n{distance_string}\n```"
        )
        embed.set_image(url=f"images/ce2.png")
        
    elif table == "ce3":
        rank, username, kills = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string     = f"{red}Rank{end}     ┃ {top_3_emoji}{rank}"
        username_string = f"{red}Username{end} ┃ {username}"
        kills_string    = f"{red}Kills{end}    ┃ {kills}"

        embed.description = (
            f"```{ansi_code}\n{rank_string}\n{username_string}\n{kills_string}\n```"
        )
        embed.set_image(url=f"images/ce3.png")
        
    elif table == "ta1":
        rank, username, score, games_won, rounds_won, total_rounds, eliminations = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string         = f"{red}Rank{end}         ┃ {top_3_emoji}{rank}"
        username_string     = f"{red}Username{end}     ┃ {username}"
        rounds_won_string   = f"{red}Rounds Won{end}   ┃ {rounds_won}"
        total_rounds_string = f"{red}Total Rounds{end} ┃ {total_rounds}"
        eliminations_string = f"{red}Eliminations{end} ┃ {eliminations}"
        games_won_string    = f"{red}Games Won{end}    ┃ {games_won}"
        score_string        = f"{red}Score{end}        ┃ {score}"

        embed.description = (
            f"```{ansi_code}\n{rank_string}\n{username_string}\n{rounds_won_string}\n{total_rounds_string}\n{eliminations_string}\n{games_won_string}\n{score_string}\n```"
        )

    else:
        rank, username, fame = data

        if rank == 1:
            top_3_emoji = "🥇"
        elif rank == 2:
            top_3_emoji = "🥈"
        elif rank == 3:
            top_3_emoji = "🥉"
        else:
            top_3_emoji = ""

        rank_string     = f"{red}Rank{end}     ┃ {top_3_emoji}{rank}"
        username_string = f"{red}Username{end} ┃ {username}"

        embed.description = f"```{ansi_code}\n{rank_string}\n{username_string}\n```"

        ingame_rank_mapping = {
            20: "diamond1",
            19: "diamond2",
            18: "diamond3",
            17: "diamond4",
            16: "platinum1",
            15: "platinum2",
            14: "platinum3",
            13: "platinum4",
            12: "gold1",
            11: "gold2",
            10: "gold3",
            9: "gold4",
            8: "silver1",
            7: "silver2",
            6: "silver3",
            5: "silver4",
            4: "bronze1",
            3: "bronze2",
            2: "bronze3",
            1: "bronze4",
        }

        ingame_rank = ingame_rank_mapping[fame]

        embed.set_thumbnail(
            url=f"images/rank_{ingame_rank}.png"
        )


class Player(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def leaderboard_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        leaderboards = [
            "Closed Beta 1 [cb1]",
            "Closed Beta 2 [cb2]",
            "Open Beta 1 [ob1]",
            "Season 1 - Crossplay [s1c]",
            "Season 1 - Steam [s1s]",
            "Season 1 - Xbox [s1x]",
            "Season 1 - PSN [s1p]",
            "Community Event 1 [ce1]",
            "Season 2 - Crossplay [s2c]",
            "Season 2 - Steam [s2s]",
            "Season 2 - Xbox [s2x]",
            "Season 2 - PSN [s2p]",
            "Community Event 2 [ce2]",
            "Terminal Attack [ta]",
            "Community Event 3 [ce3]"
        ]
        return [
            app_commands.Choice(name=leaderboard, value=leaderboard)
            for leaderboard in leaderboards
            if current.lower() in leaderboard.lower()
        ][:25]

    async def player_autocomplete(
        self,
        interaction: discord.Interaction,
        current: str,
    ) -> List[app_commands.Choice[str]]:
        players = []
        if "leaderboard" in interaction.namespace:
            leaderboard = interaction.namespace["leaderboard"]
            table = get_leaderboard_table(leaderboard)

            if table in ["cb1", "cb2", "ob1", "s1c", "s1s", "s1x", "s1p"]:
                with sqlite3.connect("databases/rankdata.sqlite") as conn:
                    cursor = conn.cursor()
                cursor.execute(f"SELECT rank, username FROM {table}")
                usernames = cursor.fetchall()
                players = [f"{item[0]}. {item[1]}" for item in usernames]

            elif table in ["ce1", "ce2", "ce3"]:
                with sqlite3.connect("databases/eventdata.sqlite") as conn:
                    cursor = conn.cursor()
                cursor.execute(f"SELECT rank, username FROM {table}")
                usernames = cursor.fetchall()
                players = [f"{item[0]}. {item[1]}" for item in usernames]
                
            elif table == "ta":
                url = "https://storage.googleapis.com/embark-discovery-leaderboard/terminal-attack-leaderboard-discovery-live.json"

                response = requests.get(url)
                response_data = response.json()

                players = [f"{item['r']}. {item['name']}" for item in response_data]

            else:
                table_urls = {
                    "s2c": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-crossplay-discovery-live.json",
                    "s2s": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-steam-discovery-live.json",
                    "s2x": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-xbox-discovery-live.json",
                    "s2p": "https://storage.googleapis.com/embark-discovery-leaderboard/s2-leaderboard-psn-discovery-live.json",
                }

                url = table_urls[table]

                response = requests.get(url)
                response_data = response.json()

                players = [f"{item['r']}. {item['name']}" for item in response_data]

        return [
            app_commands.Choice(name=player, value=player)
            for player in players
            if current.lower() in player.lower()
        ][:25]

    @app_commands.command(
        name="player", description="Lookup a player's rank and stats."
    )
    @app_commands.autocomplete(leaderboard=leaderboard_autocomplete)
    @app_commands.autocomplete(player=player_autocomplete)
    @app_commands.describe(leaderboard="Leaderboard to search")
    @app_commands.describe(player="Player to get stats on")
    @app_commands.describe(formatting="Colour formatting")
    async def player(
        self, interaction: discord.Interaction, leaderboard: str, player: str, formatting: bool = True
    ):
        try:
            config = await self.bot.get_config()

            if player == None:
                return await self.bot.embed_error(
                    interaction, "Please provide a player to search."
                )

            table = get_leaderboard_table(leaderboard)

            if table == None:
                embed = self.bot.embed_error(
                    config, "Please provide a valid leaderboard to search."
                )
                return await interaction.response.send_message(embed=embed)

            data = get_table_data(table, player)

            if data == None:
                return await self.bot.embed_error(interaction, "Player not found.")

            embed = discord.Embed(
                title=leaderboard,
                color=int(config["color"][1:], 16),
            )

            embed.set_footer(
                text=config["footer_text"],
                icon_url=f"images/{config['footer_icon']}.png",
            )

            parse_leaderboard_data(table, data, embed, formatting)
            return await interaction.response.send_message(embed=embed)

        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Player(bot))
