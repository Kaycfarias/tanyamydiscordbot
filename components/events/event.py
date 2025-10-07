import discord
from discord.ext import commands, tasks
import asyncio
from datetime import datetime, timezone

from assets.logging import get_logger


class EventHandler(commands.Cog):
    """Gerenciador de eventos principais do bot."""
    
    def __init__(self, bot):
        self.bot = bot
        self.logger = get_logger(__name__)
        self.start_time = datetime.now(timezone.utc)
        # Mensagens de status rotativas
        self._status_messages = [
            {"text": "/ajuda para comandos", "type": "listening"},
            {"text": "Criando embeds incríveis", "type": "creating"}, 
            {"text": "Moderando servidores", "type": "watching"},
            {"text": "Online 24/7", "type": "playing"},
            {"text": "Comandos de barra", "type": "listening"},
            {"text": "Embeds personalizados", "type": "creating"}
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
            
            self.logger.info("🤖 Bot conectado com sucesso!")
            self.logger.info(f"   ├── 👤 Nome: {self.bot.user.name}")
            self.logger.info(f"   ├── 🆔 ID: {self.bot.user.id}")
            self.logger.info(f"   ├── 📋 Versão Discord.py: {discord.__version__}")
            self.logger.info(f"   ├── 🌐 Servidores: {len(self.bot.guilds)}")
            self.logger.info(f"   ├── 👥 Membros totais: {total_members:,}")
            self.logger.info(f"   ├── 📺 Canais totais: {total_channels:,}")
            self.logger.info(f"   └── ⏰ Tempo de inicialização: {uptime.total_seconds():.2f}s")
            
            # Log estruturado adicional
            self.logger.debug("Estatísticas detalhadas do bot", extra={
                "guilds": len(self.bot.guilds),
                "members": total_members,
                "channels": total_channels,
                "startup_time": uptime.total_seconds()
            })
            
            # Definir status inicial
            await self._set_initial_status()
            
            # Iniciar tasks
            if not self.status_updater.is_running():
                self.status_updater.start()
            
            # Sincronizar comandos de aplicação (opcional)
            try:
                synced = await self.bot.tree.sync()
                self.logger.info(f"Sincronizados {len(synced)} comandos de aplicação")
            except Exception as e:
                self.logger.warning(f"Falha ao sincronizar comandos: {e}")

    @tasks.loop(minutes=15, reconnect=True)
    async def status_updater(self):
        """Atualiza o status do bot periodicamente."""
        try:
            total_members = sum(guild.member_count for guild in self.bot.guilds if guild.member_count)
            
            # Pegar mensagem atual
            current_status = self._status_messages[self._current_status_index]
            self._current_status_index = (self._current_status_index + 1) % len(self._status_messages)
            
            # Mapear tipos de atividade
            activity_types = {
                "playing": discord.ActivityType.playing,
                "listening": discord.ActivityType.listening,
                "watching": discord.ActivityType.watching,
                "creating": discord.ActivityType.custom
            }
            
            activity_type = activity_types.get(current_status["type"], discord.ActivityType.playing)
            
            # Adicionar informações dinâmicas para alguns tipos
            if current_status["type"] in ["watching", "playing"]:
                status_text = f"{current_status['text']} | {len(self.bot.guilds)} servidores"
            else:
                status_text = current_status["text"]
            
            # Criar e definir atividade
            activity = discord.Activity(type=activity_type, name=status_text)
            await self.bot.change_presence(
                activity=activity,
                status=discord.Status.online
            )
            
            self.logger.debug(f"🔄 Status atualizado: {status_text} ({current_status['type']})")
            
        except Exception as e:
            self.logger.error(f"❌ Erro ao atualizar status: {e}")

    @status_updater.before_loop
    async def before_status_updater(self):
        """Aguarda o bot estar pronto antes de iniciar o loop."""
        await self.bot.wait_until_ready()

    async def _set_initial_status(self):
        """Define o status inicial do bot."""
        try:
            initial_activity = discord.Activity(
                type=discord.ActivityType.playing,
                name=f"/ajuda | {len(self.bot.guilds)} servidores | Pronto!"
            )
            await self.bot.change_presence(
                activity=initial_activity,
                status=discord.Status.online
            )
            self.logger.info("✅ Status inicial definido")
        except Exception as e:
            self.logger.warning(f"⚠️ Erro ao definir status inicial: {e}")

    def cog_unload(self):
        """Cleanup quando o cog for removido."""
        if self.status_updater.is_running():
            self.status_updater.cancel()
            self.logger.info("🛑 Task de status cancelada")


async def setup(bot: commands.Bot):
    await bot.add_cog(EventHandler(bot))
