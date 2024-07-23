import discord
from discord.ext import commands
from discord import app_commands
import datetime
from PIL import Image, ImageDraw, ImageFont


class Generate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="generate", description="Generate text into THE FINALS font!"
    )
    @app_commands.describe(text="Text to generate")
    @app_commands.describe(tm="Slap a ™ at the end")
    async def generate(
        self, interaction: discord.Interaction, text: str, tm: bool = True
    ):
        try:
            config = await self.bot.get_config()

            text = text.upper()

            if tm == True:
                text = text + "™"

            font = ImageFont.truetype("resources/THE-FINALS-Font-Modified-By-iTz_Nao.ttf", 100, encoding="unic")
            text_width = font.getlength(text)
            width = text_width + 50
            height = 100

            image = Image.new("RGBA", (int(width), height), (0, 0, 0, 0))
            draw = ImageDraw.Draw(image)

            y = (height - 150) // 2

            draw.text((20, y), text, fill="#d21e3d", font=font, embedded_color=True)

            file_name = f"{interaction.user.id}-{datetime.datetime.now().timestamp()}"
            file_path = f"temp/{file_name}.png"

            image.save(file_path)

            with open(file_path, "rb") as file:
                await interaction.response.send_message(
                    file=discord.File(file, f"{file_name}.png")
                )

        except Exception as e:
            await self.bot.embed_error(interaction, f"{e}")
            raise


async def setup(bot):
    await bot.add_cog(Generate(bot))
