
from lib.db import db
from discord.ext.commands import Cog, command, has_permissions, CheckFailure

class Prefix(Cog):
    def __init__(self, bot):
        self.bot = bot

    @command(name='prefix')
    @has_permissions(manage_guild=True)
    async def change_prefix(self, ctx, new: str):
        limit = 3
        if len(new) > limit:
            await ctx.send(f"The prefix can not be more than {limit} characters in length.")
        else:
            db.execute("UPDATE guilds SET Prefix = ? WHERE GuildID = ?", new, ctx.guild.id)
            await ctx.send(f"Prefix set to {new}")

    # @change_prefix.error
    # async def change_prefix_error(self, ctx, exc):
    #     if isinstance(exc, CheckFailure):
    #         await ctx.send("You need the Manage Messages premission to do that.")

    @Cog.listener()
    async def on_ready(self):
        if not self.bot.ready:
            print('Setting prefix cog ready..')
            self.bot.cogs_ready.ready_up('prefix')


def setup(bot):
    bot.add_cog(Prefix(bot))
