# 🤖 Tanya - Bot Discord

Um bot Discord moderno focado em criação avançada de embeds, desenvolvido em Python com discord.py.

## ✨ Características

- **Sistema de Embeds Avançado**: Criação interativa de embeds com interface visual completa
- **Arquitetura Modular**: Sistema de cogs com carregamento automático de componentes
- **Interface Intuitiva**: Views, botões, dropdowns e modais para interação fluida
- **Suporte a Webhooks**: Envio de embeds através de webhooks personalizados
- **Localização**: Suporte para Português Brasileiro e Inglês
- **Comandos Slash**: Integração completa com comandos de barra do Discord

## 🚀 Instalação

### Pré-requisitos

- Python 3.8+
- Conta de desenvolvedor Discord
- Token do bot Discord

### Configuração

1. **Clone o repositório:**

```bash
git clone https://github.com/Kaycfarias/tanyamydiscordbot
cd tanyamydiscordbot
```

2. **Instale as dependências:**

```bash
pip install -r requirements.txt
```

ou usando ambiente virtual (recomendado):

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

3. **Configure as variáveis de ambiente:**
   Crie um arquivo `.env` na raiz do projeto:

```env
TOKEN=seu_token_do_bot_aqui
CHATGPT_KEY=sua_chave_gpt_aqui
```

4. **Execute o bot:**

```bash
python main.py
```

## 🏗️ Arquitetura

```
📁 components/
├── 📁 commands/     # Comandos slash organizados por categoria
├── 📁 events/       # Event listeners (on_ready, etc.)
📁 embedcreator/     # Sistema de criação de embeds
├── 📁 components/   # Componentes UI (botões, dropdowns, modais)
├── 📁 modals/       # Formulários de entrada
└── defaultview.py   # Interface principal
📁 assets/
├── cogsloader.py    # Carregamento automático de módulos
└── translator.py    # Sistema de tradução
```

## 🎯 Funcionalidades Principais

### Sistema de Embeds

- Criação visual de até 10 embeds por sessão
- Editor de campos, cores, imagens e rodapés
- Preview em tempo real
- Cópia de embeds existentes via URL
- Envio direto para canais ou via webhook

### Comandos Disponíveis

- `/embed create advanced` - Abre o criador avançado de embeds
- `/ajuda` - Lista de comandos e documentação
- `/info servidor` - Informações detalhadas do servidor
- Comandos de utilidade e gerenciamento

## 🛠️ Desenvolvimento

### Adicionando Novos Comandos

1. Crie um arquivo `.py` em `components/commands/`
2. Use o padrão `commands.GroupCog`
3. Adicione a função `async def setup(bot)`
4. O bot carregará automaticamente no reinício

### Padrão de Views

```python
class MinhaView(discord.ui.View):
    def __init__(self, embeds, bot, defaultView):
        self.embeds = embeds
        self.bot = bot
        self.defaultView = defaultView
        super().__init__(timeout=None)
```

### Sistema de Tradução

```python
from discord.app_commands import locale_str as _T

@app_commands.command(description=_T("Descrição do comando"))
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'feat: adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 👨‍💻 Autor

**Kaycfarias**

- GitHub: [@Kaycfarias](https://github.com/Kaycfarias)

## 🔗 Links

- [Convite do Bot](https://discord.com/oauth2/authorize?client_id=1103371629117063278&permissions=275415166032&scope=applications.commands%20bot)
- [Documentação Discord.py](https://discordpy.readthedocs.io/)

---

> **Nota:** O bot pode estar offline por questões de hospedagem. O código permanece ativamente mantido para desenvolvimento e contribuições.
