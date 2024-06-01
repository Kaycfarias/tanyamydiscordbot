import discord
from discord import app_commands


class myCustomTranslator(app_commands.Translator):
    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ):
        """
        .`locale_str` é a string que está solicitando a tradução
         `locale` é o idioma de destino para traduzir
         `context` é a origem desta string, por exemplo, TranslationContext.command_name, etc
         Esta função deve retornar uma string (que foi traduzida), ou `None` para sinalizar que não há tradução disponível, e o padrão será o original
        """
        message_str = string.message
        if message_str == "help":
            if locale == discord.Locale.brazil_portuguese:
                return "ajuda"
        elif message_str == "See information about the bot and the list of available commands.":
            if locale == discord.Locale.brazil_portuguese:
                return "veja informações sobre bot e a lista de comandos disponíveis."

        elif message_str == "create":
            if locale == discord.Locale.brazil_portuguese:
                return "criar"

        elif message_str == "advanced":
            if locale == discord.Locale.brazil_portuguese:
                return "avançado"

        elif message_str == "[utilities] Open advanced menu for creating embeds":
            if locale == discord.Locale.brazil_portuguese:
                return "[útilidades] Abrir menu avançado para criação de embeds"

        elif message_str == "Provide the link of the message containing the embed to be copied":
            if locale == discord.Locale.brazil_portuguese:
                return "Fornecer o link da mensagem contendo a incorporação a ser copiada"

        elif message_str == "clear":
            if locale == discord.Locale.brazil_portuguese:
                return "limpar"

        elif message_str == "[Moderation] Clear chat messages.":
            if locale == discord.Locale.brazil_portuguese:
                return "[Moderação] Limpe mensagens do chat"

        elif message_str == "Please enter the number of messages to be deleted.":
            if locale == discord.Locale.brazil_portuguese:
                return "digite a quantidade de mensagens a serem apagadas."

        elif message_str == "say":
            if locale == discord.Locale.brazil_portuguese:
                return "falar"

        elif message_str == "[Misc] May I speak?":
            if locale == discord.Locale.brazil_portuguese:
                return "[Misc] Posso falar?"

        elif message_str == "Tell me what to say.":
            if locale == discord.Locale.brazil_portuguese:
                return "Me diga o que devo dizer."

        elif message_str == "Bot Latency":
            if locale == discord.Locale.brazil_portuguese:
                return "Latência do Bot"

        elif message_str == "[Utilities] Enable slow mode in a channel":
            if locale == discord.Locale.brazil_portuguese:
                return "[Utilidades] Ative o modo lento em um canal"

        elif message_str == "slowmode":
            if locale == discord.Locale.brazil_portuguese:
                return "modo_lento"

        elif message_str == "Enter the desired duration:":
            if locale == discord.Locale.brazil_portuguese:
                return "Digite a duração desejada:"

        elif message_str == "Select a channel:":
            if locale == discord.Locale.brazil_portuguese:
                return "Selecione um canal:"

        elif message_str == "Select the time unit:":
            if locale == discord.Locale.brazil_portuguese:
                return "Selecione a unidade de tempo:"

        elif message_str == "Second(s)":
            if locale == discord.Locale.brazil_portuguese:
                return "Segundo(s)"

        elif message_str == "Minute(s)":
            if locale == discord.Locale.brazil_portuguese:
                return "Minuto(s)"

        elif message_str == "Hour(s)":
            if locale == discord.Locale.brazil_portuguese:
                return "Hora(s)"
        elif message_str == "user":
            if locale == discord.Locale.brazil_portuguese:
                return "usuário"
        elif message_str == "[Utilities] View a user's avatar...":
            if locale == discord.Locale.brazil_portuguese:
                return "[Útilidades] Veja o avatar de um usuário..."
        elif message_str == "[Utilities] View a user's profile banner...":
            if locale == discord.Locale.brazil_portuguese:
                return "[Útilidades] Veja o banner de perfil de um usuário..."
        return message_str
