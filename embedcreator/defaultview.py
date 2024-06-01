import discord
from embedcreator.components.dropdownembed import dropdownEmbed
from embedcreator.components.finalysend.finalysendview import finalySendView

# Esta é a "view" padrão
class defaultView(discord.ui.View):
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(dropdownEmbed(self.embeds, self.bot, defaultView))
        if len(self.embeds) == 10:
            self.disable_button()

    def disable_button(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttonembedadd":
                    child.disabled = True

    @discord.ui.button(
        label="Adcionar embed",
        style=discord.ButtonStyle.blurple,
        emoji="<:adicionar:1105963449491665016>",
        custom_id="buttonembedadd",
        row=1,
    )
    async def on_add(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embeds.append(
            discord.Embed(title="título", description="Descrição",
                          colour=discord.Colour.random())
        )
        await interaction.response.edit_message(
            embeds=self.embeds, view=defaultView(self.embeds, self.bot)
        )

    @discord.ui.button(
        label="Finalizar",
        style=discord.ButtonStyle.green,
        emoji="<:enviar:1105962897768726650>",
        custom_id="buttonfinalizar",
        row=1,
    )
    async def on_finalizar(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=finalySendView(self.embeds, self.bot, defaultView))
