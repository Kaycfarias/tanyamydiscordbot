import discord
import validators


class ImageModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Edite a imagens da embed.")
        self.imagem = discord.ui.TextInput(
            label="Imagem da embed:",
            placeholder="Insira um url válido para a imagem da embed...",
            default=self.embed.image.url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.thumb = discord.ui.TextInput(
            label="Thumbnail da embed:",
            placeholder="Insira um url válido para a thumbnail da embed...",
            default=self.embed.thumbnail.url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.add_item(self.imagem)
        self.add_item(self.thumb)

    async def on_submit(self, interaction: discord.Interaction):
        messa = "<:error:1116338705955823626> | Parece que aconteceu um erro:"
        if self.imagem.value is not None and self.imagem.value.strip() != "":
            if validators.url(self.imagem.value):
                self.embed.set_image(url=self.imagem)
            else:
                messa += "\nUrl da imagem inválido"
        else:
            self.embed.set_image(url=None)
        if self.thumb.value is not None and self.thumb.value.strip() != "":
            if validators.url(self.thumb.value):
                self.embed.set_thumbnail(url=self.thumb)
            else:
                messa += "\nUrl da thumbnail inválido"
        else:
            self.embed.set_thumbnail(url=None)
        if messa == "<:error:1116338705955823626> | Parece que aconteceu um erro:":
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(messa, ephemeral=True, delete_after=7)
