
from discord.ext.commands import Cog

class Fun(Cog):
    def __init__(self, bot):
        self.bot = bot

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            print('Setting cog ready..')
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