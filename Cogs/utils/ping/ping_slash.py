# Import required modules
import asyncio  # Async operation support
import main  # Main bot module containing client instance
from disnake.ext import commands  # Command framework

class PingSlash(commands.Cog):
    """Slash command cog for network latency checks and moderation utilities.
    
    Features:
    - Rate-limited slash commands
    - Deferred responses for better UX
    - WebSocket latency measurement
    """
    
    def __init__(self, client):
        """Initialize cog with bot reference."""
        self.client = client  # Reference to main bot instance

    @commands.cooldown(1, 3, commands.BucketType.user)  # 3-second cooldown per user
    @commands.slash_command(description="Bans a user or member from the server.")  # [!] WARNING: Incorrect description
    async def ping(self, inter):
        """Display bot's WebSocket latency through slash command.
        
        Workflow:
        1. Defer response to prevent interaction timeout
        2. Calculate and format latency
        3. Update interaction response
        """
        
        # Acknowledge interaction first (prevents "Interaction Failed" errors)
        await inter.response.defer()  # Gives 15 minutes to respond
        
        # Calculate latency and format response (latency is in seconds)
        latency_ms = main.client.latency * 1000  # Convert to milliseconds
        
        # Update deferred response with calculated value
        await inter.edit_original_response(
            content=f"The ping is {latency_ms:.2f}ms"
        )

def setup(client):
    """Standard cog registration hook for disnake."""
    client.add_cog(PingSlash(client))  # Add cog to bot instance