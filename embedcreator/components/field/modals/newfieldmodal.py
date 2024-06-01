import discord


class NewFieldModal(discord.ui.Modal):
    def __init__(self, index, embeds, bot, FieldView, ButtonView, DefaultView):
        self.index = index
        self.embeds = embeds
        self.bot = bot
        self.FieldView = FieldView
        self.ButtonView = ButtonView
        self.DefaultView = DefaultView
        self.embed = self.embeds[self.index]
        super().__init__(title="Painel de criação do campo.")
        self.nome = discord.ui.TextInput(
            label="Nome do campo:",
            placeholder="Insira o nome do campo...",
            default="Nome do campo",
            style=discord.TextStyle.short,
            max_length=256,
        )
        self.valor = discord.ui.TextInput(
            label="Valor do campo:",
            placeholder="Insira o valor do campo...",
            default="Valor do campo",
            style=discord.TextStyle.paragraph,
            required=False,
            max_length=1024,
        )
        self.emlinha = discord.ui.TextInput(
            label="Em linha?...",
            placeholder="S ou Y para sim e N para não",
            default="N",
            style=discord.TextStyle.short,
            max_length=1,
        )
        self.add_item(self.nome)
        self.add_item(self.valor)
        self.add_item(self.emlinha)

    async def on_submit(self, interaction: discord.Interaction):
        emlinha = self.emlinha.value
        if emlinha is not None:
            emlinha.replace(" ", "")
            if emlinha.lower() == "s" or emlinha.lower() == "y":
                emlinha = True
            else:
                emlinha = False

        self.embed.add_field(name=self.nome.value,
                             value=self.valor.value, inline=emlinha)
        await interaction.response.edit_message(
            embed=self.embed, view=self.FieldView(
                self.index, self.embeds, self.bot,
                self.ButtonView, self.DefaultView
            )
        )
