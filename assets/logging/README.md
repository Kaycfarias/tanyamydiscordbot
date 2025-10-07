# 🎨 Sistema de Logging com Cores - Tanya Bot

Sistema de logging personalizado com cores para terminal e logging estruturado para arquivos.

## 📁 Estrutura

```
assets/logging/
├── __init__.py          # Configuração principal
├── colors.py            # Códigos de cores ANSI
├── formatters.py        # Formatadores personalizados
├── demo.py             # Demonstração das funcionalidades
└── README.md           # Esta documentação
```

## 🚀 Uso Básico

### Configuração Simples

```python
from assets.logging import setup_logging, get_logger

# Configurar o sistema (uma vez no main.py)
setup_logging()

# Obter logger em qualquer módulo
logger = get_logger(__name__)

# Usar o logger
logger.info("🚀 Bot iniciando...")
logger.error("❌ Erro encontrado")
```

### Configuração Avançada

```python
from assets.logging import setup_logging, set_discord_logging_level, set_debug_mode
import logging

# Configuração personalizada
setup_logging(
    level=logging.DEBUG,
    console_format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    log_file="logs/bot.log"
)

# Configurar nível do Discord.py
set_discord_logging_level(logging.WARNING)

# Ativar modo debug
set_debug_mode(True)
```

## 🎨 Cores Disponíveis

### Cores Básicas

- 🔴 **Vermelho** (`Colors.RED`) - Para erros
- 🟢 **Verde** (`Colors.GREEN`) - Para sucessos
- 🟡 **Amarelo** (`Colors.YELLOW`) - Para avisos
- 🔵 **Azul** (`Colors.BLUE`) - Para informações
- 🟣 **Magenta** (`Colors.MAGENTA`) - Para destaques
- 🔷 **Ciano** (`Colors.CYAN`) - Para debug
- ⚫ **Cinza** (`Colors.GRAY`) - Para texto secundário

### Cores Brilhantes

- 🔴 **Vermelho Brilhante** (`Colors.BRIGHT_RED`) - Para erros críticos
- 🟢 **Verde Brilhante** (`Colors.BRIGHT_GREEN`) - Para sucessos importantes
- 🟡 **Amarelo Brilhante** (`Colors.BRIGHT_YELLOW`) - Para avisos importantes
- 🔵 **Azul Brilhante** (`Colors.BRIGHT_BLUE`) - Para informações importantes

### Métodos de Conveniência

```python
from assets.logging.colors import Colors

# Aplicar cores rapidamente
print(Colors.success("✅ Operação concluída"))
print(Colors.error("❌ Falha na operação"))
print(Colors.warning("⚠️ Atenção necessária"))
print(Colors.info("ℹ️ Informação importante"))
print(Colors.debug("🔍 Dados de debug"))
print(Colors.muted("💬 Texto secundário"))
```

## 🎯 Níveis de Log com Cores

| Nível      | Cor                            | Quando Usar                                 |
| ---------- | ------------------------------ | ------------------------------------------- |
| `DEBUG`    | 🔷 Ciano                       | Informações detalhadas para desenvolvedores |
| `INFO`     | 🟢 Verde Brilhante             | Informações gerais de funcionamento         |
| `WARNING`  | 🟡 Amarelo Brilhante           | Situações que precisam atenção              |
| `ERROR`    | 🔴 Vermelho Brilhante          | Erros que não param o programa              |
| `CRITICAL` | 🟣 Magenta Brilhante + Negrito | Erros críticos                              |

## 🎭 Emojis Coloridos Automaticamente

O sistema automaticamente colore estes emojis:

- 🚀 **Azul Brilhante** - Inicialização
- ✅ **Verde Brilhante** - Sucesso
- ❌ **Vermelho Brilhante** - Erro
- ⚠️ **Amarelo Brilhante** - Aviso
- 👋 **Ciano Brilhante** - Despedida
- 🔧 **Amarelo** - Configuração
- 📦 **Azul** - Pacotes/Módulos
- 🗂️ **Magenta** - Estruturas/Diretórios
- 🤖 **Magenta Brilhante** - Bot/Sistema
- 🎉 **Verde Brilhante** - Celebração

## 📝 Exemplos Práticos

### Logging de Inicialização

```python
logger = get_logger(__name__)

logger.info("🚀 Iniciando sistema...")
logger.info("🔧 Configurando componentes...")
logger.info("📦 Carregando módulos...")
logger.info("✅ Sistema pronto!")
```

### Estrutura em Árvore

```python
logger.info("🗂️ Componentes carregados:")
logger.info("   ├── 📁 commands")
logger.info("   │   ├── ✅ embed.py")
logger.info("   │   └── ✅ util.py")
logger.info("   └── ⚡ events")
logger.info("       └── ✅ event.py")
```

### Tratamento de Erros

```python
try:
    # Operação perigosa
    pass
except Exception as e:
    logger.error(f"❌ Falha na operação: {e}")
    logger.debug(f"🔍 Detalhes técnicos: {traceback.format_exc()}")
```

## ⚙️ Funcionalidades Avançadas

### Controle de Debug

```python
from assets.logging import set_debug_mode

# Ativar logs de debug
set_debug_mode(True)

# Desativar logs de debug
set_debug_mode(False)
```

### Configuração do Discord.py

```python
from assets.logging import set_discord_logging_level
import logging

# Reduzir logs do discord.py
set_discord_logging_level(logging.WARNING)

# Logs detalhados do discord.py
set_discord_logging_level(logging.DEBUG)
```

### Logger Personalizado

```python
from assets.logging import get_logger

# Logger específico para um módulo
logger = get_logger("meu_modulo")

# Logger com nome customizado
logger = get_logger("sistema.database")
```

## 📁 Arquivos de Log

- **Console**: Colorido com emojis destacados
- **Arquivo**: Texto simples sem cores (para compatibilidade)
- **Localização**: `bot.log` (configurável)
- **Codificação**: UTF-8 para suporte a emojis

## 🔧 Demonstração

Execute a demonstração para ver todas as funcionalidades:

```bash
python assets/logging/demo.py
```

## 📚 API Reference

### Funções Principais

- `setup_logging(level, console_format, file_format, ...)` - Configura o sistema
- `get_logger(name)` - Retorna logger configurado
- `set_debug_mode(enabled)` - Controla modo debug
- `set_discord_logging_level(level)` - Configura logs do Discord.py

### Classes

- `Colors` - Códigos de cores ANSI e métodos de conveniência
- `ColoredFormatter` - Formatter com cores para console
- `PlainFormatter` - Formatter simples para arquivos

## 🎨 Personalização

O sistema é totalmente personalizável:

- **Cores**: Modifique `colors.py`
- **Formatação**: Ajuste `formatters.py`
- **Configuração**: Customize `__init__.py`
- **Emojis**: Adicione novos mapeamentos em `ColoredFormatter`

---

**💡 Dica**: As cores só aparecem em terminais compatíveis. Em ambientes sem suporte a cores, o texto aparece normalmente sem formatação.
