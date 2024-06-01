import json
import os

import discord
import requests
import validators
from discord.errors import Forbidden


class DefaultView(discord.ui.View):
    # Esta é a "view" padrão
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(DropdownEmbed(self.embeds, self.bot))
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
    async def on_add(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.embeds.append(
            discord.Embed(title="título", description="Descrição",
                          colour=discord.Colour.random())
        )
        await interaction.response.edit_message(
            embeds=self.embeds, view=DefaultView(self.embeds, self.bot)
        )

    @discord.ui.button(
        label="Finalizar",
        style=discord.ButtonStyle.green,
        emoji="<:enviar:1105962897768726650>",
        custom_id="buttonfinalizar",
        row=1,
    )
    async def on_finalizar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=FinalizarView(self.embeds, self.bot))


class FieldView(discord.ui.View):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.bot = bot
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
    async def on_campo_edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=BotaoView(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="Adcionar novo campo",
        style=discord.ButtonStyle.grey,
        emoji="<:adicionar:1105963449491665016>",
        custom_id="buttoncampo",
        row=1,
    )
    async def on_campo(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(FieldModal(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="Editar campo",
        style=discord.ButtonStyle.grey,
        emoji="<:titulo:1105963013284057158>",
        custom_id="buttoneditfield",
        row=2,
    )
    async def on_edit_field(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=FieldDropdownEditView(self.index, self.embeds, self.bot)
        )

    @discord.ui.button(
        label="apagar",
        style=discord.ButtonStyle.red,
        emoji="<:lixo:1105962772543574206>",
        custom_id="buttonapagar",
        row=2,
    )
    async def on_apagar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=FieldDropdownClearView(self.index, self.embeds, self.bot)
        )


class FieldDropdownEditView(discord.ui.View):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.embed = self.embeds[self.index]
        super().__init__(timeout=None)
        self.add_item(FieldDropdownEdit(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltar2",
        row=0,
    )
    async def on_voltar2(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=FieldView(self.index, self.embeds, self.bot))


class FieldDropdownEdit(discord.ui.Select):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.bot = bot
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
                           selected_field, field_index)
        )


class FieldDropdownClearView(discord.ui.View):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.embed = self.embeds[self.index]
        super().__init__(timeout=None)
        self.add_item(FieldDropdownClear(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltar1",
        row=0,
    )
    async def on_voltar3(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=FieldView(self.index, self.embeds, self.bot))


class FieldDropdownClear(discord.ui.Select):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.embed = self.embeds[self.index]
        super().__init__(
            placeholder="Escolha um campo para apagar",
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
        self.embed.remove_field(index=field_index)
        if len(self.embed.fields) > 0:
            await interaction.response.edit_message(
                embed=self.embed, view=FieldDropdownClearView(
                    self.index, self.embeds, self.bot)
            )
        else:
            await interaction.response.edit_message(
                embed=self.embed, view=FieldView(
                    self.index, self.embeds, self.bot)
            )


class CorView(discord.ui.View):
    def __init__(self, index, embeds, bot):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(CorDropdown(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltar1",
        row=0,
    )
    async def on_voltar4(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=BotaoView(self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="Código HEX",
        style=discord.ButtonStyle.grey,
        emoji="<:adicionar:1105963449491665016>",
        custom_id="buttoncorhex",
        row=1,
    )
    async def on_hex(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(CorModal(self.index, self.embeds))



class FinalizarView(discord.ui.View):
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(timeout=None)

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltarfinalizar",
        row=0,
    )
    async def on_voltar6(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=PrimView(self.embeds, self.bot))

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
        await interaction.response.edit_message(view=EscolherChatView(self.embeds, self.bot))

    @discord.ui.button(
        label="Editar embed já enviada",
        style=discord.ButtonStyle.blurple,
        emoji="<:editar:1116337400659050506>",
        custom_id="buttonfinalizaredit",
        row=2,
    )
    async def on_edit(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(EdicaoModal(self.embeds, self.bot))

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
            await interaction.response.send_modal(WebhookModal(self.embeds, interaction.user))


class WebhookModal(discord.ui.Modal):
    def __init__(self, embeds, membro):
        self.embeds = embeds
        self.membro = membro
        super().__init__(title="Crie antes o webhook")
        self.nome = discord.ui.TextInput(
            label="Nome do webhook",
            placeholder="Defina um nome para o webhook...",
            default=membro.display_name,
            style=discord.TextStyle.short,
        )
        self.avatar = discord.ui.TextInput(
            label="Imagem do avatar do webhook",
            placeholder="Insira uma url válida para o avatar do webhook...",
            default=membro.avatar.url,
            style=discord.TextStyle.long,
        )
        self.add_item(self.nome)
        self.add_item(self.avatar)

    async def on_submit(self, interaction: discord.Interaction):
        if validators.url(self.avatar.value):
            await interaction.response.defer()
            try:
                webhook = await interaction.channel.create_webhook(
                    name=self.nome.value,
                    avatar=requests.get(self.avatar.value).content,
                    reason=f"criado pelo usuário {interaction.user} usando comando",
                )
                await webhook.send(embeds=self.embeds)
                await webhook.delete()
                await interaction.followup.send(
                    f"<:suceso:1116338902228275310> | embed envia por webhook",
                    ephemeral=True,
                )
            except Forbidden:
                await interaction.followup.send(
                    "<:error:1116338705955823626> | Sinto muito, eu não tenho permissão para gerenciar webhooks",
                    ephemeral=True,
                )
            except:
                await interaction.followup.send(
                    "<:error:1116338705955823626> | Vish, parece que esse link não é de uma imagem compativel",
                    ephemeral=True,
                )
        else:
            await interaction.followup.send(
                "<:error:1116338705955823626> | Vish, deu erro, verifique a url da imagem fornecida para o avatar",
                ephemeral=True,
            )


class EdicaoModal(discord.ui.Modal):
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(title="Aplicar edição a uma embed existente")
        self.link = discord.ui.TextInput(
            label="Link da mensagem:",
            placeholder="Insira o link da mensagem que contém a embed ...",
            style=discord.TextStyle.short,
        )
        self.add_item(self.link)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            server_id, channel_id, message_id = self.link.value.split("/")[-3:]
            channel = self.bot.get_channel(int(channel_id))
            target_message = await channel.fetch_message(message_id)
        except:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Sinto muito, Não consegui encontrar esta mensagem, verifique o link fornecido",
                ephemeral=True,
                delete_after=5,
            )
            return
        if target_message.author != self.bot.user:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Essa mensagem não foi enviada por mim",
                ephemeral=True,
                delete_after=5,
            )
            return
        if int(server_id) == interaction.guild_id:
            await target_message.edit(embeds=self.embeds)
            await interaction.response.send_message(
                f"<:suceso:1116338902228275310> | A embed da mensagem https://discord.com/channels/{server_id}/{channel_id}/{message_id} foi editada",
                ephemeral=True,
                delete_after=5,
            )
        else:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Sinto muito, mas parece que esta mensagem foi enviada em outro servidor",
                ephemeral=True,
                delete_after=5,
            )


class EscolherChatView(discord.ui.View):
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(timeout=None)
        self.add_item(EscolherChatDropDown(self.embeds, self.bot))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltarenviar",
        row=0,
    )
    async def on_voltar_enviar(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(view=FinalizarView(self.embeds, self.bot))


class EscolherChatDropDown(discord.ui.ChannelSelect):
    def __init__(self, embeds, bot):
        self.embeds = embeds
        self.bot = bot
        super().__init__(
            placeholder="Escolha o chat:",
            channel_types=[discord.ChannelType.text, discord.ChannelType.news],
            min_values=1,
            max_values=1,
            custom_id="ChatDropdown",
            row=1,
        )

    async def callback(self, interaction: discord.Interaction):
        try:
            channel = await self.bot.fetch_channel(self.values[0].id)
            await channel.send(embeds=self.embeds)
            await interaction.response.send_message(
                f"<:suceso:1116338902228275310> | A embed foi enviada para o chat{self.values[0].mention}.",
                ephemeral=True,
                delete_after=5,
            )
        except discord.errors.Forbidden:
            await interaction.response.send_message(
                f"<:error:1116338705955823626> | Parece que não tenho as permissões necessárias para enviar mensagens no chat {self.values[0].mention}",
                ephemeral=True,
                delete_after=7,
            )
