import discord


class chooseChannelView(discord.ui.View):
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
        await interaction.response.edit_message(view=finalyView(self.embeds, self.bot, self.defaultView))


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
