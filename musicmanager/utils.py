"""
Utilitários para o MusicManager.
"""


def format_duration(ms: int) -> str:
    """
    Formata duração de milissegundos para mm:ss ou hh:mm:ss.
    
    Args:
        ms: Duração em milissegundos
        
    Returns:
        String formatada (ex: "3:45" ou "1:23:45")
    """
    seconds = ms // 1000
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    
    if hours:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    return f"{minutes}:{seconds:02d}"
