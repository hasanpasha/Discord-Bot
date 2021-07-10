# from discord.embeds import Embed
from os import initgroups
from random import choice, randint
from typing import Optional, Text
from aiohttp import request
from attr import attr
from discord import Member, Embed
from discord.errors import HTTPException
from discord.ext.commands import (
    Cog, command, BadArgument, MissingRequiredArgument, BucketType, cooldown) 
# from discord.message import Message
from .non_cog.CustomExceptiosn import *

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.special_values = {}

    @command(name='hi', aliases=['hey', 'hee'], hide=False, pass_context=True)
    @cooldown(5, 10, BucketType.user)
    async def say_hi_to_user(self, ctx, *args):
        await ctx.send(f"{choice(('hello', 'hey', 'hi', 'hee'))} {ctx.author.mention}")

    @command(name='dice', aliases=['roll'])
    @cooldown(1, 30, BucketType.user)    # Every 1 time for 30 seconds
    async def roll_dice(self, ctx, dice_string: str):
        if dice_string:
            dice, value = (int(term) for term in dice_string.split('d'))

            self.special_values['dice_limit'] = 500
            self.special_values['value_limit'] = 100000000

            if dice > self.special_values['dice_limit'] or value > self.special_values['value_limit']:
                raise LargeNumberException()

            rolls = [randint(1, value) for i in range(dice)]
            print('sending')
            await ctx.send(" + ".join(str(r) for r in rolls) + f"= {sum(rolls)}")

    # Handle errors 
    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if hasattr(exc, "original"):
            if isinstance(exc.original, LargeNumberException):
                embed_ = Embed(title="Limits")
                fields = [
                    ("dice", self.special_values['dice_limit'], True),
                    ("value", self.special_values['value_limit'], True)
                ]
                for name, value, inline in fields:
                    embed_.add_field(name=name, value=value, inline=inline)
                await ctx.send("Numbers is too large, Please try a lower number.", embed=embed_)

            elif isinstance(exc.original, HTTPException):
                await ctx.send("Result is too large, Please try a lower number.")

    @command(name='slap', aliases=['hit'])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        # if isinstance(exc, MissingRequiredArgument):
        #     await ctx.send("One or more required arguments are missing.")

        if isinstance(exc, BadArgument):
            await ctx.send("I can't find the member.")

    @command(name='echo', aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)
    
    # Used for api requests
    async def get_data(self, URL):
        async with request("GET", URL, headers={}) as resp:
            if resp.status == 200:  # OK
                return await resp.json()
            else:
                return resp.status
   
    @command(name='fact', aliases=['fact-about'])
    @cooldown(1, 60, BucketType.user)
    async def animal_fact(self, ctx, animal: Optional[str]):
        animals = ('dog', 'cat', 'panda', 'fox', 'bird', 'koala', )
        get_data = self.get_data
        async def send_fact(animal):
            FACT_URL = f"https://some-random-api.ml/facts/{animal.lower()}"
            IMAGE_URL = f"https://some-random-api.ml/img/{animal.lower()}"
            # if data := await get_data(FACT_URL):
            fact_data = await get_data(FACT_URL)
            if isinstance(fact_data, dict):
                embed = Embed(
                    title=f"{animal.title()} fact",
                    description=fact_data['fact'],
                    colour=ctx.author.colour
                )

                image_data = await get_data(IMAGE_URL)
                if isinstance(image_data, dict):
                    image_url = image_data['link']
                    embed.set_image(url=image_url)

                await ctx.send(embed=embed)
            
            else:
                await ctx.send(f"API returned a {fact_data} status.")
                return
            
        if animal:
            if animal.lower() in animals:
                await send_fact(animal.lower())
            else:
                await ctx.send("No facts are available for this animal.")

        else:
            await send_fact(choice(animals))
        
    @command(name='meme', aliases=['mem', 'memes'])
    @cooldown(1, 45, BucketType.user)
    async def get_memes(self, ctx):
        URL = "https://some-random-api.ml/meme"
        get_data = self.get_data
        data = await get_data(URL)
        if isinstance(data, dict):
            embed = Embed(
                title=data['caption'],
            )
            embed.set_image(url=data['image'])
            await ctx.send(embed=embed)

        else:
            await ctx.send(f"API returned a {data} status.")
            return

    @command(name='lyrics', aliases=['lyric', 'words'])
    @cooldown(1, 100, BucketType.user)   # Every 1 time for 100 seconds
    async def get_lyrics(self, ctx, *, name):
        suffix = '+'.join(name.split())
        URL = f"https://some-random-api.ml/lyrics?title={suffix}"
        # print()
        get_data = self.get_data
        data = await get_data(URL)
        if isinstance(data, dict):
            embed = Embed(
                title=data['title'],
            )
            fields = [
                ('author', data['author'], True),
                # ('lyrics', data['lyrics'], False)
            ]
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_image(url=data['thumbnail']['genius'])

            if len(data['lyrics']) > 4000:
                lyrics = data['lyrics'].split('\n')
                previous = -1
                for i in range(30, len(lyrics), 30):
                    if (len(lyrics) - i) < 30:
                        await ctx.send(' '.join(lyrics[previous + 1:]))
                    else:
                        # print('sending')
                        await ctx.send(' '.join(lyrics[previous + 1:i]))
                        previous = i
                    
                await ctx.send(embed=embed)
            # await ctx.send(data['lyrics'], embed=embed)

        else:
            await ctx.send(f"API returned a {data} status.")
            return
        
    # @get_lyrics.error
    # async def get_lyrics_error(self, ctx, exc):
    #     if isinstance(exc, MissingRequiredArgument):
    #         await ctx.send("Song name is missing.")

    @command(name='anime', aliases=['anim', 'animu'])
    @cooldown(1, 30, BucketType.user)
    async def get_anime_quote(self, ctx, cate: Optional[str]):
        if cate in ('wink', 'pat', 'hug', 'face-palm'):
            URL = f"https://some-random-api.ml/animu/{cate}"
            get_data = self.get_data
            data = await get_data(URL)
            if isinstance(data, dict):
                embed = Embed()
                embed.set_image(url=data['link'])
                # delete_after =
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {data} status.")
                return

        else:
            URL = "https://some-random-api.ml/animu/quote"
            get_data = self.get_data
            data = await get_data(URL)
            if isinstance(data, dict):
                embed = Embed(
                    title=data['characther'].title(),
                    description=data['sentence'],
                    colour=ctx.author.colour
                )
                embed.set_footer(text=data['anime'].title())
                await ctx.send(embed=embed)

            else:
                await ctx.send(f"API returned a {data} status.")
                return

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            print('Setting fun cog ready..')
            self.bot.cogs_ready.ready_up('fun')

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        if message.content.startswith('HELLO'):
            await message.reply('HELLO BACK TO YOU!')


def setup(bot):
    bot.add_cog(Fun(bot))
