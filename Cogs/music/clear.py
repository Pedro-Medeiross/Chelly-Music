import disnake
from disnake.ext import commands
from utils.queue_manager import clear_queue, is_empty  # Utility functions to manage the music queue
from embeds.music.clear_embed import (
    queue_cleared_embed,  # Embed indicating the queue has been cleared
    queue_empty_embed     # Embed indicating the queue is already empty
)

class ClearQueue(commands.Cog):
    """A cog for clearing the music queue."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clearqueue", aliases=["cq"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def clearqueue(self, ctx):
        """
        Clears the entire music playback queue.

        If the queue is already empty, sends an embed informing that there are no songs to remove.
        """
        # Check if the queue is empty
        if is_empty():
            # Send an embed indicating the queue is empty
            return await ctx.send(embed=queue_empty_embed())

        # Clear the queue
        clear_queue()
        # Send an embed indicating the queue has been cleared
        await ctx.send(embed=queue_cleared_embed())

def setup(bot):
    """Adds the ClearQueue cog to the bot."""
    bot.add_cog(ClearQueue(bot))
