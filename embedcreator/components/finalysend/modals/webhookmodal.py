import discord
import validators
import aiohttp

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
            default=membro.avatar.url if membro.avatar else "",
            style=discord.TextStyle.long,
            required=False
        )
        self.add_item(self.nome)
        self.add_item(self.avatar)

    async def on_submit(self, interaction: discord.Interaction):
        avatar_data = None
        await interaction.response.defer()
        if self.avatar.value is not None and self.avatar.value.strip() != "":
            if not validators.url(self.avatar.value):
                return await interaction.followup.send(
                    "<:error:1116338705955823626> | Vish, deu erro, verifique a url da imagem fornecida para o avatar",
                    ephemeral=True,
                )
            try:

                # Fazer download assíncrono da imagem do avatar
                async with aiohttp.ClientSession() as session:
                    async with session.get(self.avatar.value, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                        if resp.status == 200 and resp.content_type.startswith('image/'):
                            avatar_data = await resp.read()
                        else:
                            return await interaction.followup.send(
                                "<:error:1116338705955823626> | A URL fornecida não é uma imagem válida ou não está acessível",
                                ephemeral=True,
                            )

            except discord.Forbidden:
                return await interaction.followup.send(
                    "<:error:1116338705955823626> | Sinto muito, eu não tenho permissão para gerenciar webhooks",
                    ephemeral=True,
                )
            except aiohttp.ClientError:
                return await interaction.followup.send(
                    "<:error:1116338705955823626> | Erro ao fazer download da imagem do avatar",
                    ephemeral=True,
                )
            except Exception:
                return await interaction.followup.send(
                    "<:error:1116338705955823626> | Vish, parece que esse link não é de uma imagem compativel",
                    ephemeral=True,
                )

        try:
            webhook = await interaction.channel.create_webhook(
                name=self.nome.value,
                avatar=avatar_data,
                reason=f"criado pelo usuário {interaction.user} usando comando",
            )
            await webhook.send(embeds=self.embeds)
            await interaction.followup.send(
                f"<:suceso:1116338902228275310> | embed envia por webhook",
                ephemeral=True,
            )
            await webhook.delete()
        except discord.Forbidden:
            await interaction.followup.send(
                "<:error:1116338705955823626> | Sinto muito, eu não tenho permissão para gerenciar webhooks",
                ephemeral=True,
            )
        except Exception:
            await interaction.followup.send(
                "<:error:1116338705955823626> | Ocorreu um erro ao criar ou enviar o webhook",
                ephemeral=True,
            )