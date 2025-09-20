import discord
from discord.ext import commands, tasks


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        # Contagem de membros
        total_members = sum(guild.member_count for guild in self.bot.guilds)
        
        print(f"\n🤖 Bot conectado com sucesso!")
        print(f"   ├── 👤 Nome: {self.bot.user.name}")
        print(f"   ├── 🆔 ID: {self.bot.user.id}")
        print(f"   ├── 📋 Versão Discord.py: {discord.__version__}")
        print(f"   ├── 🌐 Servidores: {len(self.bot.guilds)}")
        print(f"   └── 👥 Membros totais: {total_members:,}")
        
        self.my_task.start()

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
    await bot.add_cog(event(bot))
