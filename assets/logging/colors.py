"""
Sistema de cores para logging do bot Tanya.
Códigos ANSI para colorir saídas no terminal.
"""


class Colors:
    """Códigos de cores ANSI para terminal."""
    RESET = '\033[0m'
    BOLD = '\033[1m'
    
    # Cores básicas
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GRAY = '\033[90m'
    
    # Cores brilhantes
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'
    BRIGHT_WHITE = '\033[97m'

    @classmethod
    def colorize(cls, text: str, color: str) -> str:
        """Aplica cor ao texto e reseta no final."""
        return f"{color}{text}{cls.RESET}"

    @classmethod
    def success(cls, text: str) -> str:
        """Texto em verde brilhante (sucesso)."""
        return cls.colorize(text, cls.BRIGHT_GREEN)

    @classmethod
    def error(cls, text: str) -> str:
        """Texto em vermelho brilhante (erro)."""
        return cls.colorize(text, cls.BRIGHT_RED)

    @classmethod
    def warning(cls, text: str) -> str:
        """Texto em amarelo brilhante (aviso)."""
        return cls.colorize(text, cls.BRIGHT_YELLOW)

    @classmethod
    def info(cls, text: str) -> str:
        """Texto em azul brilhante (informação)."""
        return cls.colorize(text, cls.BRIGHT_BLUE)

    @classmethod
    def debug(cls, text: str) -> str:
        """Texto em ciano (debug)."""
        return cls.colorize(text, cls.CYAN)

    @classmethod
    def muted(cls, text: str) -> str:
        """Texto em cinza (texto secundário)."""
        return cls.colorize(text, cls.GRAY)