import discord
from discord.ext import commands
import aiofiles, aiohttp
from PIL import Image
import os, shutil
from os import listdir
from os.path import isfile, join
import imageio

class JPEG(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self,message):
        channel = message.channel
        content = str(message.content).lower()
        print(content)

        # Takes previous image in chat and compresses it
        if content.lower().startswith("needsmorejpeg") or content.lower().startswith("needs more jpeg") \
                or content.lower().startswith("morejpeg") or content.lower().startswith("more jpeg"):
            number = 2
            img = ""

            # Get link to previous image in chat
            async for x in channel.history(limit=number):
                if x.content != "needsmorejpeg" or x.content != "needs more jpeg" or x.content != "morejpeg" \
                        or x.content != "more jpeg":
                    if x.content == "":
                        img = x.attachments[0]["url"]
                    else:
                        img = x.content

            # Download image locally to server
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(img) as resp:
                        if resp.status == 200:
                            file = await aiofiles.open("morejpeg.gif", mode="wb")
                            await file.write(await resp.read())
                            await file.close()

                            await channel.send(file=await self.assemble_gif("morejpeg.gif",os.getcwd()+"/download/gif"))

                            # Save as JPEG in lowest quality and send it

                            '''
                            im = Image.open("morejpeg.jpeg")
                            im = im.convert("RGB")
                            im.save("morejpeg.jpeg", format="jpeg", quality=1)
                            await channel.send(file=discord.File("morejpeg.jpeg"))'''

            except Exception as e:
                print(e)

                if img.split(".")[1] == "gif":
                    error = "Gif files are not supported"
                else:
                    error = "No image found in previous message"

    async def assemble_gif(self, inGif, outFolder):
        frame = Image.open(inGif)
        nframes = 0
        while frame:
            frame.save( '%s/%s-%s.gif' % (outFolder, os.path.basename(inGif), nframes ) , 'GIF', quality=1)
            nframes += 1
            try:
                frame.seek( nframes )
            except EOFError:
                break
        files = [f for f in listdir(outFolder) if isfile(join(outFolder, f))]
        images = []

        for file in files:
            images.append(imageio.imread(file))
        imageio.mimsave('jpeg.gif', images)

        return "jpeg.gif"


def setup(bot):
    bot.add_cog(JPEG(bot))