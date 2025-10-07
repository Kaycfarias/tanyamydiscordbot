import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.errors import Forbidden
from discord.ext import commands


class DropdownhelpView(discord.ui.View):
    def __init__(self, bot):
        self.bot = bot
        super().__init__(timeout=190)
        self.add_item(DropdownHelp(self.bot))


class DropdownHelp(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        prefixo = "{" + self.bot.command_prefix + "}"
        options = [
            discord.SelectOption(label=f"Comandos de prefixo {prefixo}", value="prefixo"),
            discord.SelectOption(label="Comandos de barra {/}", value="slash"),
        ]
        super().__init__(
            placeholder="Lista de comandos..",
            custom_id="DropdownHelp",
            min_values=1,
            max_values=1,
            options=options,
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "prefixo":
            embed = discord.Embed(
                title="Lista de comandos",
                description="Lista de comandos por Prefixo ``{prefixo}``",
                color=0x5865F2,
            )
            for cog in self.bot.cogs:
                if cog == "Sync":
                    pass
                else:
                    if len(self.bot.get_cog(cog).get_commands()) > 0:
                        comandos = ""
                        for command in self.bot.get_cog(cog).get_commands():
                            if not command.hidden:
                                parameter = ""
                                for params in command.params:
                                    parameter += f"<{params}> "
                                comandos += f"**{self.bot.command_prefix}{command.name} {parameter}** ➥ {command.description}\n"
                        embed.add_field(name=cog, value=comandos, inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        elif self.values[0] == "slash":
            embed = discord.Embed(
                title="Lista de comandos",
                description="Lista de comandos de aplicativo(slash commands{/})",
                color=0x5865F2,
            )
            for cog in self.bot.cogs:
                if cog in ["Sync", "Setup"]:
                    pass
                else:
                    comandos = ""
                    for command in self.bot.get_cog(cog).walk_app_commands():
                        comandos += f"</{command.qualified_name}:{self.bot.user.id}> ➥ {command.description}\n"
                    for command in self.bot.get_cog(cog).walk_commands():
                        if command.qualified_name not in comandos:
                            comandos += f"</{command.qualified_name}:{self.bot.user.id}> ➥ {command.description}\n"
                    if comandos != "":
                        embed.add_field(name=cog, value=comandos, inline=False)

            await interaction.response.send_message(embed=embed, ephemeral=True)


async def send_embed(ctx, embed, bot):
    try:
        await ctx.send(embed=embed, view=DropdownhelpView(bot))
    except Forbidden:
        try:
            await ctx.send(
                "Opa, parece que eu não posso enviar embeds aqui. Pf verifique minhas permisões :)"
            )
        except Forbidden:
            await ctx.author.send(
                f"Opa, não consegui enviar mensagens em {ctx.channel.name} no servidor {ctx.guild.name}\n"
                f"Pode informar o time do servidor sobre isso?? :slight_smile: ",
                embed=embed,
            )


class Ajuda(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_command(
        aliases=["ajuda"],
        name=_T("help"),
        description=_T("See information about the bot and the list of available commands."),
    )
    async def help(
        self,
        ctx: commands.Context,
    ):
        #    if comando:
        #        embed = discord.Embed(
        #            title=f"ajuda com comando",
        #        )
        #        for cog in self.bot.cogs:
        #            comando_cog = self.bot.get_cog(cog)
        #            for command in comando_cog.walk_app_commands():
        #                result = "\nVocê quis dizer:\n"
        #                if fuzz.ratio(comando, command.qualified_name) > 40:
        #                    result += command.qualified_name + "\n"
        #                if comando == command.qualified_name:
        #                    parameter = ""
        #                    for params in command.parameters:
        #                        parameter += f"<{params}> "
        #                    embed.add_field(
        #                        name="Comando de barra {/}",
        #                        value=f"</{command.qualified_name}:{self.bot.user.id}> {parameter}",
        #                    )
        #            if len(embed.fields) == 0:
        #                if result != "\nVocê quis dizer:\n":
        #                    await ctx.reply(f"Verifique a ortografia{result}")
        #                else:
        #                    await ctx.reply(f"Verifique a ortografia")
        #            else:
        #                await ctx.reply(embed=embed)
        #            return
        embed = discord.Embed(
            title="Painel de ajuda e informações",
            description=f"Olá! Eu sou um bot programado em [Python/discord.py](https://github.com/Rapptz/discord.py) <:python:1122514160870236250> e estou em constante desenvolvimento. Fui criado usando as ferramentas disponíveis com apenas um celular.\nMeu prefixo padrão é **`{self.bot.command_prefix}`**, mas a maioria dos meus comandos só está disponível através de comandos de barra (/). Certifique-se de usar (/) para acessar todos os recursos e funcionalidades que tenho a oferecer.\n\nSe você gostar da minha companhia e quiser me apoiar, por favor, vote em mim através deste link:\n**[Vote em mim](https://top.gg/bot/1103371629117063278/vote)**",
            color=0xFF99EE,
        )
        embed.set_thumbnail(url=self.bot.user.avatar.url if self.bot.user.avatar else None)
        await send_embed(ctx, embed, self.bot)


async def setup(bot: commands.Bot):
    await bot.add_cog(Ajuda(bot))
