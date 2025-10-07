import discord
from discord.ext import commands
from discord import app_commands
from discord.app_commands import locale_str as _T
import logging


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)

    @commands.Cog.listener()
    async def on_command_error(self, ctx: commands.Context, error):
        print(error)
        if isinstance(error, commands.errors.CommandNotFound):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Não encontrei esse comando",
                description="Lamento, mas não parece que esse comando esteja na minha lista, consulte todos os meus comandos </ajuda:1>.",
                color=0xFF9090,
            )
        elif isinstance(error, commands.errors.PartialEmojiConversionFailure):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Emoji incompatível",
                description=f"Desculpe, mas o emoji '**{error.argument}**' não é compativel.",
                color=0xFF9090,
            )
        elif isinstance(error, commands.errors.MissingRequiredArgument):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Hum..., parece que esta faltando algo",
                description=f"Percebi que o argumento obrigatório '**{error.param.name}**' está faltando no comando. Por gentileza, forneça o argumento necessário para que o comando funcione conforme o esperado.\nUse </ajuda:{self.bot.user.id}>",
                color=0xFF9090,
            )

        elif isinstance(error, commands.CommandOnCooldown):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Calma ai amigão!",
                description=f"Tente novamente em {error.retry_after:.2f}s.",
                color=0xFF9090,
            )

        elif isinstance(error, commands.errors.MemberNotFound):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Membro não encontrado",
                description=f"Não foi possivel encontrar o membro: **{error.argument}**, forneça a mencão ou id",
                color=0xFF9090,
            )

        elif isinstance(error, commands.errors.BotMissingPermissions):
            # Corrigir o bug na formatação de permissões
            permissões = ", ".join(error.missing_permissions)
            em = discord.Embed(
                title="<:error:1116338705955823626> | Por favor, conceda-me as permissões necessárias.",
                description=f"Antes de tentar o comando novamente, certifique-se de que eu possua as permissões necessárias. Você pode seguir o conjunto de permissões e pedir a um moderador para conceder as permissão(ões): **{permissões}** a mim.",
                color=0xFF9090,
            )
        else:
            em = discord.Embed(
                title="<:error:1116338705955823626> | Erro",
                description=f"Sinto muito, um erro aconteceu inesperado, o desenvolvedor já foi informado",
                color=0xFF9090,
            )
            # Logging estruturado para debugging
            self.logger.error(f"Erro inesperado no comando: {error}", extra={
                "guild": ctx.guild.id if ctx.guild else None,
                "guild_name": ctx.guild.name if ctx.guild else "DM",
                "channel": ctx.channel.id,
                "user": ctx.author.id,
                "username": str(ctx.author),
                "command": str(ctx.command),
                "message_content": ctx.message.content[:200],
                "error_type": type(error).__name__
            })
        try:
            await ctx.reply(embed=em)
        except discord.errors.Forbidden:
            try:
                await ctx.author.create_dm()
            except discord.errors.Forbidden:
                pass
            finally:
                await ctx.author.send(
                    embed=discord.Embed(
                        title="<:error:1116338705955823626> | Por favor, conceda-me as permissões necessárias.",
                        description=f"Oops, parece que não tenho permissão para enviar mensagens em {ctx.channel.mention} no servidor `{ctx.guild.name}` porque não possuo as permissões necessárias.\nPor favor, informe a equipe do servidor sobre isso. 🙂",
                        color=0xFF9090,
                    )
                )

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        """Trata erros de slash commands."""
        
        # Log do erro para debugging
        self.logger.error(f"App command error: {error}", extra={
            "guild": interaction.guild_id,
            "channel": interaction.channel_id,
            "user": interaction.user.id,
            "command": interaction.command.name if interaction.command else "Unknown"
        })
        
        if isinstance(error, app_commands.CommandOnCooldown):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Calma aí amigão!",
                description=f"Tente novamente em {error.retry_after:.2f}s.",
                color=0xFF9090,
            )
        elif isinstance(error, app_commands.MissingPermissions):
            permissões = ", ".join(error.missing_permissions)
            em = discord.Embed(
                title="<:error:1116338705955823626> | Você não tem permissão",
                description=f"Você precisa das seguintes permissões: **{permissões}**",
                color=0xFF9090,
            )
        elif isinstance(error, app_commands.BotMissingPermissions):
            permissões = ", ".join(error.missing_permissions)
            em = discord.Embed(
                title="<:error:1116338705955823626> | Por favor, conceda-me as permissões necessárias.",
                description=f"Eu preciso das seguintes permissões: **{permissões}**",
                color=0xFF9090,
            )
        elif isinstance(error, app_commands.NoPrivateMessage):
            em = discord.Embed(
                title="<:error:1116338705955823626> | Comando apenas para servidores",
                description="Este comando só pode ser usado em servidores, não em mensagens privadas.",
                color=0xFF9090,
            )
        else:
            em = discord.Embed(
                title="<:error:1116338705955823626> | Erro",
                description="Sinto muito, um erro inesperado aconteceu, o desenvolvedor já foi informado",
                color=0xFF9090,
            )
        
        # Tentar responder à interação
        try:
            if interaction.response.is_done():
                await interaction.followup.send(embed=em, ephemeral=True)
            else:
                await interaction.response.send_message(embed=em, ephemeral=True)
        except discord.errors.Forbidden:
            # Se não conseguir responder, tentar mandar DM
            try:
                await interaction.user.send(embed=em)
            except discord.errors.Forbidden:
                pass  # Se não conseguir mandar DM, não há mais o que fazer


async def setup(bot: commands.Bot):
    await bot.add_cog(Errors(bot))
