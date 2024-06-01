import discord
import validators

from embedcreator.components.finalysend.modals.webhookmodal import webhookModal
from embedcreator.components.finalysend.modals.editembedmodal import editEmbedModal
from embedcreator.components.finalysend.choosechannel.choosechannelview import chooseChannelView


class finalySendView(discord.ui.View):
    def __init__(self, embeds, bot, defaultView):
        self.embeds = embeds
        self.bot = bot
        self.defaultView = defaultView
        super().__init__(timeout=None)

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltarfinalizar",
        row=0,
    )
    async def on_voltar6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=self.defaultView(self.embeds, self.bot))

    @discord.ui.button(
        label="Enviar aqui",
        style=discord.ButtonStyle.green,
        emoji="<:enviar:1105962897768726650>",
        custom_id="buttonenviaraqui",
        row=1,
    )
    async def on_enviar_aqui(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.channel.send(embeds=self.embeds)
            await interaction.response.send_message(
                "<:suceso:1116338902228275310> | Embed enviada com sucesso",
                ephemeral=True,
                delete_after=5,
            )
        except discord.errors.Forbidden:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Parece que não tenho as permissões necessárias para enviar mensagens aqui",
                ephemeral=True,
                delete_after=7,
            )

    @discord.ui.button(
        label="Escolher chat",
        style=discord.ButtonStyle.green,
        emoji="<:enviar:1105962897768726650>",
        custom_id="buttonenviarpara",
        row=1,
    )
    async def on_enviar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=chooseChannelView(self.embeds, self.bot))

    @discord.ui.button(
        label="Editar embed já enviada",
        style=discord.ButtonStyle.blurple,
        emoji="<:editar:1116337400659050506>",
        custom_id="buttonfinalizaredit",
        row=2,
    )
    async def on_edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(editEmbedModal(self.embeds, self.bot))

    @discord.ui.button(
        label="Enviar por webhook",
        style=discord.ButtonStyle.green,
        emoji="<:webhook:1123280184959844403>",
        custom_id="buttonfinalizarwebhook",
        row=3,
    )
    async def on_webhook(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.app_permissions.manage_webhooks:
            return await interaction.response.send_message(
                "<:error:1116338705955823626> | Opa, parece que eu não possuo permissão de gerenciar webhooks nesse servidor",
                ephemeral=True,
                delete_after=10,
            )
        webhooks_n = len(await interaction.channel.webhooks())
        if webhooks_n >= 13:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | limite de webhooks alcancado nesse canal, considere apagar alguns caso esteja sem uso",
                ephemeral=True,
                delete_after=True,
            )
        else:
            await interaction.response.send_modal(webhookModal(self.embeds, interaction.user))
