# Tanya Discord Bot - Copilot Instructions

## Project Overview

Tanya is a Discord bot written in Python using discord.py, focused on advanced embed creation and management. The bot features a modular cog-based architecture with Portuguese localization and complex UI components.

## Architecture & Key Components

### Bot Structure

- **Entry Point**: `main.py` - Uses `MyBot` class extending `commands.Bot` with prefix `">>"` and comprehensive intents
- **Environment**: `.env` file contains `TOKEN` and `CHATGPT_KEY` (loaded via `python-dotenv`)
- **Module System**: Components are auto-loaded from `components/` directory via `assets/cogsloader.py`

### Component Organization

```
components/
├── commands/     # Slash commands and command groups
├── events/       # Discord event handlers
embedcreator/     # Advanced embed creation system
├── components/   # UI components (buttons, dropdowns, modals)
└── defaultview.py # Main embed creator interface
```

### Translation System

- Uses `discord.app_commands.Translator` in `assets/translator.py`
- Import with: `from discord.app_commands import locale_str as _T`
- Wrap translatable strings: `_T("text")` for Portuguese/English support

## Development Patterns

### Command Structure

- Commands use `commands.GroupCog` for organization (see `embed.py`)
- Permission checking: `@commands.bot_has_permissions(send_messages=True)`
- Guild-only commands: `@app_commands.guild_only()`
- Permission validation: `if interaction.user.guild_permissions.manage_guild:`

### Cog Loading Pattern

```python
# In command files
async def setup(bot: commands.Bot):
    await bot.add_cog(YourCog(bot))
```

### UI Component Architecture

- **Views**: Inherit from `discord.ui.View` with `timeout=None` for persistent components
- **Modals**: Used for text input (title, description, etc.)
- **Cascading Views**: Components pass `(embeds, bot, defaultView)` to maintain state
- **Dynamic Updates**: Use `interaction.response.edit_message()` to update interfaces

### Embed Creator System

- Main interface: `embedcreator/defaultview.py` with add/finalize buttons
- Component hierarchy: `buttonview.py` → specialized components (color, field, etc.)
- State management: Embeds list passed through all views
- Limit: Maximum 10 embeds per creation session

### Error Handling

- Use emoji indicators: `<:error:1116338705955823626> | Error message`
- Ephemeral responses for errors: `ephemeral=True, delete_after=30`
- Try-catch for message parsing (URLs, IDs)

## Development Workflow

### Running the Bot

```bash
python main.py  # Starts bot with auto-loading components
```

### Adding New Commands

1. Create `.py` file in `components/commands/`
2. Use `commands.GroupCog` pattern
3. Add `async def setup(bot)` function
4. Bot auto-loads on restart

### UI Development

- Place UI components in `embedcreator/components/`
- Follow the pattern: View → Buttons/Dropdowns → Modals for complex interactions
- Always pass `(embeds, bot, defaultView)` for state continuity

## Key Dependencies

- `discord.py`: Main Discord API wrapper
- `python-dotenv`: Environment variable management
- `validators`: URL/input validation

## Important Notes

- Code is primarily in Portuguese with English Discord integration
- Custom emojis used throughout (stored as Discord IDs)
- Bot requires `manage_guild` permission for embed creation
- All UI interactions use ephemeral responses for privacy
- **Use only Python for code** - This is a Python-only project using discord.py
