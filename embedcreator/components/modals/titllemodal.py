import discord
import validators


class TitleModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Painel de edicão do Título.")
        self.titulo = discord.ui.TextInput(
            label="Título da Embed:",
            placeholder="Defina um título para sua embed...",
            default=self.embed.title,
            style=discord.TextStyle.long,
            required=False,
            max_length=256,
        )
        self.url = discord.ui.TextInput(
            label="Defina o url da embed:",
            placeholder="Insira um url válido para o Título...",
            default=self.embed.url,
            style=discord.TextStyle.short,
            required=False,
        )
        self.add_item(self.titulo)
        self.add_item(self.url)

    async def on_submit(self, interaction: discord.Interaction):
        mess = None
        self.embed.title = self.titulo.value
        if self.url.value is not None and self.url.value.strip() != "":
            if validators.url(self.url.value):
                self.embed.url = self.url.value
            else:
                mess = (
                    "<:error:1116338705955823626> | Sinto muito, a url fornecida não é compatível"
                )
        if mess is None:
            await interaction.response.edit_message(embed=self.embed)
        else:
            await interaction.response.send_message(
                mess, ephemeral=True, delete_after=7)
