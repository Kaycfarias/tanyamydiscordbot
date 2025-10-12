

import aiohttp
import discord
import traceback

from dotenv import dotenv_values
from discord import app_commands
from discord.ext import commands

async def responder(message: discord.Message, pergunta, bot):
    if message.author.id in Chatgpt.resposta_andamento:
        em = discord.Embed(
            title="<:error:1116338705955823626> | Em andamento",
            description="Uma pergunta está em processo. Por favor, aguarde um momento enquanto trabalho nisso. Agradeço a sua paciência!",
            color=0xFF9090,
        )
        return await message.reply(embed=em)
    await message.add_reaction("<a:loading_thp:1133025100564811776>")
    await message.channel.typing()
    response = await Chatgpt.response(pergunta, message.author.id)
    if response:
        if len(response) >= 2000:
            await message.reply(
                response[:2000],
                view=BotaoContinueView(response[2000:], message.author),
                embed=discord.Embed(
                    description="Sua resposta ficou muito longa, mas não se preucupe, vc pode continua-la clicando no botao abaixo",
                    color=0xF1C40F,
                ),
            )
        else:
            await message.reply(response, view=BotaoContinueView(None, message.author))
    else:
        await message.reply(
            embed=discord.Embed(
                description="Desculpe, ocorreu um erro ao processar sua solicitação. Verifique os dados fornecidos e tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte para obter assistência.",
                color=0xFF0000,
            )
        )
    await message.remove_reaction("<a:loading_thp:1133025100564811776>", bot.user)


class ClientChatGpt:
    def __init__(self, api_key=None):
        self.sessions = {}
        self.resposta_andamento = []
        self.api_key = api_key

    def create_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = {
                "model": "gpt-5",
                "messages": [
                    {
                        "role": "system",
                        "content": "You are a helpful assistant designed to be used on Discord servers, named Pix-e, Developed by @k4yc and using the ChatGPT artificial intelligence.",
                    },
                ],
            }

    def delete_session(self, user_id):
        if user_id in self.sessions:
            del self.sessions[user_id]
            return True
        else:
            return False

    async def response(self, user_input, user_id, tentativas=0):
        if user_id not in self.sessions:
            self.create_session(user_id)
        if user_id not in self.resposta_andamento:
            self.resposta_andamento.append(user_id)
        api_url = "https://api.openai.com/v1/chat/completions"
        #api_url = "https://free.churchless.tech/v1/chat/completions"
        headers = {
			"Authorization": f'Bearer {self.api_key}',
			"Content-Type": "application/json"}

        payload = {
            "model": self.sessions[user_id]["model"],
            "messages": [
                *self.sessions[user_id]["messages"],
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
            "temperature": 0.7,
        }
        try:
            async with aiohttp.ClientSession() as session, session.post(
                api_url, headers=headers, json=payload, timeout=120
            ) as response:
                if response:
                    data = await response.json()
                elif not response or tentativas <= 5:
                    tentativas+1
                    print('Tentando novamente')
                    return self.response(user_input, user_id, tentativas)
                else:
                    self.resposta_andamento.remove(user_id)
                    return None
        except aiohttp.ClientError as e:
            if tentativas < 5:
                tentativas+=1
                traceback.print_exc()
                return await self.response(user_input, user_id, tentativas)
            else:
                self.resposta_andamento.remove(user_id)
                return None
            
        print(f'chat error = {data}')
        if "choices" in data:
            self.sessions[user_id]["messages"].append(
                {"role": "assistant", "content": data["choices"][0]["message"]["content"]}
            )
            self.resposta_andamento.remove(user_id)
            return data["choices"][0]["message"]["content"]

        self.resposta_andamento.remove(user_id)
        return None


Chatgpt = ClientChatGpt()


class BotaoContinueView(discord.ui.View):
    def __init__(self, resp, user):
        super().__init__(timeout=600)
        self.resp = resp
        self.user = user
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "gptuser":
                    child.label = f"@{self.user.name}"
        if not self.resp:
            self.disable_button()

    def disable_button(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "gpt":
                    self.remove_item(child)

    @discord.ui.button(
        style=discord.ButtonStyle.success, label="Continuar", emoji="📃", custom_id="gpt"
    )
    async def on_resp(self, inter, button):
        if self.user.id == inter.user.id:
            self.stop()
            if len(self.resp) > 2000:
                await inter.response.send_message(
                    self.resp[:2000],
                    view=BotaoContinueView(self.resp[2000:], self.user),
                    embed=discord.Embed(
                        description="Sua resposta está muito longa, mas não se preocupe, você pode continuar clicando no botão abaixo.",
                        color=0xF1C40F,
                    ),
                )
            else:
                await inter.response.send_message(
                    self.resp, view=BotaoContinueView(None, self.user)
                )
                self.stop()
        else:
            await inter.response.send_message("Essa conversa não é sua", ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="Opções do ChatGPT",
        emoji="<:engrenagem:1107280634952552580>",
        custom_id="opcoes",
    )
    async def on_op(self, inter, button):
        await inter.response.send_message(view=BotaoConfigView(), ephemeral=True)

    @discord.ui.button(
        style=discord.ButtonStyle.grey,
        label="name",
        emoji="👤",
        custom_id="gptuser",
        disabled=True,
    )
    async def user(self, inter, button):
        pass


class BotaoConfigView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=600)

    @discord.ui.button(
        style=discord.ButtonStyle.red,
        label="Limpar sessão",
        emoji="<:lixo:1105962772543574206>",
        custom_id="chathis",
    )
    async def on_resp(self, inter, button):
        clear = Chatgpt.delete_session(inter.user.id)
        if clear:
            await inter.response.send_message("Sessão esquecida", ephemeral=True, delete_after=5)
        else:
            await inter.response.send_message(
                "Não encontrei uma sessão com você", ephemeral=True, delete_after=5
            )

    @discord.ui.select(
        custom_id="select",
        placeholder="Personalidade",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(
                label="Neutra",
                value="1",
                description="Personalidade padrão",
                emoji="😐",
            ),
            discord.SelectOption(
                label="Prestativa",
                value="2",
                description="Sua assistente prestativa",
                emoji="🙌",
                default=True,
            ),
            discord.SelectOption(
                label="Precisa", value="3", description="Precisa e direta ao ponto", emoji="📜"
            ),
        ],
    )
    async def on_per(self, inter, select: discord.ui.Select):
        if inter.user.id not in Chatgpt.sessions:
            Chatgpt.create_session(inter.user.id)
        for message in Chatgpt.sessions[inter.user.id]["messages"]:
            if message["role"] == "system":
                if select.values[0] == "1":
                    message[
                        "content"
                    ] = "You are a assistant designed to be used on Discord servers, named Pix-e, Developed by @k4yc and using the ChatGPT artificial intelligence."
                elif select.values[0] == "2":
                    message[
                        "content"
                    ] = "You are a assistant designed to be used on Discord servers, named Pix-e, Developed by @k4yc and using the ChatGPT artificial intelligence. your personality is Helpful and visible in conversation"

                elif select.values[0] == "3":
                    message[
                        "content"
                    ] = "You are a assistant designed to be used on Discord servers, named Pix-e, Developed by @k4yc and using the ChatGPT artificial intelligence. your personality is is from someone with precise and straight to the point answers to the pointand visible in conversation"
                elif select.values[0] == "4":
                    message[
                        "content"
                    ] = "You are a assistant designed to be used on Discord servers, named Pix-e, Developed by @k4yc and using the ChatGPT artificial intelligence. you are anime character"
        await inter.response.send_message(
            f"Nova Personalidade. Para esquecer a personalidade anterior é necessario limpar a sessão",
            ephemeral=True,
            delete_after=10,
        )


class gpt(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # Inicializar o ClientChatGpt com a chave do bot
        global Chatgpt
        Chatgpt = ClientChatGpt(api_key=bot.chatgpt_key)

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        elif message.content == self.bot.user.mention:
            await message.reply(
                f"salve {message.author.mention}!!, o meu prefixo nesse nervidor é ``{self.bot.command_prefix}``, use </ajuda:{self.bot.user.id}> ou ``{self.bot.command_prefix}ajuda`` para obter informacães"
            )
        # elif message.reference:
        #    if message.reference.cached_message:
        #        if message.reference.cached_message.author.id == self.bot.user.id:
        #            await responder(
        #                message, message.content.removeprefix(self.bot.user.mention), self.bot
        #            )
        # elif self.bot.user.mentioned_in(message):
        #    await responder(message, message.content.removeprefix(self.bot.user.mention), self.bot)

        elif isinstance(message.channel, discord.DMChannel) and not message.content.startswith(
            self.bot.command_prefix
        ):
            await responder(message, message.content.removeprefix(self.bot.user.mention), self.bot)
            await self.bot.process_commands(message)

    @commands.bot_has_permissions(send_messages=True)
    @commands.hybrid_command(name="chat", description="Use a incrivel IA chatgpt")
    @app_commands.describe(pergunta="Faça um pergunta...")
    async def chat(self, ctx: commands.Context, *, pergunta: str):
        if ctx.author.id in Chatgpt.resposta_andamento:
            em = discord.Embed(
                title="<:error:1116338705955823626> | Em andamento",
                description="Uma pergunta está em processo. Por favor, aguarde um momento enquanto trabalho nisso. Agradeço a sua paciência!",
                color=0xFF9090,
            )
            return await ctx.reply(embed=em)
        try:
            await ctx.message.add_reaction("<a:loading_thp:1133025100564811776>")
        except Exception:
            pass
        await ctx.typing()
        response = await Chatgpt.response(pergunta, ctx.author.id)
        if response:
            if len(response) >= 2000:
                await ctx.reply(
                    response[:2000],
                    view=BotaoContinueView(response[2000:], ctx.author),
                    embed=discord.Embed(
                        description="Sua resposta ficou muito longa, mas não se preucupe, vc pode continua-la clicando no botao abaixo",
                        color=0xF1C40F,
                    ),
                )
            else:
                await ctx.reply(response, view=BotaoContinueView(None, ctx.author))
        else:
            await ctx.reply(
                embed=discord.Embed(
                    title="<:error:1116338705955823626> | Erro",
                    description="Desculpe, ocorreu um erro ao processar sua solicitação. Verifique os dados fornecidos e tente novamente mais tarde. Se o problema persistir, entre em contato com o suporte para obter assistência.",
                    color=0xFF9090,
                )
            )
        try:
            await ctx.message.remove_reaction("<a:loading_thp:1133025100564811776>", self.bot.user)
        except Exception:
            return None


async def setup(bot: commands.Bot):
    await bot.add_cog(gpt(bot))
