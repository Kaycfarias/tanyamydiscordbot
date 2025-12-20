"""
Funções de busca e cache.
"""

import asyncio
from typing import Dict, List, Optional

import wavelink


async def search_tracks(
    query: str,
    limit: int = 5,
    timeout: float = 2.0
) -> List[wavelink.Playable]:
    """
    Busca tracks no Lavalink.
    
    Args:
        query: Termo de busca ou URL
        limit: Número máximo de resultados
        timeout: Timeout em segundos
        
    Returns:
        Lista de tracks encontradas
    """
    try:
        tracks = await asyncio.wait_for(
            wavelink.Playable.search(query),
            timeout=timeout
        )
        return tracks[:limit] if tracks else []
    except asyncio.TimeoutError:
        return []
    except Exception:
        return []


class SearchCache:
    """
    Cache para resultados de busca.
    
    Armazena tracks buscadas para reutilização no autocomplete → play.
    """
    
    def __init__(self, max_size: int = 100):
        """
        Inicializa o cache.
        
        Args:
            max_size: Tamanho máximo do cache
        """
        self._cache: Dict[str, wavelink.Playable] = {}
        self._max_size = max_size
    
    def get(self, key: str) -> Optional[wavelink.Playable]:
        """
        Obtém uma track do cache.
        
        Args:
            key: Chave de busca
            
        Returns:
            Track ou None se não encontrada
        """
        return self._cache.get(key)
    
    def set(self, key: str, track: wavelink.Playable) -> None:
        """
        Adiciona uma track ao cache.
        
        Args:
            key: Chave de busca
            track: Track para armazenar
        """
        # Remove o item mais antigo se atingir o limite
        if len(self._cache) >= self._max_size:
            first_key = next(iter(self._cache))
            del self._cache[first_key]
        
        self._cache[key] = track
    
    def clear(self) -> None:
        """Limpa o cache."""
        self._cache.clear()
    
    def __contains__(self, key: str) -> bool:
        """Verifica se a chave existe no cache."""
        return key in self._cache
    
    def __len__(self) -> int:
        """Retorna o tamanho do cache."""
        return len(self._cache)
