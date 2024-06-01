import discord
import validators


class FooterModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Edite o rodapé.")
        self.rodape = discord.ui.TextInput(
            label="Nome do rodapé da embed:",
            placeholder="Insira um nome para o rodapé da embed...",
            default=self.embed.footer.text,
            style=discord.TextStyle.short,
            required=False,
        )
        self.url = discord.ui.TextInput(
            label="Imagem no rodapé:",
            placeholder="Insira um url válido para a imagem no rodapé da embed...",
            default=self.embed.footer.icon_url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.add_item(self.rodape)
        self.add_item(self.url)

    async def on_submit(self, interaction: discord.Interaction):
        icon_url_rodape = None
        messa = "<:error:1116338705955823626> | Parece que aconteceu um erro:"
        if self.url.value is not None and self.url.value.strip() != "":
            if validators.url(self.url.value):
                icon_url_rodape = self.url
            else:
                messa += "\nUrl da imagem do rodape inválido"
        if messa == "<:error:1116338705955823626> | Parece que aconteceu um erro:":
            self.embed.set_footer(text=self.rodape.value,
                                  icon_url=icon_url_rodape)
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(messa, ephemeral=True, delete_after=7)
