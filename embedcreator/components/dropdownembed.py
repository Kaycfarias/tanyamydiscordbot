import discord
from embedcreator.components.buttonview import buttonsView


class dropdownEmbed(discord.ui.Select):
    def __init__(self, embeds, bot, DefaulView):
        self.embeds = embeds
        self.bot = bot
        self.DefaulView = DefaulView
        super().__init__(
            options=[],
            placeholder="Escolha uma embed pra editar")
        self.add_options()

    def add_options(self):
        for i, embed in enumerate(self.embeds):
            label = f"{i + 1} | Título: {embed.title}"
            description = f"Descrição: {embed.description}"
            value = f"{i}"
            if len(label) >= 100:
                label = label[:97] + "..."
            if len(description) >= 100:
                description = description[:97] + "..."
            self.add_option(label=label, description=description, value=value)

    async def callback(self, interaction=discord.Interaction):
        await interaction.response.edit_message(
            embed=self.embeds[int(self.values[0])],
            view=buttonsView(
                int(self.values[0]), self.embeds, self.bot, self.DefaulView),
        )
