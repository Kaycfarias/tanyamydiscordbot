"""
Demonstração do sistema de logging com cores do bot Tanya.
Execute este arquivo para ver as cores em ação.
"""

import sys
from pathlib import Path

# Adicionar diretório do projeto ao path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from assets.logging import setup_logging, get_logger, set_debug_mode
from assets.logging.colors import Colors


def demo_colors():
    """Demonstra as cores disponíveis."""
    print("\n🎨 Demonstração das Cores Disponíveis:")
    print("=" * 50)
    
    # Cores básicas
    print(f"{Colors.RED}Vermelho{Colors.RESET} - Para erros")
    print(f"{Colors.GREEN}Verde{Colors.RESET} - Para sucessos")
    print(f"{Colors.YELLOW}Amarelo{Colors.RESET} - Para avisos")
    print(f"{Colors.BLUE}Azul{Colors.RESET} - Para informações")
    print(f"{Colors.MAGENTA}Magenta{Colors.RESET} - Para destaques")
    print(f"{Colors.CYAN}Ciano{Colors.RESET} - Para debug")
    print(f"{Colors.GRAY}Cinza{Colors.RESET} - Para texto secundário")
    
    # Cores brilhantes
    print(f"{Colors.BRIGHT_RED}Vermelho Brilhante{Colors.RESET} - Para erros críticos")
    print(f"{Colors.BRIGHT_GREEN}Verde Brilhante{Colors.RESET} - Para sucessos importantes")
    print(f"{Colors.BRIGHT_YELLOW}Amarelo Brilhante{Colors.RESET} - Para avisos importantes")
    print(f"{Colors.BRIGHT_BLUE}Azul Brilhante{Colors.RESET} - Para informações importantes")
    
    # Métodos de conveniência
    print(f"\n📋 Métodos de Conveniência:")
    print(Colors.success("✅ Texto de sucesso"))
    print(Colors.error("❌ Texto de erro"))
    print(Colors.warning("⚠️ Texto de aviso"))
    print(Colors.info("ℹ️ Texto de informação"))
    print(Colors.debug("🔍 Texto de debug"))
    print(Colors.muted("💬 Texto secundário"))


def demo_logging():
    """Demonstra o sistema de logging."""
    print("\n📝 Demonstração do Sistema de Logging:")
    print("=" * 50)
    
    # Configurar logging
    setup_logging()
    logger = get_logger("demo")
    
    # Diferentes níveis de log
    logger.debug("🔍 Mensagem de debug")
    logger.info("ℹ️ Mensagem informativa")
    logger.warning("⚠️ Mensagem de aviso")
    logger.error("❌ Mensagem de erro")
    logger.critical("🚨 Mensagem crítica")
    
    # Mensagens com emojis coloridos
    logger.info("🚀 Bot iniciando...")
    logger.info("✅ Componente carregado")
    logger.info("📦 Sistema configurado")
    logger.info("🔧 Ferramentas preparadas")
    logger.info("🎉 Tudo pronto!")
    
    # Estrutura em árvore (como no cogsloader)
    logger.info("🗂️ Estrutura do projeto:")
    logger.info("   ├── 📁 assets")
    logger.info("   │   ├── ✅ logging")
    logger.info("   │   └── ✅ loader")
    logger.info("   └── 📁 components")
    logger.info("       ├── ✅ commands")
    logger.info("       └── ✅ events")


def demo_debug_mode():
    """Demonstra o modo debug."""
    print("\n🔍 Demonstração do Modo Debug:")
    print("=" * 50)
    
    logger = get_logger("debug_demo")
    
    # Ativar modo debug
    set_debug_mode(True)
    logger.debug("🔍 Modo debug ATIVADO - esta mensagem aparece")
    
    # Desativar modo debug
    set_debug_mode(False)
    logger.debug("🔍 Modo debug DESATIVADO - esta mensagem NÃO aparece")
    logger.info("ℹ️ Modo normal - esta mensagem sempre aparece")


def main():
    """Função principal da demonstração."""
    print(Colors.success("🎨 Sistema de Logging com Cores - Tanya Bot"))
    print(Colors.muted("Demonstração das funcionalidades de logging"))
    
    try:
        demo_colors()
        demo_logging()
        demo_debug_mode()
        
        print(f"\n{Colors.success('🎉 Demonstração concluída com sucesso!')}")
        print(Colors.info("💡 As cores aparecem apenas no terminal, não nos arquivos de log"))
        print(Colors.muted("📁 Verifique o arquivo 'bot.log' para ver os logs sem cores"))
        
    except Exception as e:
        print(Colors.error(f"❌ Erro durante demonstração: {e}"))
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())