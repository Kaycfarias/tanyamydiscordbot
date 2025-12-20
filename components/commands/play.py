import discord
import wavelink
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from musicmanager import (
    search_tracks,
    get_or_create_player,
    play_track,
    stop_player,
    pause_player,
    resume_player,
    skip_track,
    set_volume,
    get_player,
    create_track_embed,
    create_nowplaying_embed,
    SearchCache,
)


class Play(commands.Cog):
    """Comandos de música usando Lavalink."""
    
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self._cache = SearchCache()

    @app_commands.command(name=_T("play"), description=_T("[Music] Play a music in voice channel"))
    @app_commands.guild_only()
    @app_commands.describe(music=_T("Name of the music or URL to play"))
    async def on_play(self, interaction: discord.Interaction, music: str):
        """Toca uma música."""
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ Você precisa estar em um canal de voz!",
                ephemeral=True
            )
            return
        
        await interaction.response.defer()
        
        try:
            # Obtém ou cria o player
            player = await get_or_create_player(
                interaction.guild,
                interaction.user.voice.channel,
                interaction.channel
            )
            
            # Verifica cache ou busca
            track = self._cache.get(music)
            if not track:
                tracks = await search_tracks(music, limit=1, timeout=5.0)
                if not tracks:
                    await interaction.followup.send("❌ Nenhuma música encontrada.")
                    return
                track = tracks[0]
            
            # Toca e envia embed
            embed = await play_track(player, track)
            await interaction.followup.send(embed=embed)
            
        except Exception as e:
            await interaction.followup.send(
                f"❌ Erro ao tocar música: {str(e)[:100]}",
                ephemeral=True
            )

    @app_commands.command(name=_T("stop"), description=_T("[Music] Stop the music and leave"))
    @app_commands.guild_only()
    async def on_stop(self, interaction: discord.Interaction):
        """Para a música e desconecta."""
        if await stop_player(interaction.guild):
            await interaction.response.send_message("⏹️ Música parada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Não estou tocando nada.", ephemeral=True)

    @app_commands.command(name=_T("pause"), description=_T("[Music] Pause the music"))
    @app_commands.guild_only()
    async def on_pause(self, interaction: discord.Interaction):
        """Pausa a música."""
        if await pause_player(interaction.guild):
            await interaction.response.send_message("⏸️ Música pausada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma música tocando.", ephemeral=True)

    @app_commands.command(name=_T("resume"), description=_T("[Music] Resume the music"))
    @app_commands.guild_only()
    async def on_resume(self, interaction: discord.Interaction):
        """Retoma a música pausada."""
        if await resume_player(interaction.guild):
            await interaction.response.send_message("▶️ Música retomada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma música pausada.", ephemeral=True)

    @app_commands.command(name=_T("skip"), description=_T("[Music] Skip current song"))
    @app_commands.guild_only()
    async def on_skip(self, interaction: discord.Interaction):
        """Pula a música atual."""
        if await skip_track(interaction.guild):
            await interaction.response.send_message("⏭️ Música pulada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma música tocando.", ephemeral=True)

    @app_commands.command(name=_T("volume"), description=_T("[Music] Set volume (0-100)"))
    @app_commands.guild_only()
    @app_commands.describe(level=_T("Volume level (0-100)"))
    async def on_volume(self, interaction: discord.Interaction, level: int):
        """Define o volume."""
        result = await set_volume(interaction.guild, level)
        if result is not None:
            await interaction.response.send_message(f"🔊 Volume: {result}%", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Não estou conectado.", ephemeral=True)

    @app_commands.command(name=_T("nowplaying"), description=_T("[Music] Show current song"))
    @app_commands.guild_only()
    async def on_nowplaying(self, interaction: discord.Interaction):
        """Mostra a música atual."""
        player = get_player(interaction.guild)
        embed = create_nowplaying_embed(player) if player else None
        
        if embed:
            await interaction.response.send_message(embed=embed)
        else:
            await interaction.response.send_message("❌ Nenhuma música tocando.", ephemeral=True)

    @on_play.autocomplete('music')
    async def music_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        """Autocomplete para buscar músicas."""
        if len(current) < 2:
            return []
        
        tracks = await search_tracks(current, limit=5, timeout=2.0)
        choices = []
        
        for track in tracks:
            display_name = f"{track.title} - {track.author}"
            if len(display_name) > 100:
                display_name = display_name[:97] + "..."
            if len(display_name) < 1:
                continue
            
            self._cache.set(display_name, track)
            choices.append(app_commands.Choice(name=display_name, value=display_name))
        
        return choices


async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
