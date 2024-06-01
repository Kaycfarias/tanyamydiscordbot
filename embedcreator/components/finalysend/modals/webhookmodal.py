import discord


class webhookModal(discord.ui.Modal):
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

