# 🌐 Sistema de Traduções

Este diretório contém o sistema de traduções do bot Tanya.

## 📁 Estrutura de Arquivos

```
translations/
├── config.json          # Configuração dos idiomas
├── pt_BR.json          # Traduções para Português Brasileiro
├── en_US.json          # Traduções para Inglês (padrão)
└── README.md           # Esta documentação
```

## ⚙️ Configuração (config.json)

```json
{
  "default_language": "en_US",           // Idioma padrão
  "supported_languages": [...],         // Lista de idiomas suportados
  "fallback_behavior": "return_original", // Comportamento quando tradução não encontrada
  "cache_translations": true,           // Cache em memória
  "auto_reload": false                  // Recarregamento automático
}
```

### Comportamentos de Fallback:

- `"return_original"`: Retorna texto original se não encontrar tradução
- `"return_default"`: Usa tradução do idioma padrão
- `"return_null"`: Retorna null (Discord mostra texto original)

## 📝 Formato dos Arquivos de Tradução

Cada arquivo de idioma segue esta estrutura:

```json
{
  "metadata": {
    "language": "pt_BR",
    "language_name": "Português Brasileiro",
    "version": "1.0.0",
    "last_updated": "2025-09-19",
    "translator": "Nome do Tradutor"
  },
  "commands": {
    "help": "ajuda",
    "create": "criar"
  },
  "descriptions": {
    "See information about the bot": "Veja informações sobre o bot"
  },
  "interface": {
    "Select a channel:": "Selecione um canal:"
  },
  "categories": {
    "utilities": "Útilidades"
  }
}
```

## 🔧 Como Adicionar Novos Idiomas

1. **Criar arquivo de tradução:**

   ```bash
   cp en_US.json novo_idioma.json
   ```

2. **Editar metadata:**

   ```json
   "metadata": {
     "language": "es_ES",
     "language_name": "Español",
     "translator": "Seu Nome"
   }
   ```

3. **Traduzir as strings:**

   ```json
   "commands": {
     "help": "ayuda",
     "create": "crear"
   }
   ```

4. **Adicionar ao config.json:**
   ```json
   {
     "code": "es_ES",
     "discord_locale": "spain_spanish",
     "name": "Español",
     "file": "es_ES.json",
     "enabled": true
   }
   ```

## 🎯 Mapeamento Discord Locale

| Discord Locale      | Código Interno |
| ------------------- | -------------- |
| `american_english`  | `en_US`        |
| `brazil_portuguese` | `pt_BR`        |
| `spain_spanish`     | `es_ES`        |

## 📊 Comandos Úteis

### No código Python:

```python
# Recarregar traduções
translator.reload_translations()

# Ver estatísticas
stats = translator.get_translation_stats()
print(f"PT-BR: {stats['pt_BR']} traduções")

# Verificar tradução específica
if translator.has_translation("pt_BR", "help"):
    print("Tradução existe!")

# Idiomas suportados
languages = translator.get_supported_languages()
```

## ✅ Boas Práticas

1. **Consistência**: Use a mesma terminologia em todas as traduções
2. **Contexto**: Mantenha `[Categoria]` nas descrições para clareza
3. **Formatação**: Preserve emojis e formatação especial
4. **Testes**: Teste as traduções no Discord antes de commitar
5. **Backup**: Sempre faça backup antes de editar arquivos

## 🚀 Exemplo de Uso

```python
# Carregar tradutor
translator = myCustomTranslator()

# Adicionar tradução temporária
translator.add_translation("pt_BR", "new_command", "novo_comando")

# Verificar suporte a idioma
languages = translator.get_supported_languages()
for lang in languages:
    if lang['enabled']:
        print(f"✅ {lang['name']}")
```

## 🐛 Resolução de Problemas

- **Arquivo não encontrado**: Verifique se o arquivo está no diretório correto
- **Erro de JSON**: Use um validador JSON online
- **Tradução não funciona**: Verifique se o idioma está habilitado no config
- **Performance**: Cache está habilitado por padrão para melhor performance
