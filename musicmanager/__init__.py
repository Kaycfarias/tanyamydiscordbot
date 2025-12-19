"""
MusicManager - Wrapper simples para o spotdl.
"""

import asyncio
from typing import Dict, List, Optional, Tuple

from spotdl import Spotdl
from spotdl.types.song import Song
from spotdl.utils.config import SPOTIFY_OPTIONS
from spotdl.utils.spotify import SpotifyClient, SpotifyError
from spotdl.providers.audio import YouTubeMusic

# Instância global (singleton)
_manager_instance: Optional["MusicManager"] = None


def get_manager() -> "MusicManager":
    """Retorna a instância global do MusicManager."""
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = MusicManager()
    return _manager_instance


class MusicManager:
    """Wrapper simples para o spotdl."""
    
    def __init__(self):
        try:
            self._spotdl = Spotdl(
                client_id=SPOTIFY_OPTIONS["client_id"],
                client_secret=SPOTIFY_OPTIONS["client_secret"],
            )
        except SpotifyError:
            # Cliente já inicializado, reutiliza
            from spotdl.download.downloader import Downloader
            self._spotdl = Spotdl.__new__(Spotdl)
            self._spotdl.downloader = Downloader()
        
        # Provider para buscar URLs de streaming
        self._audio_provider = YouTubeMusic()
        
        # Cache de URLs de streaming (query -> url)
        self._stream_cache: Dict[str, str] = {}
        
        # Cache de Songs (query -> Song)
        self._song_cache: Dict[str, Song] = {}
        
        # Cliente Spotify para buscas customizadas
        self._spotify = SpotifyClient()
    
    def _search(self, query: str, limit: int = 10) -> List[Song]:
        """Busca músicas (síncrono). Retorna múltiplos resultados."""
        # Usa a API do Spotify diretamente com limite
        results = self._spotify.search(query, limit=limit, type="track")
        
        if not results or not results.get("tracks", {}).get("items"):
            return []
        
        songs = []
        for track in results["tracks"]["items"]:
            try:
                song = Song.from_url(f"https://open.spotify.com/track/{track['id']}")
                songs.append(song)
            except Exception:
                continue
        
        return songs
    
    async def search(self, query: str, limit: int = 10) -> List[Song]:
        """Busca músicas (assíncrono)."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._search, query, limit)
    
    def _download(self, song: Song) -> Optional[str]:
        """Baixa uma música. Retorna o caminho do arquivo."""
        _, path = self._spotdl.download(song)
        return str(path) if path else None
    
    async def download(self, song: Song) -> Optional[str]:
        """Baixa uma música (assíncrono)."""
        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(None, self._download, song)
    
    def _get_stream_url(self, song: Song) -> Optional[str]:
        """
        Obtém a URL de streaming direto do YouTube (sem baixar).
        Retorna a URL que pode ser usada com FFmpeg/discord.py.
        """
        # Busca a URL do vídeo no YouTube Music
        yt_url = self._audio_provider.search(song)
        if not yt_url:
            return None
        
        # Obtém os metadados com a URL de streaming
        info = self._audio_provider.get_download_metadata(yt_url, download=False)
        if info and "url" in info:
            return info["url"]
        
        # Fallback: retorna a URL do YouTube para o FFmpeg processar
        return yt_url
    
    async def get_stream_url(self, song: Song) -> Optional[str]:
        """
        Obtém a URL de streaming com cache.
        Use esta URL com discord.FFmpegPCMAudio para tocar em canal de voz.
        """
        cache_key = song.song_id or song.url
        
        # Verifica cache primeiro
        if cache_key in self._stream_cache:
            return self._stream_cache[cache_key]
        
        loop = asyncio.get_running_loop()
        url = await loop.run_in_executor(None, self._get_stream_url, song)
        
        # Salva no cache
        if url:
            self._stream_cache[cache_key] = url
        
        return url
    
    async def search_and_get_stream(self, query: str) -> Tuple[Optional[Song], Optional[str]]:
        """
        Busca uma música e retorna a Song + URL de streaming.
        Método conveniente para uso direto nos comandos.
        Aceita query string (do autocomplete ou digitada pelo usuário).
        """
        # Verifica se já temos a Song em cache
        if query in self._song_cache:
            song = self._song_cache[query]
        else:
            # Busca a música
            songs = await self.search(query)
            if not songs:
                return None, None
            song = songs[0]
            # Salva no cache usando a query como chave
            self._song_cache[query] = song
        
        stream_url = await self.get_stream_url(song)
        return song, stream_url
    
    def clear_cache(self) -> None:
        """Limpa o cache de URLs de streaming e songs."""
        self._stream_cache.clear()
        self._song_cache.clear()


__all__ = ["MusicManager", "get_manager"]
