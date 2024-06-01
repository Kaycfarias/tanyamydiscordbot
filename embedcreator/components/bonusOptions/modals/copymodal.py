import discord


class copyModal(discord.ui.Modal):
    def __init__(self, index, embeds, bot, defaultView,
                 buttonsView, bonusOptionsView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.embed = self.embeds[self.index]
        self.defaultView = defaultView
        self.buttonsView = buttonsView
        self.bonusOptionsView = bonusOptionsView
        super().__init__(title="Copie a embed de uma mensagem.")
        self.link = discord.ui.TextInput(
            label="Link da messagem contendo a embed:",
            placeholder="Insira o link da mensagem...",
            style=discord.TextStyle.short,
        )
        self.pos = discord.ui.TextInput(
            label="Posição da embed na mensagem",
            default="1",
            placeholder="Insira a posição da embed",
            style=discord.TextStyle.short,
            max_length=2,
            min_length=1,
        )
        self.add_item(self.link)
        self.add_item(self.pos)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            channel_id, message_id = self.link.value.split("/")[-2:]
            channel = self.bot.get_channel(int(channel_id))
            target_message = await channel.fetch_message(message_id)
        except:
            return await interaction.response.send_message(
                "<:error:1116338705955823626> | Não consegui encontrar essa mensagem",
                ephemeral=True,
                delete_after=3,
            )

        def podeserint(n):
            try:
                int(n)
                return True
            except:
                return False

        if podeserint(self.pos.value):
            if int(self.pos.value) <= (len(target_message.embeds)) and int(self.pos.value) > 0:
                self.embeds[self.index] = target_message.embeds[int(
                    self.pos.value) - 1]
                # self.embed.author = embed.author
                # self.embed.colour = embed.colour
                # self.embed.description = embed.description
                # self.embed.fields = embed.fields
                # self.embed.footer = embed.footer
                # self.embed.image = embed.image
                # self.embed.thumbnail = embed.thumbnail
                # self.embed.timestamp = embed.timestamp
                # self.embed.title = embed.title
                # self.embed.url = embed.url
                await interaction.response.edit_message(
                    embed=self.embeds[self.index],
                    view=self.bonusOptionsView(self.index, self.embeds, self.bot,
                    self.defaultView, self.buttonsView),
                )
            else:
                await interaction.response.send_message(
                    f"<:error:1116338705955823626> | Não foi possível copiar a embed de posição {self.pos.value} desta mensagem, pois ela contém apenas {len(target_message.embeds)} embeds.",
                    ephemeral=True,
                    delete_after=7,
                )
        else:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Por favor, informe o valor numérico que representa a posição da embed na mensagem.",
                ephemeral=True,
                delete_after=7,
            )

