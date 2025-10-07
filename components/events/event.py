import discord
from discord.ext import commands, tasks
import logging
import asyncio
from datetime import datetime, timezone


class EventHandler(commands.Cog):
    """Gerenciador de eventos principais do bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = logging.getLogger(__name__)
        self.start_time = datetime.now(timezone.utc)
        self._status_messages = [
            "/ajuda para comandos",
            "Criando embeds incríveis",
            "Moderando servidores",
            "Online 24/7"
        ]
        self._current_status_index = 0

    @commands.Cog.listener()
    async def on_ready(self):
        """Executado quando o bot está pronto e conectado."""
        if not hasattr(self, '_ready_fired'):
            self._ready_fired = True
            
            # Estatísticas do bot
            total_members = sum(guild.member_count for guild in self.bot.guilds)
            total_channels = sum(len(guild.channels) for guild in self.bot.guilds)
            
            # Informações de sistema
            uptime = datetime.now(timezone.utc) - self.start_time
            
            print(f"\n🤖 Bot conectado com sucesso!")
            print(f"   ├── 👤 Nome: {self.bot.user.name}")
            print(f"   ├── 🆔 ID: {self.bot.user.id}")
            print(f"   ├── 📋 Versão Discord.py: {discord.__version__}")
            print(f"   ├── 🌐 Servidores: {len(self.bot.guilds)}")
            print(f"   ├── 👥 Membros totais: {total_members:,}")
            print(f"   ├── 📺 Canais totais: {total_channels:,}")
            print(f"   └── ⏰ Tempo de inicialização: {uptime.total_seconds():.2f}s")
            
            # Log estruturado
            self.logger.info("Bot conectado com sucesso", extra={
                "guilds": len(self.bot.guilds),
                "members": total_members,
                "channels": total_channels,
                "startup_time": uptime.total_seconds()
            })
            
            # Iniciar tasks
            if not self.status_updater.is_running():
                self.status_updater.start()
            
            # Sincronizar comandos de aplicação (opcional)
            try:
                synced = await self.bot.tree.sync()
                self.logger.info(f"Sincronizados {len(synced)} comandos de aplicação")
            except Exception as e:
                self.logger.warning(f"Falha ao sincronizar comandos: {e}")

    @tasks.loop(hours=1, reconnect=True)
    async def my_task(self):
        """Atualiza o status do bot a cada hora."""
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        
        # Status com informações dinâmicas
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=f"/ajuda | {len(self.bot.guilds)} servidores | {total_members:,} usuários",
        )
        await self.bot.change_presence(activity=activity)
        
        # Log opcional para debug (comentado por padrão)
        # print(f"🔄 Status atualizado: {len(self.bot.guilds)} servidores, {total_members:,} membros")


async def setup(bot: commands.Bot):
    await bot.add_cog(EventHandler(bot))
