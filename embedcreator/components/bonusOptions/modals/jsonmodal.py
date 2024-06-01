import json
import discord


class jsonModal(discord.ui.Modal):
    def __init__(self, index, embeds, bot,
                 defaultView, buttonsView, bonusOptionsView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.defaultView = defaultView
        self.buttonsView = buttonsView
        self.bonusOptionsView = bonusOptionsView
        super().__init__(title="Json da embed.")
        self.json = discord.ui.TextInput(
            label="Json da embed:",
            placeholder="Cole o JSON aqui",
            style=discord.TextStyle.paragraph,
        )
        self.add_item(self.json)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            self.embeds[self.index] = discord.Embed.from_dict(
                json.loads(self.json.value))
            await interaction.response.edit_message(embed=self.embeds[self.index])
        except json.decoder.JSONDecodeError:
            await interaction.response.send_message(
                "<:error:1116338705955823626> | Não consegui criar uma embed a partir do JSON fornecido",
                ephemeral=True,
                delete_after=7,
            )

