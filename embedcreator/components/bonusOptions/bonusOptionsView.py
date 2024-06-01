import discord
import json

from embedcreator.components.bonusOptions.modals.copymodal import copyModal
from embedcreator.components.bonusOptions.modals.jsonmodal import jsonModal


class bonusOptionsView(discord.ui.View):
    def __init__(self, index, embeds, bot,
                 defaultView, buttonsView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.embed = self.embeds[self.index]
        self.defaultView = defaultView
        self.buttonsView = buttonsView
        super().__init__(timeout=None)

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltarextras",
        row=0,
    )
    async def on_voltar5(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=self.buttonsView(self.index, self.embeds, self.bot, self.defaultView))

    @discord.ui.button(
        label="Copiar embed",
        style=discord.ButtonStyle.green,
        emoji="<:copy:1115749292783706222>",
        custom_id="buttoncopyextras",
        row=1,
    )
    async def on_copy(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(copyModal(self.index, self.embeds, self.bot, self.defaultView,  self.buttonsView, bonusOptionsView))

    @discord.ui.button(
        label="JSON importar",
        style=discord.ButtonStyle.primary,
        emoji="<:download:1123270385731899433>",
        custom_id="buttonjsoninport",
        row=2,
    )
    async def on_json_in(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(jsonModal(
            self.index, self.embeds, self.bot,
            self.defaultView, self.buttonsView, bonusOptionsView))

    @discord.ui.button(
        label="JSON exportar",
        style=discord.ButtonStyle.primary,
        emoji="<:upload:1123270066465673237>",
        custom_id="buttonjsonexport",
        row=2,
    )
    async def on_json_ex(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed_json = json.dumps(self.embed.to_dict())
        if len(json.dumps(self.embed.to_dict())) <= 1990:
            await interaction.response.send_message(f"```{embed_json}```", ephemeral=True)
        else:
            with open(f"./arquivo{interaction.user.id}.txt", "w") as arquivo:
                # Escrever no arquivo
                arquivo.write(embed_json)
            with open(f"./arquivo{interaction.user.id}.txt", "rb") as file:
                await interaction.response.send_message(file=discord.File(file), ephemeral=True)
                os.remove(f"./arquivo{interaction.user.id}.txt")


