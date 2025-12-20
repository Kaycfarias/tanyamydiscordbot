import discord
from discord import app_commands
from discord.app_commands import locale_str as _T
from discord.ext import commands

from musicmanager import get_manager

from typing import cast
import wavelink

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
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message(
                "❌ Você precisa estar em um canal de voz!",
                ephemeral=True
            )
            return

        await interaction.response.defer()

        # Conecta ao canal de voz
        player: wavelink.Player
        player = cast(wavelink.Player, interaction.guild.voice_client)

        if not player:
            try:
                player = await interaction.user.voice.channel.connect(cls=wavelink.Player)
            except Exception as e:
                await interaction.followup.send(f"❌ Erro ao conectar ao canal de voz: {e}")
                return

        player.autoplay = wavelink.AutoPlayMode.enabled

        # Busca informações da música no Spotify via music_manager
        song = None
        if music in self.music_manager._song_cache:
            song = self.music_manager._song_cache[music]
        else:
            songs = await self.music_manager.search(music, limit=1)
            if songs:
                song = songs[0]

        # Busca a track no SoundCloud usando nome + artista do Spotify
        search_query = f"{song.name} {song.artist}" if song else music
        tracks: wavelink.Search = await wavelink.Playable.search(search_query, source=wavelink.TrackSource.YouTubeMusic)
        
        if not tracks:
            await interaction.followup.send("❌ Nenhuma música encontrada.")
            return

        track: wavelink.Playable = tracks[0]
        await player.queue.put_wait(track)

        if not player.playing:
            await player.play(player.queue.get(), volume=30)

        # Cria embed com informações da música (usa dados do Spotify se disponível)
        if song:
            embed = discord.Embed(
                title="🎵 Tocando agora",
                description=f"**{song.name}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Artista", value=song.artist, inline=True)
            embed.add_field(name="Álbum", value=song.album_name or "N/A", inline=True)
            embed.add_field(name="Duração", value=f"{track.length // 60000}:{(track.length // 1000) % 60:02d}", inline=True)
            
            if song.cover_url:
                embed.set_thumbnail(url=song.cover_url)
            
            embed.set_footer(text=f"Spotify: {song.url}")
        else:
            embed = discord.Embed(
                title="🎵 Tocando agora",
                description=f"**{track.title}**",
                color=discord.Color.green()
            )
            embed.add_field(name="Artista", value=track.author or "Desconhecido", inline=True)
            embed.add_field(name="Duração", value=f"{track.length // 60000}:{(track.length // 1000) % 60:02d}", inline=True)
            
            if track.artwork:
                embed.set_thumbnail(url=track.artwork)
            
            embed.set_footer(text=f"Fonte: {track.source}")
        
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
            choices.append(app_commands.Choice(name=display_name[:50], value=display_name[:50]))
        
        return choices
        

async def setup(bot: commands.Bot):
    await bot.add_cog(Play(bot))