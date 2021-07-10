# from asyncio.tasks import Task, sleep
from datetime import datetime
from asyncio import sleep
from glob import glob
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from discord import (
    Intents,
    Embed,
    File,
)
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import Context
from discord.errors import Forbidden, HTTPException
from discord.ext.commands.errors import (
     MissingRequiredArgument, BadArgument, CommandNotFound, CommandOnCooldown
)
from lib.cogs.non_cog.CustomExceptiosn import LargeNumberException
from lib.db import db

PREFIX = "!"
OWNER_IDS = [
    438073319900839986
]
COGS = [path.split('/')[-1][:-3] for path in glob('./lib/cogs/*.py')]
IGNORE_EXCEPTIONS = (BadArgument, LargeNumberException, CommandNotFound)

class CogsReady(object):
    def __init__(self):
        for cog in COGS:
            setattr(self, cog, False)

    def ready_up(self, cog):
        setattr(self, cog, True)

    @property
    def all_ready(self):
        return all([getattr(self, cog) for cog in COGS])


class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.cogs_ready = CogsReady()
        self.guild = None
        self.scheduler = AsyncIOScheduler()

        db.autosave(self.scheduler)

        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            Intents=Intents.all()
        )
    
    def setup(self):
        for cog in COGS:
            self.load_extension(f'lib.cogs.{cog}')
            print(f"\'{cog}\' cog loaded")

    def run(self, version):
        self.VERSION = version

        print('running setup..')
        self.setup()

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def process_commands(self, message):
        ctx = await self.get_context(message, cls=Context)

        if ctx.command is not None and ctx.guild is not None:
            if self.ready:
                await self.invoke(ctx)

            else:
                await ctx.send("I'm not ready to receive command, Please wait for a few seconds.")

    async def rules_reminder(self):
        # stdout_channel = self.get_channel(862940566370254868)
        await self.stdout_channel.send("Remember to adhere to the rules!")


    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong with the command.")
            # print(err)

        else:
            await self.stdout_channel.send(f"An error occured. [{err}]")
            # raise

    async def on_command_error(self, ctx, exc):
        if hasattr(exc, "original"):
            if isinstance(exc.original, HTTPException):
                await ctx.send("Unable to send the message.")

            elif isinstance(exc.original, Forbidden):
                await ctx.send("I do not have the premission to do that.")

        else:

            if any([isinstance(exc, error) for error in IGNORE_EXCEPTIONS]):
                pass

            elif isinstance(exc, CommandOnCooldown):
                await ctx.send(f"The command is on cooldown, Try again in {exc.retry_after:,.2f}", delete_after=exc.retry_after / 2)
                # await ctx.delete()

            elif isinstance(exc, MissingRequiredArgument):
                await ctx.send("One or more required arguments are missing.")

            # elif isinstance(exc, CommandNotFound):
            #     await ctx.send("Command is not available.")

            else:
                await ctx.send(exc)


    async def on_ready(self):
        if not self.ready:
            self.stdout_channel = self.get_channel(862940566370254868)
            self.guild = self.get_guild(853338000368599102)
            self.scheduler.add_job(self.rules_reminder, CronTrigger(day_of_week=0, hour=12, minute=0, second=0))
            self.scheduler.start()

            # embed = Embed(
            #     title="Now Online!",
            #     description="The server is now online",
            #     colour=0xFF0000,
            #     timestamp=datetime.utcnow()
            # )
            # fields = [
            #     ("Owner", "Hasan Pasha", True),
            #     ("Another field", "This field is next to each other", True),
            #     ("A non-inline field", "This field will appear on it's own row.", False)
            # ]
            # for name, value, inline in fields:
            #     embed.add_field(name=name, value=value, inline=inline)
            # embed.set_author(name="Demons Army", icon_url=self.guild.icon_url)
            # embed.set_footer(text="This is the footer.")
            # embed.set_image(url=self.guild.icon_url)
            # embed.set_thumbnail(url=self.guild.icon_url)
            # await stdout_channel.send(embed=embed)
            # await stdout_channel.send(file=File('./lib/db/data/images/avatar.png'))

            while not self.cogs_ready.all_ready:
                await sleep(0.5)

            self.ready = True
            await self.stdout_channel.send("Now Online!")
            print("bot ready")

        else:
            print("bot reconnected")

    async def on_message(self, message):
        # if message.author.bot and message.author != message.guild.me:
        if not message.author.bot:
            await self.process_commands(message)


bot = Bot()
