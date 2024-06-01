import discord
from discord.ext import commands, tasks


class event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(
            f"└─» Cliente/\n    │ » Entramos como: {self.bot.user.name} - {self.bot.user.id}\n    │ » Versão: {discord.__version__}\n    └─» Online em {len(self.bot.guilds)} servidores"
        )
        self.my_task.start()

    @tasks.loop(hours=1, reconnect=True)
    async def my_task(self):
        membro = 0
        for guild in self.bot.guilds:
            membro += guild.member_count
        activity = discord.Activity(
            type=discord.ActivityType.playing,
            name=f"/ajuda | prefixo: '{self.bot.command_prefix}'",
        )
        await self.bot.change_presence(activity=activity)


async def setup(bot: commands.Bot):
    await bot.add_cog(event(bot))
