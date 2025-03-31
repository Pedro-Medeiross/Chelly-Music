# Import required modules
import asyncio  # Asynchronous I/O operations
import main  # Main bot module (contains client instance)
from disnake.ext import commands  # Bot command framework

class Ping(commands.Cog):
    """Discord cog handling ping/pong functionality and latency checks.
    
    Features:
    - Rate limiting to prevent command spam
    - Automatic message cleanup
    - Network latency measurement
    """
    
    def __init__(self, client):
        """Initialize cog with bot reference."""
        self.client = client  # Reference to main bot instance

    @commands.cooldown(1, 3, commands.BucketType.user)  # 3-second cooldown per user
    @commands.command(pass_context=True)  # Legacy context passing (auto-enabled in newer versions)
    async def ping(self, ctx):
        """Display bot's network latency (WebSocket heartbeat).
        
        Workflow:
        1. Delete command message (cleanup)
        2. Send temporary response
        3. Calculate and display latency
        """
        
        # Cleanup original command message
        await ctx.message.delete()  # Privacy/cleanup measure
        
        # Initial response - shows command acknowledgement
        response = await ctx.send("O Chelly Bot está executando o comando")
        
        # Edit message with calculated latency (converted to milliseconds)
        # client.latency is measured in seconds
        await response.edit(
            content=f"The ping is {main.client.latency * 1000:.2f}ms"
        )

def setup(client):
    """Standard cog setup function required by disnake."""
    client.add_cog(Ping(client))  # Register cog with bot