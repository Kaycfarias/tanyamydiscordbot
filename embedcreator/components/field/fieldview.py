import discord
from embedcreator.components.field.modals.newfieldmodal import NewFieldModal
from embedcreator.components.field.fielddropdownclearview import FieldDropdownClearView
from embedcreator.components.field.fielddropdowneditview import FieldDropdownEditView


class FieldView(discord.ui.View):
    def __init__(self, index, embeds, bot, ButtonView, DefaultView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.ButtonView = ButtonView
        self.DefaultView = DefaultView
        self.embed = self.embeds[self.index]
        super().__init__(timeout=None)
        if len(self.embed.fields) == 0:
            self.disable_button()

        if len(self.embed.fields) >= 25:
            self.disable_button1()

    def disable_button(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttonapagar":
                    child.disabled = True

                if child.custom_id == "buttoneditfield":
                    child.disabled = True

    def disable_button1(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttoncampo":
                    child.disabled = True

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttoncampoexit",
        row=0,
    )
    async def on_voltar(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=self.ButtonView(self.index, self.embeds,
                                 self.bot, self.DefaultView)
        )

    @discord.ui.button(
        label="Adcionar novo campo",
        style=discord.ButtonStyle.grey,
        emoji="<:adicionar:1105963449491665016>",
        custom_id="buttoncampo",
        row=1,
    )
    async def on_campo(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            NewFieldModal(self.index, self.embeds, self.bot,
                          FieldView, self.ButtonView, self.DefaultView)
        )

    @discord.ui.button(
        label="Editar campo",
        style=discord.ButtonStyle.grey,
        emoji="<:titulo:1105963013284057158>",
        custom_id="buttoneditfield",
        row=2,
    )
    async def on_edit_field(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=FieldDropdownEditView(
                self.index, self.embeds, self.bot,
                FieldView, self.ButtonView, self.DefaultView
            )
        )

    @discord.ui.button(
        label="apagar",
        style=discord.ButtonStyle.red,
        emoji="<:lixo:1105962772543574206>",
        custom_id="buttonapagar",
        row=2,
    )
    async def on_apagar(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=FieldDropdownClearView(
                self.index, self.embeds, self.bot,
                FieldView, self.ButtonView, self.DefaultView
            )
        )
