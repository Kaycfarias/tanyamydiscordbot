"""
Funções para controle do player.
"""

from typing import Optional, cast

import discord
import wavelink

from .embeds import create_track_embed


async def get_or_create_player(
    guild: discord.Guild,
    voice_channel: discord.VoiceChannel,
    text_channel: discord.TextChannel
) -> wavelink.Player:
    """
    Obtém o player existente ou cria um novo.
    
    Args:
        guild: Guild do Discord
        voice_channel: Canal de voz para conectar
        text_channel: Canal de texto para notificações
        
    Returns:
        Player do wavelink
    """
    player: wavelink.Player = cast(
        wavelink.Player,
        guild.voice_client or await voice_channel.connect(cls=wavelink.Player)
    )
    
    # Salva o canal de texto para notificações
    player.text_channel = text_channel
    
    # Move para o canal do usuário se necessário
    if player.channel != voice_channel:
        await player.move_to(voice_channel)
    
    return player


def get_player(guild: discord.Guild) -> Optional[wavelink.Player]:
    """
    Obtém o player atual da guild.
    
    Args:
        guild: Guild do Discord
        
    Returns:
        Player do wavelink ou None
    """
    return cast(wavelink.Player, guild.voice_client) if guild.voice_client else None


async def play_track(
    player: wavelink.Player,
    track: wavelink.Playable
) -> discord.Embed:
    """
    Toca uma track no player.
    
    Args:
        player: Player do wavelink
        track: Track para tocar
        
    Returns:
        Embed com informações da música
    """
    await player.play(track)
    return create_track_embed(track)


async def stop_player(guild: discord.Guild) -> bool:
    """
    Para o player e desconecta.
    
    Args:
        guild: Guild do Discord
        
    Returns:
        True se parou, False se não estava conectado
    """
    player = get_player(guild)
    
    if player:
        await player.disconnect()
        return True
    return False


async def pause_player(guild: discord.Guild) -> bool:
    """
    Pausa o player.
    
    Args:
        guild: Guild do Discord
        
    Returns:
        True se pausou, False se não estava tocando
    """
    player = get_player(guild)
    
    if player and player.playing:
        await player.pause(True)
        return True
    return False


async def resume_player(guild: discord.Guild) -> bool:
    """
    Retoma o player.
    
    Args:
        guild: Guild do Discord
        
    Returns:
        True se retomou, False se não estava pausado
    """
    player = get_player(guild)
    
    if player and player.paused:
        await player.pause(False)
        return True
    return False


async def skip_track(guild: discord.Guild) -> bool:
    """
    Pula a música atual.
    
    Args:
        guild: Guild do Discord
        
    Returns:
        True se pulou, False se não estava tocando
    """
    player = get_player(guild)
    
    if player and player.playing:
        await player.stop()
        return True
    return False


async def set_volume(guild: discord.Guild, level: int) -> Optional[int]:
    """
    Define o volume do player.
    
    Args:
        guild: Guild do Discord
        level: Nível de volume (0-100)
        
    Returns:
        Volume definido ou None se não conectado
    """
    player = get_player(guild)
    
    if not player:
        return None
    
    level = max(0, min(100, level))  # Clamp entre 0 e 100
    await player.set_volume(level)
    return level
