from dotenv import dotenv_values

import discord
from discord.ext import commands

from assets.cogsloader import cogsLoader
from assets.translator import myCustomTranslator

# Carregar arquivo env
config = dotenv_values(".env")

# Token do bot
TOKEN = config["TOKEN"]


# Estrutura de classe do Cliente do BOT
class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            case_insensitive=True,
            command_prefix=">>",
            intents=discord.Intents(
                members=True,
                messages=True,
                message_content=True,
                guild_messages=True,
                guilds=True
            ),
            help_command=None,
        )
        self.run(TOKEN)

    # Rotina inicianda antes do BOT estar completamente on-line
    async def setup_hook(self):
        myCustomTranslator() # Tradutor de comandos
        await cogsLoader(self) # 


MyBot()  # Inicar o BOT