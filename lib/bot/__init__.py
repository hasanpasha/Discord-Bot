from asyncio.tasks import Task
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from discord import (
    Intents,
    Embed,
    File
)
from discord.ext.commands import Bot as BotBase
from discord.ext.commands import CommandNotFound

PREFIX = "+"
OWNER_IDS = [
    438073319900839986
]

class Bot(BotBase):
    def __init__(self):
        self.PREFIX = PREFIX
        self.ready = False
        self.guild = None
        self.scheduler = AsyncIOScheduler()
        super().__init__(
            command_prefix=PREFIX,
            owner_ids=OWNER_IDS,
            Intents=Intents.all()
        )
 
    def run(self, version):
        self.VERSION = version

        with open('./lib/bot/token.0', 'r', encoding='utf-8') as tf:
            self.TOKEN = tf.read()

        print("running bot...")
        super().run(self.TOKEN, reconnect=True)

    async def on_connect(self):
        print("bot connected")

    async def on_disconnect(self):
        print("bot disconnected")

    async def on_error(self, err, *args, **kwargs):
        if err == "on_command_error":
            await args[0].send("Something went wrong.")

        else:
            stdout_channel = self.get_channel(862940566370254868)
            await stdout_channel.send("An error occured.")

        raise

    async def on_command_error(self, ctx, exc):
        if isinstance(exc, CommandNotFound):
            # await ctx.send("Wrong command.")
            pass

        elif hasattr(exc, "original"):
            raise exc.original

        else:
            raise exc


    async def on_ready(self):
        if not self.ready:
            self.ready = True
            print("bot ready")

            self.guild = self.get_guild(853338000368599102)
            stdout_channel = self.get_channel(862940566370254868)
            await stdout_channel.send("Now Online!")

            embed = Embed(
                title="Now Online!",
                description="The server is now online",
                colour=0xFF0000,
                timestamp=datetime.utcnow()
            )
            fields = [
                ("Owner", "Hasan Pasha", True),
                ("Another field", "This field is next to each other", True),
                ("A non-inline field", "This field will appear on it's own row.", False)
            ]

            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
            embed.set_author(name="Demons Army", icon_url=self.guild.icon_url)
            embed.set_footer(text="This is the footer.")
            embed.set_image(url=self.guild.icon_url)
            embed.set_thumbnail(url=self.guild.icon_url)

            await stdout_channel.send(embed=embed)

            await stdout_channel.send(file=File('./lib/db/data/images/avatar.png'))

        else:
            print("bot reconnected")

    async def on_message(self, message):
        pass


bot = Bot()
