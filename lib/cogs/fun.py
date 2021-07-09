# from discord.embeds import Embed
from random import choice, randint
from typing import Optional

from discord import Member
from discord.ext.commands import Cog, command

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='hi', aliases=['hey', 'hee'], hide=False, pass_context=True)
    async def say_hi_to_user(self, ctx, *args):
        await ctx.send(f"{choice(('hello', 'hey', 'hi', 'hee'))} {ctx.author.mention}")

    @command(name='dice', aliases=['roll'])
    async def roll_dice(self, ctx, dice_string: str):
        dice, value = (int(term) for term in dice_string.split('d'))
        rolls = [randint(1, value) for i in range(dice)]

        # print(" + ".join(str(r) for r in rolls) + f"= {sum(rolls)}")
        await ctx.send(" + ".join(str(r) for r in rolls) + f"= {sum(rolls)}")
        # await ctx.send('working fine')


    @command(name='slap', aliases=['hit'])
    async def slap_memeber(self, ctx, member: Member, *, reason: Optional[str] = "no reason"):
        await ctx.send(f"{ctx.author.display_name} slapped {member.mention} for {reason}!")


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
