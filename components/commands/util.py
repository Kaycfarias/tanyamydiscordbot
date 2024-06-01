import datetime
import typing

import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands


async def apagar(apagadas, quantidade, interaction, limite=None, loops=0):
    if not limite:
        limite = quantidade - apagadas
    apagadas += len(
        await interaction.channel.purge(
            limit=limite,
            check=lambda m: interaction.message.id != m.id,
        )
    )
    loops += 1
    if apagadas >= quantidade or loops == 15:
        return apagadas
    else:
        return await apagar(apagadas, quantidade, interaction, (quantidade - apagadas) + 1, loops)


async def apagar_membro(membro_id, apagadas, quantidade, interaction, limite=None, loops=0):
    def check_member(m):
        if m.author.id == membro_id:
            if interaction.message.id != m.id:
                return True

    if not limite:
        limite = quantidade - apagadas
    apagadas += len(
        await interaction.channel.purge(
            limit=limite,
            check=check_member,
        )
    )
    loops += 1
    if apagadas >= quantidade or loops == 25:
        return apagadas
    else:
        return await apagar_membro(
            membro_id, apagadas, quantidade, interaction, (quantidade - apagadas) + 1, loops
        )


class Utilidades(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.guild_only()
    @commands.bot_has_permissions(manage_messages=True)
    @commands.cooldown(1, 25, commands.BucketType.user)
    @commands.hybrid_command(
        name=_T("clear"), description=_T("[Moderation] Clear chat messages."), aliases=["limpar"]
    )
    @app_commands.describe(quantidade=_T("Please enter the number of messages to be deleted."))
    async def limpar(
        self, interaction: commands.Context, quantidade: int, membro: discord.Member = None
    ):
        if interaction.author.guild_permissions.manage_messages:
            if quantidade <= 0 or quantidade > 100:
                await interaction.reply(
                    "O número de mensagens a serem excluídas deve estar entre 1 e 100.",
                    ephemeral=True,
                )
                return
            message = await interaction.typing()
            try:
                await message.delete()
            except AttributeError:
                pass
            if membro:
                limpas = await apagar_membro(membro.id, 0, quantidade, interaction)
                await interaction.channel.send(
                    f"{interaction.author.mention} excluiu as últimas {limpas} mensagens de {membro.mention} em {interaction.channel.mention}"
                )
            else:
                limpas = await apagar(0, quantidade, interaction)
                await interaction.channel.send(
                    f"{interaction.author.mention} excluiu as últimas {limpas} mensagens em {interaction.channel.mention}"
                )
        else:
            await interaction.reply(
                f":lock:Permissão negada.\nVoce precisa da permisão: gerenciar mensagens!!",
                ephemeral=True,
                delete_after=60,
            )

    @commands.hybrid_command(name="ping", description=_T("Bot Latency"))
    async def ping(self, interaction: commands.Context):
        start_time = discord.utils.utcnow()
        message = await interaction.reply(":satellite: **Pong!**")
        end_time = discord.utils.utcnow()
        api_latency = round((end_time - start_time).total_seconds() * 1000)
        gateway_latency = round(self.bot.latency * 1000)
        await message.edit(
            content=f":satellite: **Pong!**\n**Latência da API:** {api_latency} ms\n**Latência do Gateway:** {gateway_latency} ms"
        )

    @commands.guild_only()
    @commands.hybrid_command(name=_T("say"), description=_T("[Misc] May I speak?"))
    @app_commands.describe(mensagem=_T("Tell me what to say."))
    async def say(
        self,
        interaction: commands.Context,
        mensagem: str,
        *,
        arquivo: typing.Optional[discord.Attachment] = None,
    ):
        if interaction.author.guild_permissions.manage_messages:
            if arquivo:
                arquivo = await arquivo.to_file()
                await interaction.reply(mensagem, file=arquivo)
            else:
                await interaction.reply(mensagem)
        else:
            await interaction.reply(
                f":lock:Permissão negada.\nVoce precisa da permisão gerenciar mensagens!!",
                ephemeral=True,
                delete_after=60,
            )

    @commands.guild_only()
    @commands.bot_has_permissions(manage_channels=True)
    @commands.hybrid_command(
        name=_T("slowmode"),
        description=_T("[Utilities] Enable slow mode in a channel"),
        aliases=["modolento", "modo_lento", "slow_mode"],
    )
    @app_commands.describe(
        duration=_T("Enter the desired duration:"),
        channel=_T("Select a channel:"),
        unit=_T("Select the time unit:"),
    )
    @app_commands.choices(
        unit=[
            app_commands.Choice(name=_T("Second(s)"), value="s"),
            app_commands.Choice(name=_T("Minute(s)"), value="m"),
            app_commands.Choice(name=_T("Hour(s)"), value="h"),
        ]
    )
    async def slowmode(
        self,
        inter: commands.Context,
        duration: int,
        unit: str,
        channel: discord.TextChannel = None,
    ):
        if inter.author.guild_permissions.manage_channels:
            casos = [
                "seconds",
                "segundos",
                "s",
                "segs",
                "minutes",
                "minutos",
                "m",
                "mins",
                "hours",
                "horas",
                "h",
            ]
            if not channel:
                channel = inter.channel
            if unit in [casos[0], casos[1], casos[2], casos[3]]:
                string_formated = f"{duration} segundo{'s' if duration > 1 else ''}"
            elif unit in [casos[4], casos[5], casos[6], casos[7]]:
                duration *= 60
                m = (duration // 60) % 60
                string_formated = f"{m} minuto{'s' if m > 1 else ''}"
            elif unit in [casos[8], casos[9], casos[10]]:
                duration *= 3600
                h = duration // 3600
                string_formated = f"{h} hora{'s' if h > 1 else ''}"
            else:
                return await inter.reply(
                    "<:error:1116338705955823626> | Por favor, escolha uma unidade de tempo válida dentre as opções disponíveis. (horas, minutos ou segundos)"
                )
            if duration > 21600:
                return await inter.reply(
                    "<:error:1116338705955823626> | O modo lento não pode exceder 6 horas."
                )
            await channel.edit(slowmode_delay=duration)
            if duration > 0:
                await inter.reply(
                    f"🐢|Modo lento de **{string_formated}** foi aplicado em {channel.mention}"
                )
            else:
                await inter.reply(f"🐢|Modo lento desativado em {channel.mention}")
        else:
            await inter.reply(
                f":lock:Permissão negada.\nVoce precisa da permisão gerenciar canais!!",
                ephemeral=True,
                delete_after=60,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Utilidades(bot))
