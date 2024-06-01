import discord
from embedcreator.components.color.modals.colormodal import ColorModal
from embedcreator.components.color.colordropdown import ColorDropdown


class ColorView(discord.ui.View):
    def __init__(self, index, embeds, bot, ButtonView, DefaultView):
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        self.bot = bot
        self.ButtonView = ButtonView
        self.DefaultView = DefaultView
        super().__init__(timeout=None)
        self.add_item(ColorDropdown(
            self.index, self.embeds, self.bot))

    @discord.ui.button(
        label="",
        style=discord.ButtonStyle.grey,
        emoji="<:voltar:1105963280071151728>",
        custom_id="buttonvoltar1",
        row=0,
    )
    async def on_voltar4(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(
            view=self.ButtonView(self.index, self.embeds,
                                 self.bot, self.DefaultView)
        )

    @discord.ui.button(
        label="Código HEX",
        style=discord.ButtonStyle.grey,
        emoji="<:adicionar:1105963449491665016>",
        custom_id="buttoncorhex",
        row=1,
    )
    async def on_hex(
            self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(ColorModal(self.index, self.embeds))


class CorDropdown(discord.ui.Select):
    def __init__(self, index, embeds, bot):
        self.bot = bot
        self.index = index
        self.embeds = embeds
        self.embed = self.embeds[self.index]
        super().__init__(
            placeholder="Escolha uma cor para sua embed",
            min_values=1,
            max_values=1,
            row=2,
            options=[
                discord.SelectOption(
                    value="red", label="Vermelho", emoji="<:red:1115672009062498384>"
                ),
                discord.SelectOption(
                    value="orange", label="Laranja", emoji="<:orange:1115671940766633984>"
                ),
                discord.SelectOption(
                    value="yellow", label="Amarelo", emoji="<:yellow:1115671862656110722>"
                ),
                discord.SelectOption(
                    value="green", label="Verde", emoji="<:green:1115671786479177748>"
                ),
                discord.SelectOption(
                    value="blue", label="Azul", emoji="<:blue:1115671706296664134>"
                ),
                discord.SelectOption(
                    value="purple", label="roxo", emoji="<:purple:1115671573874094132>"
                ),
                discord.SelectOption(
                    value="pink", label="Rosa", emoji="<:pink:1115671400129249342>"
                ),
                discord.SelectOption(
                    value="brown", label="Marron", emoji="<:brown:1115671490520690848>"
                ),
                discord.SelectOption(value="black", label="Preto", emoji="⬛"),
                discord.SelectOption(value="white", label="Branco", emoji="⬜"),
                discord.SelectOption(
                    value="dblue", label="Discord azul", emoji="<:squareblue:1115656685776797747>"
                ),
                discord.SelectOption(
                    value="dblurple",
                    label="Discord Roxo-azulado",
                    emoji="<:squareblurple:1115651968795430963>",
                ),
                discord.SelectOption(
                    value="dgold", label="Discord ouro", emoji="<:gold:1115678170625081435>"
                ),
                discord.SelectOption(
                    value="dgreen",
                    label="Discord verde",
                    emoji="<:squaregreen:1115656866303852706>",
                ),
                discord.SelectOption(
                    value="dmagenta",
                    label="Discord magenta",
                    emoji="<:squaremagenta:1115657261335990312>",
                ),
                discord.SelectOption(
                    value="dorange", label="Discord laranja", emoji="<:orange:1115678121740480544>"
                ),
                discord.SelectOption(
                    value="dpurple", label="Discord roxo", emoji="<:purple:1115678064131723264>"
                ),
                discord.SelectOption(
                    value="dred", label="Discord vermelho", emoji="<:squarered:1115657128951169054>"
                ),
                discord.SelectOption(
                    value="dyellow",
                    label="Discord amarelo",
                    emoji="<:squareyellow:1115657034935828480>",
                ),
                discord.SelectOption(
                    value="dblack",
                    label="Discord preto",
                    emoji="<:squareblack:1115657357821739069>",
                ),
                discord.SelectOption(
                    value="drandom",
                    label="Discord cores aleatórias",
                    emoji="<:aleatory:1115672065190662285>",
                ),
            ],
        )

    async def callback(self, interaction: discord.Interaction):
        if self.values[0] == "red":
            self.embed.color = 0xFF0000
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "orange":
            self.embed.color = 0xFFA500
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "yellow":
            self.embed.color = 0xFFFF00
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "green":
            self.embed.color = 0x00FF00
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "blue":
            self.embed.color = 0x0000FF
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "purple":
            self.embed.color = 0x993399
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "pink":
            self.embed.color = 0xFF00FF
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "brown":
            self.embed.color = 0x964B00
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "black":
            self.embed.color = 0x000000
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "white":
            self.embed.color = 0xFFFFFF
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dblue":
            self.embed.color = discord.Colour.blue()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dblurple":
            self.embed.color = discord.Colour.blurple()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dgold":
            self.embed.color = discord.Colour.gold()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dgreen":
            self.embed.color = discord.Colour.green()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dmagenta":
            self.embed.color = discord.Colour.magenta()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dorange":
            self.embed.color = discord.Colour.orange()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dpurple":
            self.embed.color = discord.Colour.purple()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dred":
            self.embed.color = discord.Colour.red()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dyellow":
            self.embed.color = discord.Colour.yellow()
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "dblack":
            self.embed.color = 0x23272A
            await interaction.response.edit_message(embed=self.embed)
        elif self.values[0] == "drandom":
            self.embed.color = discord.Colour.random()
            await interaction.response.edit_message(embed=self.embed)
