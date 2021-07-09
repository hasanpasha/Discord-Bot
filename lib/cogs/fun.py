# from discord.embeds import Embed
from os import initgroups
from random import choice, randint
from typing import Optional

from discord import Member, Embed
from discord.errors import HTTPException
from discord.ext.commands import Cog, command, BadArgument, MissingRequiredArgument
from .non_cog.CustomExceptiosn import *

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.special_values = {}

    @command(name='hi', aliases=['hey', 'hee'], hide=False, pass_context=True)
    async def say_hi_to_user(self, ctx, *args):
        await ctx.send(f"{choice(('hello', 'hey', 'hi', 'hee'))} {ctx.author.mention}")

    @command(name='dice', aliases=['roll'])
    async def roll_dice(self, ctx, dice_string: str):
        dice, value = (int(term) for term in dice_string.split('d'))

        self.special_values['dice_limit'] = 500
        self.special_values['value_limit'] = 100000000

        if dice > self.special_values['dice_limit'] or value > self.special_values['value_limit']:
            raise LargeNumberException()

        rolls = [randint(1, value) for i in range(dice)]
        await ctx.send(" + ".join(str(r) for r in rolls) + f"= {sum(rolls)}")

    # Handle errors 
    @roll_dice.error
    async def roll_dice_error(self, ctx, exc):
        if isinstance(exc.original, HTTPException):
            await ctx.send("Result is too large, Please try a lower number.")

        elif isinstance(exc.original, LargeNumberException):
            embed_ = Embed(title="Limits")
            fields = [
                ("dice", self.special_values['dice_limit'], True),
                ("value", self.special_values['value_limit'], True)
            ]
            for name, value, inline in fields:
                embed_.add_field(name=name, value=value, inline=inline)
            await ctx.send("Numbers is too large, Please try a lower number.", embed=embed_)

    @command(name='slap', aliases=['hit'])
    async def slap_member(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")

    @slap_member.error
    async def slap_member_error(self, ctx, exc):
        if isinstance(exc, MissingRequiredArgument):
            await ctx.send("One or more required arguments are missing.")

        elif isinstance(exc, BadArgument):
            await ctx.send("I can't find the member.")

    @command(name='echo', aliases=['say'])
    async def echo_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)


    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            print('Setting fun cog ready..')
            self.bot.cogs_ready.ready_up('fun')
        # await self.bot.stdout_channel.send("Fun cog is ready.")
        # print('Fun cog ready')

    @Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
            
        if message.content.startswith('HELLO'):
            await message.reply('HELLO BACK TO YOU!')


def setup(bot):
    bot.add_cog(Fun(bot))
