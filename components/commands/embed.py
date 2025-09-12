import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from embedcreator.defaultview import defaultView


@commands.bot_has_permissions(send_messages=True)
@app_commands.guild_only()
class Embed(commands.GroupCog, name="embed", description=_T("[utilities] Commands for creating embeds")):
    def __init__(self, bot):
        self.bot = bot

    criar = app_commands.Group(
        name=_T("create"), description=_T("criação de embeds"))

    @criar.command(
        name=_T("advanced"), description=_T("[utilities] Open advanced menu for creating embeds")
    )
    @app_commands.describe(
        copy=_T("Provide the link of the message containing the embed to be copied")
    )
    async def on_criar_embed(self, interaction: discord.Interaction, copy: str = None):
        if interaction.user.guild_permissions.manage_guild:
            if copy:
                try:
                    channel_id, message_id = copy.split("/")[-2:]
                    channel = self.bot.get_channel(int(channel_id))
                    target_message = await channel.fetch_message(message_id)
                    embeds = target_message.embeds
                except:
                    await interaction.response.send_message(
                        "<:error:1116338705955823626> | Não consegui encontrar essa mensagem",
                        ephemeral=True,
                        delete_after=30,
                    )
                    return
            else:
                embeds = [
                    discord.Embed(
                        title="Título", description="Descrição", colour=discord.Colour.random()
                    )
                ]
            await interaction.response.send_message(
                embeds=embeds, view=defaultView(embeds, self.bot), ephemeral=True
            )
        else:
            await interaction.response.send_message(
                ":lock:Permissão negada.\nComando restrito a moderadores!",
                ephemeral=True,
                delete_after=20,
            )


async def setup(bot: commands.Bot):
    await bot.add_cog(Embed(bot))
