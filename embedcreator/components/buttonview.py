import discord
from embedcreator.components.modals.titllemodal import TitleModal
from embedcreator.components.modals.descriptionmodal import DescriptionModal
from embedcreator.components.modals.authotmodal import AuthorModal

from embedcreator.components.color.colorview import ColorView
from embedcreator.components.field.fieldview import FieldView

from embedcreator.components.modals.imagemodal import ImageModal
from embedcreator.components.modals.footermodal import FooterModal
# ExtrasView
from embedcreator.components.bonusOptions.bonusOptionsView import bonusOptionsView


class buttonsView(discord.ui.View):
    def __init__(self, index, embeds, bot, defaultView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.defaultView = defaultView
        super().__init__(timeout=None)
        if len(self.embeds) == 1:
            self.disable_button()

    def disable_button(self):
        for child in self.children:
            if isinstance(child, discord.ui.Button):
                if child.custom_id == "buttonembedapgar":
                    self.remove_item(child)

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonviewexit",
        row=0,
    )
    async def on_voltar(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            embeds=self.embeds, view=self.defaultView(self.embeds, self.bot)
        )

    @discord.ui.button(
        label="Título",
        style=discord.ButtonStyle.grey,
        emoji="<:titulo:1105963013284057158>",
        custom_id="buttontitle",
        row=1,
    )
    async def on_titulo(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            TitleModal(
                self.index, self.embeds
            )
        )

    @discord.ui.button(
        label="Descrição",
        style=discord.ButtonStyle.grey,
        emoji="<:descricao:1105962952437268492>",
        custom_id="buttondesc",
        row=1,
    )
    async def on_desc(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            DescriptionModal(self.index, self.embeds)
        )

    @discord.ui.button(
        label="Cor",
        style=discord.ButtonStyle.grey,
        emoji="<:cor:1105963155760357437>",
        custom_id="buttoncor",
        row=1,
    )
    async def on_Cor(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=ColorView(
                self.index, self.embeds,
                self.bot, buttonsView, self.defaultView)
        )

    @discord.ui.button(
        label="Autor",
        style=discord.ButtonStyle.grey,
        emoji="<:author:1105962409035829308>",
        custom_id="buttonautor",
        row=1,
    )
    async def on_autor(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(
            AuthorModal(self.index, self.embeds)
        )

    @discord.ui.button(
        label="Editar campos",
        style=discord.ButtonStyle.grey,
        emoji="<:campos:1105962681606885517>",
        custom_id="buttoncampoedit",
        row=1,
    )
    async def on_campo_edit(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=FieldView(self.index, self.embeds, self.bot, buttonsView, self.defaultView))

    @discord.ui.button(
        label="Imagem e thumbnail",
        style=discord.ButtonStyle.grey,
        emoji="<:image:1105963213637562520>",
        custom_id="buttonimagem",
        row=2,
    )
    async def on_imagem(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ImageModal(self.index, self.embeds))

    @discord.ui.button(
        label="Rodapé",
        style=discord.ButtonStyle.grey,
        emoji="<:rodape:1122530874110517278>",
        custom_id="buttonrodape",
        row=2,
    )
    async def on_rodape(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FooterModal(self.index, self.embeds))

    @discord.ui.button(
        label="Carimbo de data/hora",
        style=discord.ButtonStyle.grey,
        emoji="<:timestamp:1133120781019250699>",
        custom_id="buttontime",
        row=2,
    )
    async def on_time(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.embeds[self.index].timestamp:
            self.embeds[self.index].timestamp = None
        else:
            self.embeds[self.index].timestamp = interaction.created_at
        await interaction.response.edit_message(embed=self.embeds[self.index])

    @discord.ui.button(
        label="Opções úteis",
        style=discord.ButtonStyle.blurple,
        emoji="<:extras:1115749406453551224>",
        custom_id="buttonextras",
        row=3,
    )
    async def on_extras(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=bonusOptionsView(self.index, self.embeds, self.bot, self.defaultView, buttonsView))

    @discord.ui.button(
        label="Apagar embed",
        style=discord.ButtonStyle.red,
        emoji="<:lixo:1105962772543574206>",
        custom_id="buttonembedapgar",
        row=3,
    )
    async def on_apagar_embed(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embeds.remove(self.embeds[self.index])
        await interaction.response.edit_message(
            embeds=self.embeds, view=self.defaultView(
                self.embeds, self.bot)
        )
