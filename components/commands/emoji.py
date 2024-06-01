import discord
from discord import app_commands
from discord.ext import commands


@commands.guild_only()
class Emoji(commands.GroupCog, group_name="emoji"):
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------comandos---------------------------#
    @commands.bot_has_permissions(manage_emojis=True)
    @commands.hybrid_command(name="criar", description="[útilidades] crie um emoji personalizado")
    @app_commands.describe(
        nome="pelo menos 2 carácteres e só podem conter carácteres alfanuméricos e underline",
        arquivo="PNG, JPEG, JPG E GIF; limite de 256kb por arquivo",
    )
    async def emoji(self, interaction: commands.Context, nome: str, arquivo: discord.Attachment):
        if interaction.author.guild_permissions.manage_emojis:
            if arquivo.filename.lower().endswith((".png", ".jpeg", ".gif", "jpg")):
                if arquivo.size > 256000:
                    await interaction.reply(
                        "O tamanho do arquivo excedeu o limite máximo de 256 KB."
                    )
                else:
                    interaction.typing()
                    if len(interaction.guild.emojis) < interaction.guild.emoji_limit:
                        try:
                            arquivo = await arquivo.read()
                            emoji = await interaction.guild.create_custom_emoji(
                                name=nome, image=arquivo
                            )
                            embed = discord.Embed(
                                title="emoji adicionado",
                                description=f"{emoji} | O emoji foi adicionado com sucesso!",
                                color=0x7575FF,
                            )
                            embed.set_thumbnail(url=emoji.url)
                            embed.set_footer(text=f"<{emoji.name}:{emoji.id}>")
                            await interaction.reply(embed=embed)
                        except discord.Forbidden:
                            await interaction.reply("Não tenho permissão para adicionar emojis.")
                    else:
                        await interaction.reply("O servidor ja chegou ao limite maximo de emojis.")
            else:
                await interaction.reply("por favor envie uma arquivo png, jpel ou gif")
        else:
            await interaction.reply(
                ":lock:Permissão negada.\nVoce precisa da permisão: gerenciar emojis e figurinhas!!",
                ephemeral=True,
                delete_after=30,
            )

    @commands.bot_has_permissions(manage_emojis=True)
    @commands.hybrid_command(
        name="copiar", description="[útilidades] Copie e adcione o emoji no servidor atual"
    )
    @app_commands.describe(emoji="Mencione o emoji personalizado...")
    async def copiar_emoji(self, interaction: commands.Context, emoji: discord.PartialEmoji):
        if interaction.author.guild_permissions.manage_emojis:
            if len(interaction.guild.emojis) < interaction.guild.emoji_limit:
                try:
                    nome_emoji = emoji.name
                    imagem_emoji = await emoji.read()
                    emoji_copiado = await interaction.guild.create_custom_emoji(
                        name=nome_emoji, image=imagem_emoji
                    )
                    embed = discord.Embed(
                        title="emoji foi copiado",
                        description=f"O emoji {emoji_copiado} foi copiado para o servidor {interaction.guild.name}.",
                        color=0xFF0000,
                    )
                    embed.set_thumbnail(url=emoji_copiado.url)
                    embed.set_footer(text=f"\{emoji_copiado}")
                    await interaction.reply(embed=embed)
                except:
                    await interaction.reply(f"Não consegui encontrar esse emoji", ephemeral=True)
            else:
                await interaction.reply("O servidor ja chegou ao limite maximo de emojis.")
        else:
            await interaction.reply(
                ":lock:Permissão negada.\nVoce precisa da permisão: gerenciar emojis e figurinhas!!",
                ephemeral=True,
                delete_after=30,
            )

    @commands.hybrid_command(
        name="info", description="[útilidades] Veja as informações de um emoji"
    )
    @app_commands.describe(emoji="Mencione o emoji personalizado...")
    async def info_emoji(self, interaction: commands.Context, emoji: discord.PartialEmoji):
        embed = discord.Embed(
            title=f"Informações do emoji {emoji}",
            color=0xFF0000,
        )
        embed.add_field(name="Nome do emoji:", value=f"{emoji.name}")
        embed.add_field(name="id:", value=f"``{emoji.id}``")
        embed.add_field(name="mencão:", value=f"```{emoji}```")
        criado = int(emoji.created_at.timestamp())
        embed.add_field(name="criado em:", value=f"<t:{criado}:D>")
        embed.set_thumbnail(url=emoji.url)
        await interaction.reply(embed=embed)


# -------------------------------------------------------------#
async def setup(bot: commands.Bot):
    await bot.add_cog(Emoji(bot))
