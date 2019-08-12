import discord
from discord.ext import commands
import aiofiles, aiohttp
from PIL import Image, ImageEnhance
import os, shutil
from os import listdir
from os.path import isfile, join
import imageio

class DeepFry(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        content = str(message.content).lower()

        # Deep fry previous image
        if content.lower().startswith("deepfry") or content.lower().startswith("deep fry"):
            number = 2
            img = ""

            # et previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "deep fry" or x.content != "deep fry":
                    if x.content == "":
                        img = x.attachments[0]["url"]
                    else:
                        img = x.content

            # Download image from URL
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:

                            # Get values for deep fry
                            try:
                                saturation_val = int(os.environ.get("FRY_SAT"))
                                brightness_val = int(os.environ.get("FRY_BRIGHT"))
                                contrast_val = int(os.environ.get("FRY_CONTRAST"))
                                sharpness_val = int(os.environ.get("FRY_SHARPNESS"))
                            except Exception as e:
                                print(e)
                                saturation_val = 4
                                brightness_val = 4
                                contrast_val = 20
                                sharpness_val = 300

                            file = await aiofiles.open("deepfried.png", mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                            # Open with PIL and "enhance" it
                            im = Image.open("deepfried.png")
                            saturated = ImageEnhance.Color(im).enhance(saturation_val)
                            brightness = ImageEnhance.Brightness(saturated).enhance(brightness_val)
                            contrast = ImageEnhance.Contrast(brightness).enhance(contrast_val)
                            final = ImageEnhance.Sharpness(contrast).enhance(sharpness_val)

                            final.save("deepfried.png", format="png")
                            await channel.send("Fresh from the fryer!", file=discord.File("deepfried.png"))

                    # Delete temp picture file
                    os.remove("deepfried.png")
            except Exception as e:
                print(e)
                await channel.send("```Found no image```")


def setup(bot):
    bot.add_cog(DeepFry(bot))