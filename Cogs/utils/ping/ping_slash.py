import asyncio
import main
from disnake.ext import commands

class PingSlash(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.slash_command(description="Bane um usuário ou membro do servidor.")
    async def ping(self, inter):
        """Return bot latency"""

        await inter.response.defer()

        r = await inter.edit_original_response(f"O ping é {main.client.latency * 1000:.2f}ms")
        await asyncio.sleep(7)
        await r.delete
        
def setup(client):
    client.add_cog(PingSlash(client))