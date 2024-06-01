import discord


class editEmbedModal(discord.ui.Modal):
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

