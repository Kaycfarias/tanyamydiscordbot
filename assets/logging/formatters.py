"""
Formatadores personalizados para logging do bot Tanya.
Inclui formatação com cores e emojis para diferentes níveis de log.
"""

import logging
from .colors import Colors


class ColoredFormatter(logging.Formatter):
    """Formatter personalizado com cores para diferentes níveis de log."""
    
    # Mapeamento de níveis para cores
    LEVEL_COLORS = {
        logging.DEBUG: Colors.CYAN,
        logging.INFO: Colors.BRIGHT_GREEN,
        logging.WARNING: Colors.BRIGHT_YELLOW,
        logging.ERROR: Colors.BRIGHT_RED,
        logging.CRITICAL: Colors.BRIGHT_MAGENTA + Colors.BOLD,
    }
    
    # Mapeamento de emojis para cores
    EMOJI_COLORS = {
        '🚀': Colors.BRIGHT_BLUE,
        '✅': Colors.BRIGHT_GREEN,
        '❌': Colors.BRIGHT_RED,
        '⚠️': Colors.BRIGHT_YELLOW,
        '👋': Colors.BRIGHT_CYAN,
        '🔧': Colors.YELLOW,
        '📦': Colors.BLUE,
        '🗂️': Colors.MAGENTA,
        '📁': Colors.BLUE,
        '⚡': Colors.YELLOW,
        '🤖': Colors.BRIGHT_MAGENTA,
        '👤': Colors.CYAN,
        '🆔': Colors.GRAY,
        '📋': Colors.BLUE,
        '🌐': Colors.GREEN,
        '👥': Colors.CYAN,
        '📺': Colors.BLUE,
        '⏰': Colors.YELLOW,
        '🎉': Colors.BRIGHT_GREEN,
    }
    
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
    
    def format(self, record):
        # Fazer uma cópia do record para não alterar o original
        record_copy = logging.makeLogRecord(record.__dict__)
        
        # Aplicar cor ao nível de log
        level_color = self.LEVEL_COLORS.get(record_copy.levelno, Colors.WHITE)
        record_copy.levelname = Colors.colorize(record_copy.levelname, level_color)
        
        # Colorir emojis na mensagem
        if hasattr(record_copy, 'msg') and isinstance(record_copy.msg, str):
            message = record_copy.msg
            
            # Aplicar cores aos emojis
            for emoji, color in self.EMOJI_COLORS.items():
                if emoji in message:
                    colored_emoji = Colors.colorize(emoji, color)
                    message = message.replace(emoji, colored_emoji)
            
            record_copy.msg = message
        
        return super().format(record_copy)


class PlainFormatter(logging.Formatter):
    """Formatter simples sem cores para arquivos de log."""
    
    def __init__(self, fmt=None, datefmt=None):
        super().__init__(fmt, datefmt)
    
    def format(self, record):
        # Usar o formatter padrão sem modificações
        return super().format(record)