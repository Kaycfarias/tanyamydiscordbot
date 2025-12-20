"""
Funções para criar embeds de música.
"""

from typing import Optional

import discord
import wavelink

from .utils import format_duration


def create_track_embed(
    track: wavelink.Playable,
    title: str = "🎵 Tocando agora"
) -> discord.Embed:
    """
    Cria um embed para uma track.
    
    Args:
        track: Track do wavelink
        title: Título do embed
        
    Returns:
        Embed do Discord
    """
    embed = discord.Embed(
        title=title,
        description=f"**{track.title}**",
        color=discord.Color.green()
    )
    embed.add_field(name="Artista", value=track.author, inline=True)
    embed.add_field(name="Duração", value=format_duration(track.length), inline=True)
    
    if track.artwork:
        embed.set_thumbnail(url=track.artwork)
    
    return embed


def create_nowplaying_embed(player: wavelink.Player) -> Optional[discord.Embed]:
    """
    Cria um embed com informações da música atual.
    
    Args:
        player: Player do wavelink
        
    Returns:
        Embed do Discord ou None se não estiver tocando
    """
    if not player or not player.current:
        return None
    
    track = player.current
    position = format_duration(player.position)
    duration = format_duration(track.length)
    
    embed = discord.Embed(
        title="🎵 Tocando agora",
        description=f"**{track.title}**",
        color=discord.Color.green()
    )
    embed.add_field(name="Artista", value=track.author, inline=True)
    embed.add_field(name="Progresso", value=f"{position} / {duration}", inline=True)
    embed.add_field(name="Volume", value=f"{player.volume}%", inline=True)
    
    if track.artwork:
        embed.set_thumbnail(url=track.artwork)
    
    return embed


def create_queue_embed(
    player: wavelink.Player,
    page: int = 1,
    per_page: int = 10
) -> Optional[discord.Embed]:
    """
    Cria um embed com a fila de músicas.
    
    Args:
        player: Player do wavelink
        page: Página atual (1-indexed)
        per_page: Itens por página
        
    Returns:
        Embed do Discord ou None se a fila estiver vazia
    """
    if not player or not player.queue:
        return None
    
    queue = player.queue
    total_pages = (len(queue) + per_page - 1) // per_page
    page = max(1, min(page, total_pages))
    
    start = (page - 1) * per_page
    end = start + per_page
    
    embed = discord.Embed(
        title="📋 Fila de Músicas",
        color=discord.Color.blue()
    )
    
    # Música atual
    if player.current:
        embed.add_field(
            name="🎵 Tocando agora",
            value=f"**{player.current.title}** - {player.current.author}",
            inline=False
        )
    
    # Lista da fila
    queue_list = []
    for i, track in enumerate(list(queue)[start:end], start=start + 1):
        duration = format_duration(track.length)
        queue_list.append(f"`{i}.` **{track.title}** - {track.author} [{duration}]")
    
    if queue_list:
        embed.add_field(
            name=f"Próximas ({len(queue)} músicas)",
            value="\n".join(queue_list),
            inline=False
        )
    
    embed.set_footer(text=f"Página {page}/{total_pages}")
    
    return embed
