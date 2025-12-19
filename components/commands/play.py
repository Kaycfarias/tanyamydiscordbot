import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from musicmanager import get_manager

# Opções do FFmpeg para streaming
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'  # Sem vídeo, apenas áudio
}


class Play(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.music_manager = get_manager()

    @app_commands.command(name=_T("play"), description=_T("[Music] Play a music in voice channel"))
    @app_commands.guild_only()
    @app_commands.describe(
        music=_T("Name of the music or Spotify URL to play")
    )
    async def on_play(self, interaction: discord.Interaction, music: str):
        # Verifica se o usuário está em um canal de voz
        if not interaction.user.voice:
            await interaction.response.send_message(
                "❌ Você precisa estar em um canal de voz!",
                ephemeral=True
            )
            return
        
        voice_channel = interaction.user.voice.channel
        
        await interaction.response.defer()
        
        # Busca a música e obtém URL de streaming
        song, stream_url = await self.music_manager.search_and_get_stream(music)
        
        if not song or not stream_url:
            await interaction.followup.send("❌ Nenhuma música encontrada.")
            return
        
        # Conecta ao canal de voz (ou usa conexão existente)
        voice_client = interaction.guild.voice_client
        
        if voice_client is None:
            voice_client = await voice_channel.connect()
        elif voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
        
        # Para música atual se estiver tocando
        if voice_client.is_playing():
            voice_client.stop()
        
        # Toca o streaming
        audio_source = discord.FFmpegPCMAudio(stream_url, **FFMPEG_OPTIONS)
        voice_client.play(audio_source)
        
        # Cria embed com informações da música
        embed = discord.Embed(
            title="🎵 Tocando agora",
            description=f"**{song.name}**",
            color=discord.Color.green()
        )
        embed.add_field(name="Artista", value=song.artist, inline=True)
        embed.add_field(name="Álbum", value=song.album_name or "N/A", inline=True)
        
        if song.cover_url:
            embed.set_thumbnail(url=song.cover_url)
        
        embed.set_footer(text=f"Spotify: {song.url}")
        
        await interaction.followup.send(embed=embed)

    @app_commands.command(name=_T("stop"), description=_T("[Music] Stop the music and leave"))
    @app_commands.guild_only()
    async def on_stop(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        
        if voice_client:
            voice_client.stop()
            await voice_client.disconnect()
            await interaction.response.send_message("⏹️ Música parada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Não estou tocando nada.", ephemeral=True)

    @app_commands.command(name=_T("pause"), description=_T("[Music] Pause the music"))
    @app_commands.guild_only()
    async def on_pause(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        
        if voice_client and voice_client.is_playing():
            voice_client.pause()
            await interaction.response.send_message("⏸️ Música pausada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma música tocando.", ephemeral=True)

    @app_commands.command(name=_T("resume"), description=_T("[Music] Resume the music"))
    @app_commands.guild_only()
    async def on_resume(self, interaction: discord.Interaction):
        voice_client = interaction.guild.voice_client
        
        if voice_client and voice_client.is_paused():
            voice_client.resume()
            await interaction.response.send_message("▶️ Música retomada.", ephemeral=True)
        else:
            await interaction.response.send_message("❌ Nenhuma música pausada.", ephemeral=True)


    @app_commands.command(name=_T("search"), description=_T("[Music] Search for a music"))
    @app_commands.guild_only()
    async def on_search(self, interaction: discord.Interaction, music: str):
        song = await self.music_manager.search(music)
        await interaction.response.send_message(f'{song}', ephemeral=False)


    @on_play.autocomplete('music')
    async def music_autocomplete(self, interaction: discord.Interaction, current: str) -> list[app_commands.Choice[str]]:
        if len(current) < 2:
            return []
        
        musics = await self.music_manager.search(current)
        choices = []
        for music in musics[:10]:
            display_name = f"{music.name} - {music.artist}"
            # Salva a Song no cache para reutilizar no play
            self.music_manager._song_cache[display_name] = music
            choices.append(app_commands.Choice(name=display_name, value=display_name))
        
        return choices
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))
