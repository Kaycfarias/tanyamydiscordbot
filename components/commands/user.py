import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands


@commands.bot_has_permissions(read_messages=True, send_messages=True)
@commands.guild_only()
class User(commands.GroupCog, group_name=_T("user")):
    def __init__(self, bot):
        self.bot = bot

    # ---------------------------comandos---------------------------#

    @commands.hybrid_command(name="avatar", description=_T("[Utilities] View a user's avatar..."))
    async def on_avatar(self, interaction: commands.Context, *, user: discord.User = None):
        if not user:
            user = interaction.author
        embed = discord.Embed(title=f"{user.mention} Avatar...", color=discord.Color.random())
        url = user.default_avatar.url if user.avatar is None else user.avatar.url
        if not user.guild_avatar:
            embed.set_image(url=url)
            view = AvatarView(
                user,
                url,
                embed,
            )
        else:
            embed.set_image(url=user.guild_avatar.url)
            embed.set_thumbnail(url=url)
            view = AvatarView(user, user.guild_avatar.url, embed)
        if user.avatar is not None:
            await interaction.reply(embed=embed, view=view)
        else:
            await interaction.reply(
                embed=embed,
            )

    @commands.hybrid_command(
        name="banner", description=_T("[Utilities] View a user's profile banner...")
    )
    async def on_banner(self, interaction: commands.Context, *, user: discord.User = None):
        if user is None:
            user = interaction.author
        user = await self.bot.fetch_user(user.id)
        if user.banner:
            embed = discord.Embed(title=f"{user.mention} banner", color=discord.Color.random())
            embed.set_image(url=user.banner.url)
            await interaction.reply(embed=embed)
        else:
            await interaction.reply(
                "Desculpe, este usuário ainda não possui um banner de perfil definido.",
                ephemeral=True,
            )


class AvatarView(discord.ui.View):
    def __init__(self, membro, url, embed):
        self.url = url
        self.membro = membro
        self.embed = embed
        super().__init__(timeout=190)
        if self.embed.image.url != self.url:
            self.url_ava_button()
        else:
            if self.membro.guild_avatar:
                pass
            else:
                self.url_ava_off()

        button = discord.ui.Button(
            label="ver no navegador", style=discord.ButtonStyle.url, url=self.url
        )
        self.add_item(button)

    def url_ava_button(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttonavatar":
                    child.label = "Ver avatar do servidor usuário"

    def url_ava_off(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttonavatar":
                    self.remove_item(child)

    @discord.ui.button(
        label="Ver avatar global do usuário",
        style=discord.ButtonStyle.blurple,
        custom_id="buttonavatar",
    )
    async def on_button_avatar(self, interaction: discord.Interaction, button: discord.Button):
        if self.embed.image.url != self.membro.avatar.url:
            url = self.membro.avatar.url
            self.embed.set_thumbnail(url=self.membro.guild_avatar.url)
            self.embed.set_image(url=self.membro.avatar.url)
        else:
            url = self.membro.guild_avatar.url
            self.embed.set_thumbnail(url=self.membro.avatar.url)
            self.embed.set_image(url=url)
        await interaction.response.edit_message(
            embed=self.embed, view=AvatarView(self.membro, url, self.embed)
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(User(bot))
