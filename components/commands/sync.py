import os

import discord
from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        fmt_priv = await self.bot.tree.sync(guild=discord.Object(id=1100204172667781120))
        fmt = await self.bot.tree.sync()
        await ctx.send(f"Sincronizados {len(fmt_priv)} comandos privados e {len(fmt)} globais")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        cog_s = []
        cog_f = []
        for f in os.listdir("./cogs"):
            if f.endswith(".py"):
                try:
                    await self.bot.reload_extension("cogs." + f[:-3])
                    print(f"Recarregado: {f}")
                    cog_s.append(f)
                except Exception:
                    print(f"Falha ao recarregar: {f}")
                    cog_f.append(f)
        await ctx.send(f"**recarregado com sucesso:** {cog_s}\n**falha ao recarregar:** {cog_f}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Sync(bot))
