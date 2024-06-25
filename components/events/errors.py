import discord
from discord.ext import commands


class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

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
            for perm in error.missing_permissions:
                permissões = ""
                if perm != error.missing_permissions[len(error.missing_permissions) - 1]:
                    permissões += perm + ", "
                else:
                    permissões += perm
            em = discord.Embed(
                title="<:error:1116338705955823626> | Por favor, conceda-me as permissões necessárias.",
                description=f"Antes de tentar o comando novamente, certifique-se de que eu possua as permissões necessárias. Você pode seguir o conjunto de permissões e pedir a um moderador para conceder as permissão(ões): **{permissões}** a mim.",
                color=0xFF9090,
            )
        else:
            em = discord.Embed(
                title="<:error:1116338705955823626> | Erro",
                description=f"Sinto muito, um erro aconteceu inexperado, o desenvolvedor ja foi informado",
                color=0xFF9090,
            )
            dono = self.bot.get_user(597216735984091137)
            await dono.create_dm()
            await dono.send(
            	embed=discord.Embed(
            	title="Um erro aconteceu",
            	description=f"```{error}```\nserver: {ctx.guild} - {ctx.channel}\nUsuario: {ctx.author} - {ctx.author.mention}\nComando:{ctx.command}\nConteudo da mensagem{ctx.message.content[200:]}",
               	 )
          	 )
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


async def setup(bot: commands.Bot):
    await bot.add_cog(Errors(bot))
