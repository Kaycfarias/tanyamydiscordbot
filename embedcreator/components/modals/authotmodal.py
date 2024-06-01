import discord
import validators


class AuthorModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Edite o autor da embed.")
        self.autor = discord.ui.TextInput(
            label="Nome do autor:",
            placeholder="Insira um nome para o autor da embed...",
            default=self.embed.author.name,
            style=discord.TextStyle.short,
            required=False,
            max_length=256,
        )
        self.autorurl = discord.ui.TextInput(
            label="Url do autor:",
            placeholder="Insira um url válido para o nome do author...",
            default=self.embed.author.url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.iconurl = discord.ui.TextInput(
            label="Url do icone do autor:",
            placeholder="Insira um url válido para o icone do autor...",
            default=self.embed.author.icon_url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.add_item(self.autor)
        self.add_item(self.autorurl)
        self.add_item(self.iconurl)

    async def on_submit(self, interaction: discord.Interaction):
        ms = "<:error:1116338705955823626> | Parece que aconteceu um erro:"
        if (
                self.autorurl.value is not None
                and self.autorurl.value.strip() != ""
        ):
            if validators.url(self.autorurl.value):
                autor_url = self.autorurl.value
            else:
                ms += "\nUrl do autor inválido"
                autor_url = None
        else:
            autor_url = None
        if self.iconurl.value is not None and self.iconurl.value.strip() != "":
            if validators.url(self.iconurl.value):
                icon_url = self.iconurl.value
            else:
                icon_url = None
                ms += "\nUrl do icone inválido"
        else:
            icon_url = None
        self.embed.set_author(
            name=self.autor.value, url=autor_url, icon_url=icon_url
        )
        if ms == "<:error:1116338705955823626> | Parece que aconteceu um erro:":
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(
                ms, ephemeral=True, delete_after=7
            )
