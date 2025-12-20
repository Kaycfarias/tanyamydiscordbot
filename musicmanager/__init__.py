"""
MusicManager - Gerenciador de música usando Lavalink/Wavelink.

Estrutura:
    - utils.py: Funções utilitárias (formatação)
    - embeds.py: Criação de embeds
    - player.py: Controle do player (play, pause, stop, etc.)
    - search.py: Busca e cache de tracks
"""

# Utils
from .utils import format_duration

# Embeds
from .embeds import (
    create_track_embed,
    create_nowplaying_embed,
    create_queue_embed,
)

# Player
from .player import (
    get_or_create_player,
    get_player,
    play_track,
    stop_player,
    pause_player,
    resume_player,
    skip_track,
    set_volume,
)

# Search
from .search import (
    search_tracks,
    SearchCache,
)


__all__ = [
    # Utils
    "format_duration",
    # Embeds
    "create_track_embed",
    "create_nowplaying_embed",
    "create_queue_embed",
    # Player
    "get_or_create_player",
    "get_player",
    "play_track",
    "stop_player",
    "pause_player",
    "resume_player",
    "skip_track",
    "set_volume",
    # Search
    "search_tracks",
    "SearchCache",
]
