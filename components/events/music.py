import wavelink
from discord.ext import commands

class MusicHandler(commands.Cog):
    """Gerenciador de eventos principais do bot."""
    
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_wavelink_node_ready(self, payload: wavelink.NodeReadyEventPayload):
        """Evento quando o node do Lavalink está pronto."""
        print(f"🎵 Node '{payload.node.identifier}' conectado!")

    @commands.Cog.listener()
    async def on_wavelink_track_start(self, payload: wavelink.TrackStartEventPayload):
        """Evento quando uma música começa a tocar."""
        player = payload.player
        if player and hasattr(player, 'text_channel'):
            embed = create_track_embed(payload.track)
            await player.text_channel.send(embed=embed)

async def setup(bot: commands.Bot):
    await bot.add_cog(MusicHandler(bot))