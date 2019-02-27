import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

import discord

from commands import commands
from config import config

log = logging.getLogger("discord")
log.setLevel(logging.DEBUG)
fh = RotatingFileHandler("{}/discord.log".format(str(Path.home())), mode='a', maxBytes=5 * 1024 * 1024, backupCount=1,
                         encoding='utf-8', delay=0)
fm = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(fm)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(fm)
log.addHandler(ch)
log.addHandler(fh)
client = discord.Client()


@client.event
async def on_message(message):
    try:
        # skip self messages
        if message.author == client.user:
            return

        # log message debug info
        try:
            log.debug("msg {} from {}:{} [channel: {}; server: {}]".format(message.id, message.author.id,
                                                                           message.author, message.channel.id,
                                                                           message.guild if message.guild is None
                                                                           else message.guild.id))
        except Exception as e:
            log.exception(e)

        # exit
        if message.content == '!stop' and message.author.id in config.admins:
            log.info("got stop command from {}".format(message.author))
            await commands.say_goodbye(client, message)
            await client.logout()

        # greetings
        if message.content.lower().startswith("hi") \
                or message.content.startswith("привет") \
                or message.content.startswith("здрав"):
            await commands.say_hello(client, message)
    except Exception as e:
        log.exception(e)


@client.event
async def on_ready():
    log.info("bot ready")
    activity = discord.Game(name="My Little Pony")
    await client.change_presence(activity=activity)


def main():
    client.run(config.TOKEN)


if __name__ == "__main__":
    log.debug("....... starting .......")
    main()
