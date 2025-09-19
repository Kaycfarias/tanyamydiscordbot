import discord
from discord import app_commands
import json
import os
from pathlib import Path
from typing import Dict, Optional


class myCustomTranslator(app_commands.Translator):
    """
    Sistema de tradução customizado baseado em arquivos JSON.
    Suporta múltiplos idiomas com carregamento dinâmico de traduções.
    """
    
    def __init__(self):
        self.translations_dir = Path(__file__).parent / "translations"
        self.config: Dict = {}
        self.translations_cache: Dict[str, Dict] = {}
        
        # Carregar configurações e traduções
        self._load_config()
        self._load_translations()

    def _load_config(self) -> None:
        """Carrega o arquivo de configuração das traduções."""
        config_path = self.translations_dir / "config.json"
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            print(f"⚠️ Arquivo de configuração não encontrado: {config_path}")
            # Configuração padrão
            self.config = {
                "default_language": "en_US",
                "supported_languages": [],
                "fallback_behavior": "return_original"
            }
        except json.JSONDecodeError as e:
            print(f"❌ Erro ao carregar configuração: {e}")
            self.config = {"default_language": "en_US", "supported_languages": []}

    def _load_translations(self) -> None:
        """Carrega todos os arquivos de tradução habilitados."""
        if not self.config.get("supported_languages"):
            return
            
        for lang_config in self.config["supported_languages"]:
            if not lang_config.get("enabled", True):
                continue
                
            lang_code = lang_config["code"]
            file_name = lang_config["file"]
            file_path = self.translations_dir / file_name
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    translation_data = json.load(f)
                    
                # Combinar todas as categorias em um dicionário único
                combined_translations = {}
                for category, translations in translation_data.items():
                    if category == "metadata":
                        continue
                    if isinstance(translations, dict):
                        combined_translations.update(translations)
                
                self.translations_cache[lang_code] = combined_translations
                print(f"✅ Traduções carregadas para {lang_config['name']}: {len(combined_translations)} items")
                
            except FileNotFoundError:
                print(f"⚠️ Arquivo de tradução não encontrado: {file_path}")
            except json.JSONDecodeError as e:
                print(f"❌ Erro ao carregar tradução {lang_code}: {e}")

    def _get_language_code_from_locale(self, locale: discord.Locale) -> Optional[str]:
        """Converte discord.Locale para código de idioma interno."""
        locale_mapping = {
            discord.Locale.american_english: "en_US",
            discord.Locale.brazil_portuguese: "pt_BR",
            # Adicione mais mapeamentos conforme necessário
        }
        return locale_mapping.get(locale)

    async def translate(
        self,
        string: app_commands.locale_str,
        locale: discord.Locale,
        context: app_commands.TranslationContext,
    ) -> Optional[str]:
        """
        Traduz strings usando os arquivos JSON de tradução.
        
        Args:
            string: String solicitando tradução
            locale: Idioma de destino
            context: Contexto da string (comando, descrição, etc.)
            
        Returns:
            String traduzida ou None se não houver tradução disponível
        """
        # Converter locale do Discord para código interno
        lang_code = self._get_language_code_from_locale(locale)
        if not lang_code:
            return None
            
        # Buscar tradução no cache
        translations = self.translations_cache.get(lang_code, {})
        message_str = string.message
        
        translation = translations.get(message_str)
        
        if translation:
            return translation
            
        # Fallback behavior configurado
        fallback = self.config.get("fallback_behavior", "return_original")
        if fallback == "return_original":
            return None  # Discord usará o texto original
        elif fallback == "return_default":
            default_lang = self.config.get("default_language", "en_US")
            default_translations = self.translations_cache.get(default_lang, {})
            return default_translations.get(message_str)
            
        return None

    def add_translation(self, lang_code: str, original: str, translated: str) -> bool:
        """
        Adiciona uma tradução ao cache (não persiste no arquivo).
        
        Args:
            lang_code: Código do idioma (ex: "pt_BR")
            original: Texto original
            translated: Texto traduzido
            
        Returns:
            True se adicionado com sucesso
        """
        if lang_code not in self.translations_cache:
            self.translations_cache[lang_code] = {}
            
        self.translations_cache[lang_code][original] = translated
        return True

    def reload_translations(self) -> None:
        """Recarrega todas as traduções dos arquivos JSON."""
        self.translations_cache.clear()
        self._load_config()
        self._load_translations()

    def get_supported_languages(self) -> list:
        """Retorna lista de idiomas suportados."""
        return [
            {
                "code": lang["code"],
                "name": lang["name"],
                "enabled": lang.get("enabled", True)
            }
            for lang in self.config.get("supported_languages", [])
        ]

    def get_translation_stats(self) -> Dict[str, int]:
        """Retorna estatísticas de traduções por idioma."""
        return {
            lang_code: len(translations)
            for lang_code, translations in self.translations_cache.items()
        }

    def has_translation(self, lang_code: str, original: str) -> bool:
        """Verifica se existe tradução específica."""
        return original in self.translations_cache.get(lang_code, {})
