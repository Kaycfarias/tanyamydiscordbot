import os
import sys
import logging
import asyncio
from pathlib import Path
from dotenv import load_dotenv

import discord
from discord.ext import commands

from assets.loader.cogsloader import cogsLoader
from assets.translations.translator import myCustomTranslator

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

# Logging do discord em nível INFO (inclui confirmação de voz)
logging.getLogger('discord.client').setLevel(logging.INFO)

# Carregar variáveis de ambiente
load_dotenv()

# Validar configurações necessárias
TOKEN = os.getenv("TOKEN")
CHATGPT_KEY = os.getenv("CHATGPT_KEY")

if not TOKEN:
    logging.error("TOKEN não encontrado no arquivo .env")
    sys.exit(1)


class TanyaBot(commands.Bot):
    """
    Classe principal do bot Tanya.
    Bot especializado em criação de embeds e moderação.
    """
    
    def __init__(self):
        # Configurar intents necessários
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True
        intents.voice_states = True  # Para funcionalidades de voz
        
        super().__init__(
            command_prefix=">>",
            case_insensitive=True,
            intents=intents,
            help_command=None,
            description="Bot especializado em criação de embeds e moderação",
        )
        
        # Logger para esta classe
        self.logger = logging.getLogger(__name__)
        
        # Configurações do bot
        self.chatgpt_key = CHATGPT_KEY
        self.version = "2.0.0"
        
    async def setup_hook(self):
        """Hook executado durante a inicialização do bot."""
        try:
            self.logger.info("🚀 Iniciando bot Tanya...")
            
            # Configurar tradutor
            translator = myCustomTranslator()
            await self.tree.set_translator(translator)
            self.logger.info("✅ Sistema de tradução configurado")
            
            # Carregar componentes
            success = await cogsLoader(self)
            if not success:
                self.logger.error("❌ Falha ao carregar componentes")
                return
                
            self.logger.info("✅ Componentes carregados com sucesso")
            
        except Exception as e:
            self.logger.error(f"❌ Erro durante setup_hook: {e}")
            raise
        
    async def close(self):
        """Cleanup quando o bot está sendo desligado."""
        self.logger.info("👋 Desligando bot...")
        await super().close()

    def run_bot(self):
        """Executa o bot com tratamento de erros."""
        try:
            self.run(TOKEN, log_handler=None)  # Usar nosso logging customizado
        except discord.LoginFailure:
            self.logger.error("❌ Token inválido! Verifique o arquivo .env")
            sys.exit(1)
        except discord.PrivilegedIntentsRequired:
            self.logger.error("❌ Intents privilegiados necessários! Configure no Discord Developer Portal")
            sys.exit(1)
        except Exception as e:
            self.logger.error(f"❌ Erro inesperado: {e}")
            sys.exit(1)


def main():
    """Função principal para inicializar o bot."""
    # Verificar versão do Python
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ é necessário!")
        sys.exit(1)
    
    # Verificar se estamos no diretório correto
    if not Path("components").exists():
        logging.error("❌ Diretório 'components' não encontrado!")
        logging.error("Execute o bot a partir do diretório raiz do projeto")
        sys.exit(1)
    
    # Criar e executar o bot
    logging.info("🚀 Inicializando Tanya Bot...")
    
    try:
        bot = TanyaBot()
        bot.run_bot()
    except KeyboardInterrupt:
        logging.info("👋 Bot interrompido pelo usuário")
    except Exception as e:
        logging.error(f"❌ Erro fatal durante execução: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()