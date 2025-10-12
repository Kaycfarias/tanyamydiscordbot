# 🤖 Tanya - Bot Discord Profissional

Bot Discord moderno e robusto especializado em criação avançada de embeds, desenvolvido em Python 3.8+ com discord.py 2.5+.

## ✨ Características Principais

- 🎨 **Sistema de Embeds Avançado**: Interface visual completa para criação de embeds profissionais
- 🏗️ **Arquitetura Modular**: Sistema de cogs com carregamento inteligente e hot-reload
- 🎯 **Interface Intuitiva**: Views, botões, dropdowns e modais para UX fluida
- 🌐 **Sistema de Webhooks**: Envio personalizado com avatares e nomes customizados
- 🌍 **Localização Completa**: Suporte nativo para Português Brasileiro e Inglês
- ⚡ **Comandos Slash**: API moderna do Discord com auto-complete
- 🎙️ **Suporte a Voz**: Funcionalidades de áudio com PyNaCl
- 🎨 **Logging Colorido**: Sistema avançado com cores e emojis
- 🔄 **Status Dinâmico**: Rotação automática de atividades do bot
- 🛡️ **Tratamento de Erros**: Sistema robusto de error handling

## 🚀 Instalação e Configuração

### 📋 Pré-requisitos

- **Python**: 3.8+ (recomendado 3.10+)
- **discord.py**: 2.5.2+
- **Token Discord**: Bot com permissões apropriadas
- **Terminal**: Suporte a cores ANSI (opcional para logs coloridos)

### ⚙️ Instalação Rápida

1. **Clone e acesse o projeto:**

```bash
git clone https://github.com/Kaycfarias/tanyamydiscordbot
cd tanyamydiscordbot
```

2. **Instale dependências:**

```bash
# Instalação padrão
pip install -r requirements.txt

# Ou com venv (recomendado)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou: venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

3. **Configuração de ambiente:**
   Crie arquivo `.env` na raiz do projeto:

```env
# Obrigatório
TOKEN=seu_token_do_bot_discord

# Opcional (para comando GPT)
CHATGPT_KEY=sua_chave_openai_api

# Opcional (configurações de logging)
DEBUG_MODE=false
LOG_LEVEL=INFO
```

4. **Inicialização:**

```bash
python main.py
```

### 🔧 Configuração Avançada

**Permissões Requeridas no Discord:**

- `Send Messages`
- `Use Slash Commands`
- `Manage Messages`
- `Embed Links`
- `Manage Webhooks`
- `Connect` (para comandos de voz)

**Variáveis de Ambiente Opcionais:**

```env
# Logging personalizado
CONSOLE_COLORS=true
LOG_FILE=bot.log
EMOJI_LOGS=true

# Performance
AUTO_SYNC=true
COMMAND_SYNC_GUILDS=guild_id_1,guild_id_2
```

## 🏗️ Arquitetura e Sistema

### 📂 Estrutura do Projeto

```
📁 assets/
├── 📁 logging/          # 🎨 Sistema de logging colorido
│   ├── __init__.py      # Configuração principal
│   ├── colors.py        # Códigos ANSI e helpers
│   ├── formatters.py    # Formatadores customizados
│   └── README.md        # Documentação do sistema
├── 📁 translations/     # 🌍 Sistema de localização
│   ├── translator.py    # Engine de tradução
│   ├── pt_BR.json      # Português brasileiro
│   └── en_US.json      # Inglês
└── cogsloader.py        # � Carregador automático

�📁 components/
├── 📁 commands/         # ⚡ Comandos slash por categoria
│   ├── embed.py         # Sistema de embeds
│   ├── user.py          # Informações do usuário
│   ├── util.py          # Utilitários gerais
│   ├── gpt.py           # Integração ChatGPT
│   └── sync.py          # Sincronização de comandos
├── 📁 events/           # 🎯 Manipuladores de eventos
│   ├── event.py         # Eventos principais + status
│   └── errors.py        # Tratamento de erros

📁 embedcreator/         # 🎨 Sistema avançado de embeds
├── defaultview.py       # Interface principal
└── 📁 components/       # Componentes UI modulares
    ├── buttonview.py    # Views de botões
    ├── 📁 color/        # Sistema de cores
    ├── 📁 field/        # Gerenciamento de fields
    ├── 📁 modals/       # Formulários de entrada
    └── 📁 finalysend/   # Sistema de envio final
```

### 🔧 Componentes Principais

- **Sistema de Logging**: Logs coloridos com emojis e formatação profissional
- **Engine de Tradução**: Suporte multi-idioma com contexto preservado
- **Carregador Modular**: Auto-discovery e hot-reload de componentes
- **Sistema de Embeds**: Interface visual completa para criação avançada
- **Gerenciamento de Status**: Rotação automática de atividades do bot

## 🎯 Funcionalidades e Recursos

### 🎨 Sistema de Logging Colorido

```bash
🚀 [2024-01-15 10:30:25] [INFO] Bot iniciado com sucesso!
✅ [2024-01-15 10:30:26] [INFO] 10/10 componentes carregados
🎉 [2024-01-15 10:30:27] [INFO] Tanya está online!
```

**Características:**

- Logs coloridos com códigos ANSI
- Emojis contextuais para diferentes tipos de log
- Saída dual: colorida no console, limpa em arquivo
- Configurável via variáveis de ambiente

### 🔄 Sistema de Status Dinâmico

O bot rotaciona automaticamente entre diferentes atividades:

- 🎮 Jogando: "Criando embeds incríveis!"
- 🎵 Ouvindo: "Comandos dos usuários"
- 📺 Assistindo: "O servidor crescer"
- 🏃 Competindo: "Para ser o melhor bot!"

**Configuração:** Rotação a cada 15 minutos com limpeza automática.

### 🎨 Sistema Avançado de Embeds

**Interface Completa:**

- Criação visual de até 10 embeds por sessão
- Editor interativo: campos, cores, imagens, rodapés
- Preview em tempo real com validação
- Sistema de cópia via URL de mensagem
- Envio multicanal e webhook personalizado

**Componentes Modulares:**

- Views hierárquicas com estado preservado
- Modals para entrada de texto complexa
- Dropdowns para seleção de opções
- Botões com feedback visual

### ⚡ Comandos Slash Disponíveis

| Comando                  | Descrição                          | Uso                |
| ------------------------ | ---------------------------------- | ------------------ |
| `/embed create advanced` | Criador avançado de embeds         | Interface completa |
| `/ajuda`                 | Central de ajuda e documentação    | Lista comandos     |
| `/info servidor`         | Informações detalhadas do servidor | Analytics          |
| `/user info`             | Dados do usuário/membro            | Perfil detalhado   |
| `/util ping`             | Latência e performance             | Diagnóstico        |
| `/gpt ask`               | Integração ChatGPT (opcional)      | IA conversacional  |
| `<prefix>sync`           | Sincronização de comandos          | Admin only         |

### 🌍 Sistema de Localização

**Idiomas Suportados:**

- 🇧🇷 **Português Brasileiro** (nativo)
- 🇺🇸 **Inglês** (completo)

**Características:**

- Tradução automática baseada no idioma do Discord
- Contexto preservado para comandos técnicos
- Arquivos JSON organizados por categorias
- Fallback inteligente para strings não traduzidas

## 🛠️ Guia de Desenvolvimento

### 🔧 Configuração do Ambiente de Desenvolvimento

**Estrutura Recomendada:**

```bash
# Clone e setup
git clone https://github.com/Kaycfarias/tanyamydiscordbot
cd tanyamydiscordbot
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Teste o ambiente
python main.py
```

### ➕ Adicionando Novos Comandos

**Estrutura Padrão:**

```python
from discord.ext import commands
from discord import app_commands
from discord.app_commands import locale_str as _T

class MeuComando(commands.GroupCog, group_name="meugrupo"):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="teste", description=_T("Comando de teste"))
    @app_commands.guild_only()
    async def meu_comando(self, interaction):
        await interaction.response.send_message("Olá!")

async def setup(bot):
    await bot.add_cog(MeuComando(bot))
```

**Passos:**

1. Crie arquivo em `components/commands/meucomando.py`
2. Implemente a classe seguindo o padrão
3. Use `_T()` para strings traduzíveis
4. Reinicie o bot - carregamento automático

### 🎨 Criando Componentes UI

**Views Personalizadas:**

```python
import discord
from discord.ui import View, Button, Select

class MinhaView(View):
    def __init__(self, embeds, bot, defaultView):
        super().__init__(timeout=None)
        self.embeds = embeds
        self.bot = bot
        self.defaultView = defaultView

    @Button(label="Minha Ação", style=discord.ButtonStyle.primary)
    async def meu_botao(self, interaction, button):
        # Lógica do botão
        await interaction.response.edit_message(view=self)
```

**Modais para Entrada:**

```python
class MeuModal(discord.ui.Modal):
    def __init__(self):
        super().__init__(title="Meu Formulário")

    texto = discord.ui.TextInput(
        label="Título",
        placeholder="Digite aqui...",
        max_length=256
    )

    async def on_submit(self, interaction):
        await interaction.response.send_message(f"Recebido: {self.texto.value}")
```

### 🎯 Sistema de Logging

**Usando o Logger:**

```python
from assets.logging import get_logger

logger = get_logger(__name__)

# Diferentes níveis
logger.info("Informação geral")
logger.success("Operação bem-sucedida")  # Verde com ✅
logger.warning("Atenção necessária")     # Amarelo com ⚠️
logger.error("Erro encontrado")          # Vermelho com ❌
logger.debug("Debug detalhado")          # Apenas em DEBUG_MODE=true
```

**Configurações Personalizadas:**

```python
# Em assets/logging/__init__.py
setup_logging(
    debug_mode=True,        # Logs detalhados
    log_file="custom.log",  # Arquivo personalizado
    use_colors=True,        # Cores no console
    use_emojis=True        # Emojis nos logs
)
```

### 🌍 Adicionando Traduções

**Arquivo JSON (`assets/translations/pt_BR.json`):**

```json
{
  "commands": {
    "meucomando": {
      "name": "meucomando",
      "description": "Descrição em português"
    }
  },
  "messages": {
    "success": "Sucesso!",
    "error": "Erro!"
  }
}
```

**No Código:**

```python
from discord.app_commands import locale_str as _T

# Para comandos
@app_commands.command(description=_T("commands.meucomando.description"))

# Para mensagens
await interaction.response.send_message(_T("messages.success"))
```

### ⚡ Performance e Otimização

**Melhores Práticas:**

- Use `@app_commands.guild_only()` para comandos específicos de servidor
- Implemente timeouts em Views: `super().__init__(timeout=300)`
- Utilize `ephemeral=True` para respostas temporárias
- Cache dados quando possível para reduzir API calls

**Monitoramento:**

```python
# Status do bot em tempo real
logger.info(f"Latência: {bot.latency*1000:.2f}ms")
logger.info(f"Servidores: {len(bot.guilds)}")
logger.info(f"Usuários: {len(bot.users)}")
```

## 🚨 Troubleshooting

### ❌ Problemas Comuns

**1. Token Inválido:**

```bash
❌ [ERROR] 401 Unauthorized
```

**Solução:** Verifique se o TOKEN no `.env` está correto e o bot está ativo no Discord Developer Portal.

**2. Comandos não Sincronizam:**

```bash
⚠️ [WARNING] Command sync failed
```

**Solução:** Execute `/sync` no Discord ou use `python main.py --sync` (se implementado).

**3. Logs sem Cor:**

```bash
# Terminal não suporta ANSI
```

**Solução:** Configure `CONSOLE_COLORS=false` no `.env` ou use terminal compatível.

**4. Imports não Encontrados:**

```bash
❌ [ERROR] ModuleNotFoundError: No module named 'discord'
```

**Solução:** Ative o ambiente virtual e reinstale dependências:

```bash
source venv/bin/activate
pip install -r requirements.txt
```

### 🔍 Debug Mode

**Ativação:**

```env
# No arquivo .env
DEBUG_MODE=true
LOG_LEVEL=DEBUG
```

**Saída Detalhada:**

```bash
🔧 [DEBUG] Loading component: commands.embed
🔧 [DEBUG] Registering command group: embed
🔧 [DEBUG] Translation loaded: pt_BR
✅ [INFO] Component loaded successfully
```

### 📊 Logs e Monitoramento

**Estrutura dos Logs:**

```
📁 logs/
├── bot.log              # Log principal (sem cores)
├── errors.log           # Apenas erros
└── debug.log            # Debug detalhado (se ativo)
```

**Análise de Performance:**

```bash
# Comandos úteis
tail -f bot.log                    # Acompanhar logs em tempo real
grep "ERROR" bot.log              # Filtrar apenas erros
grep "🚀" bot.log | tail -10      # Últimas inicializações
```

## 🤝 Contribuição

### 📝 Guidelines

1. **Fork** o repositório
2. Crie uma **branch** para sua feature: `git checkout -b feature/nova-funcionalidade`
3. **Commit** suas mudanças: `git commit -m "feat: adiciona nova funcionalidade"`
4. **Push** para a branch: `git push origin feature/nova-funcionalidade`
5. Abra um **Pull Request**

### 🎯 Padrões de Código

- Use **type hints** sempre que possível
- Documente funções complexas com **docstrings**
- Mantenha **compatibilidade** com Python 3.8+
- Siga as convenções do **discord.py 2.5+**
- Use o sistema de **logging colorido** para debug

### ✅ Checklist de PR

- [ ] Código testado em ambiente local
- [ ] Logs apropriados adicionados
- [ ] Documentação atualizada (se necessário)
- [ ] Traduções incluídas (pt_BR e en_US)
- [ ] Sem quebras de compatibilidade
- [ ] Performance otimizada

## 📄 Licença

Este projeto está sob a licença [MIT](LICENSE). Veja o arquivo `LICENSE` para mais detalhes.

## 🔗 Links Úteis

- [Discord.py Documentação](https://discordpy.readthedocs.io/)
- [Discord Developer Portal](https://discord.com/developers/applications)
- [Python 3.8+ Downloads](https://www.python.org/downloads/)

---

<div align="center">

**Tanya Discord Bot** - Criado com ❤️ por [Kayc](https://github.com/Kaycfarias)

_Bot profissional para criação de embeds e gerenciamento de servidores Discord_

[![Discord](https://img.shields.io/badge/Discord-Bot-7289da?logo=discord&logoColor=white)](https://discord.com/developers/applications)
[![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python&logoColor=white)](https://python.org)
[![discord.py](https://img.shields.io/badge/discord.py-2.5+-00d4aa?logo=discord&logoColor=white)](https://github.com/Rapptz/discord.py)

**🔗 Links Importantes:**

- [🤖 Convite do Bot](https://discord.com/oauth2/authorize?client_id=1103371629117063278&permissions=275415166032&scope=applications.commands%20bot)
- [📚 Documentação discord.py](https://discordpy.readthedocs.io/)
- [🔧 Discord Developer Portal](https://discord.com/developers/applications)
- [🐍 Python Downloads](https://www.python.org/downloads/)
- [📖 Repositório do Projeto](https://github.com/Kaycfarias/tanyamydiscordbot)

</div>

---

<div align="center">

_⚡ "Transformando ideias em embeds incríveis desde 2023!" ⚡_

</div>
