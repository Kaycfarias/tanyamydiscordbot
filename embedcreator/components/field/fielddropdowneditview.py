import discord
from embedcreator.components.field.modals.editfieldmodal import EditFieldModal


class FieldDropdownEditView(discord.ui.View):
    def __init__(self, index, embeds, bot, FieldView, ButtonView, DefaultView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.FieldView = FieldView
        self.ButtonView = ButtonView
        self.DefaultView = DefaultView
        self.embed = self.embeds[self.index]
        super().__init__(timeout=None)
        self.add_item(FieldDropdownEdit(self.index, self.embeds, self.bot,
                                        FieldView, ButtonView, DefaultView))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltar2",
        row=0,
    )
    async def on_voltar2(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=self.FieldView(
                self.index, self.embeds, self.bot,
                self.ButtonView, self.DefaultView)
        )


class FieldDropdownEdit(discord.ui.Select):
    def __init__(self, index, embeds, bot, FieldView, ButtonView, DefaultView):

        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.FieldView = FieldView
        self.ButtonView = ButtonView
        self.DefaultView = DefaultView
        self.embed = self.embeds[self.index]
        super().__init__(
            placeholder="Escolha um campo para editar",
            min_values=1,
            max_values=1,
            options=[],
            row=1,
        )
        self.add_options()

    def add_options(self):
        for i, field in enumerate(self.embed.fields):
            label = f"Nome: {field.name}"
            description = f"Valor: {field.value}"
            value = f"0,{i}"
            if len(label) >= 100:
                label = label[:97] + "..."
            if len(description) >= 100:
                description = description[:97] + "..."
            self.add_option(label=label, description=description, value=value)

    async def callback(self, interaction: discord.Interaction):
        embed_index, field_index = map(int, self.values[0].split(","))
        selected_field = self.embed.fields[field_index]
        await interaction.response.send_modal(
            EditFieldModal(self.index, self.embeds, self.bot,
                           selected_field, field_index, FieldDropdownEditView,
                           self.FieldView, self.ButtonView, self.DefaultView)
        )
