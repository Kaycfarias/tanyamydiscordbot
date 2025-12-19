import os

import discord
from discord.ext import commands


class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx):
        #fmt_priv = await self.bot.tree.sync(guild=discord.Object(id=1100204172667781120))
        fmt = await self.bot.tree.sync()
        await ctx.send(f"Sincronizados {len(fmt)} comandos")

    @commands.command()
    @commands.is_owner()
    async def reload(self, ctx):
        cog_s = []
        cog_f = []
        components_dir = "./components"
        
        for category in os.listdir(components_dir):
            category_path = os.path.join(components_dir, category)
            if not os.path.isdir(category_path) or category.startswith("_"):
                continue
            
            for f in os.listdir(category_path):
                if f.endswith(".py") and not f.startswith("_"):
                    extension_name = f"components.{category}.{f[:-3]}"
                    try:
                        await self.bot.reload_extension(extension_name)
                        print(f"Recarregado: {extension_name}")
                        cog_s.append(f[:-3])
                    except Exception as e:
                        print(f"Falha ao recarregar: {extension_name} - {e}")
                        cog_f.append(f[:-3])
        
        await ctx.send(f"**recarregado com sucesso:** {cog_s}\n**falha ao recarregar:** {cog_f}")


async def setup(bot: commands.Bot):
    await bot.add_cog(Sync(bot))
