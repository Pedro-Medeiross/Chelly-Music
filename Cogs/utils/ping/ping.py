import typing
import disnake
import asyncio
import main
from disnake.ext import commands

class Ping(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def ping(self, ctx):
        """Return bot latency"""
        await ctx.message.delete()
        
        r = await ctx.send("A Faith está executando o comando")
        
        await r.edit(f"O ping é {main.client.latency * 1000:.2f}ms")
        await asyncio.sleep(7)
        await r.delete()
        
        
def setup(client):
    client.add_cog(Ping(client))