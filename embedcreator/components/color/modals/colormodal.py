import discord


class ColorModal(discord.ui.Modal):
    def __init__(self, index, embeds):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(title="Escolha a cor da embed.")
        self.cor = discord.ui.TextInput(
            label="Cor da Embed em HEX: Exemplo: #ff0000",
            placeholder="Insira uma cor válida em código HEX...",
            default=f"#{self.embed.colour.value:06x}",
            style=discord.TextStyle.short,
        )
        self.add_item(self.cor)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            int_color = int(self.cor.value[1:], 16)
            self.embed.color = int_color
            await interaction.response.edit_message(embed=self.embed)
        except Exception:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Insira um código HEX válido por favor",
                ephemeral=True,
                delete_after=7,
            )
