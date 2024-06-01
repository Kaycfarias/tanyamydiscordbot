import discord


class DescriptionModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Painel de edicão da Descrição.")
        self.desc = discord.ui.TextInput(
            label="Descrição da embed...",
            placeholder="Insira a descrição da embed...",
            default=self.embed.description,
            style=discord.TextStyle.paragraph,
            required=False,
        )
        self.add_item(self.desc)

    async def on_submit(self, interaction: discord.Interaction):
        self.embed.description = self.desc.value

        await interaction.response.edit_message(embed=self.embed)
