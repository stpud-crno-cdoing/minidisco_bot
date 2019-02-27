import logging
from random import choice

log = logging.getLogger("discord")


async def say_hello(_, message):
    try:
        greetings = ["Привет", "Алоха", "Шалом", "Ассаламу алейкум", "Ave", "Мабухай"]
        await message.channel.send("{}, {}!".format(choice(greetings), message.author.mention))
    except Exception as e:
        log.exception(e)


async def say_goodbye(_, message):
    try:
        await message.channel.send("НУ ВСЁ НАХУЙ Я ВЫПИЛИВАЮСЬ")
    except Exception as e:
        log.exception(e)
