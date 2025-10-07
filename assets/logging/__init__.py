"""
Configuração do sistema de logging do bot Tanya.
Configura handlers para console (com cores) e arquivo (sem cores).
"""

import logging
import sys
from pathlib import Path
from .formatters import ColoredFormatter, PlainFormatter


def setup_logging(
    level: int = logging.INFO,
    console_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    file_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    console_datefmt: str = "%H:%M:%S",
    file_datefmt: str = "%Y-%m-%d %H:%M:%S",
    log_file: str = "bot.log"
) -> logging.Logger:
    """
    Configura o sistema de logging com cores para console e arquivo simples.
    
    Args:
        level: Nível de logging (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        console_format: Formato para saída do console
        file_format: Formato para arquivo de log
        console_datefmt: Formato de data/hora para console
        file_datefmt: Formato de data/hora para arquivo
        log_file: Caminho para o arquivo de log
        
    Returns:
        Logger principal configurado
    """
    # Logger principal
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    
    # Limpar handlers existentes para evitar duplicação
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Formatter colorido para console
    console_formatter = ColoredFormatter(
        fmt=console_format,
        datefmt=console_datefmt
    )
    
    # Formatter simples para arquivo
    file_formatter = PlainFormatter(
        fmt=file_format,
        datefmt=file_datefmt
    )
    
    # Handler para console (stdout com cores)
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(level)
    
    # Handler para arquivo (sem cores)
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)
    
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(level)
    
    # Adicionar handlers ao logger principal
    root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)
    
    return root_logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Retorna um logger configurado.
    
    Args:
        name: Nome do logger (se None, usa o módulo chamador)
        
    Returns:
        Logger configurado
    """
    return logging.getLogger(name)


def set_discord_logging_level(level: int = logging.WARNING):
    """
    Configura o nível de logging para bibliotecas do Discord.
    
    Args:
        level: Nível de logging para discord.py
    """
    # Configurar loggers do discord.py
    logging.getLogger('discord').setLevel(level)
    logging.getLogger('discord.client').setLevel(level)
    logging.getLogger('discord.gateway').setLevel(level)
    logging.getLogger('discord.http').setLevel(level)


def set_debug_mode(enabled: bool = True):
    """
    Ativa/desativa o modo debug.
    
    Args:
        enabled: Se True, ativa logging DEBUG
    """
    level = logging.DEBUG if enabled else logging.INFO
    logging.getLogger().setLevel(level)
    
    # Atualizar handlers
    for handler in logging.getLogger().handlers:
        handler.setLevel(level)