from disnake.ext import commands  # Import commands for creating bot commands and cogs
import disnake  # Discord API library
from utils.queue_manager import get_recent_tracks, clear_played, add_to_queue  # Import functions to manage the playback queue and history
from embeds.music.playrecent_embed import (
    empty_history_embed,  # Embed to indicate that no track history exists
    success_add_recenplayed_embed  # Embed to confirm that history was re-added to the queue
)

class PlayRecent(commands.Cog):
    """
    Cog that replays the history of recently played tracks.
    
    This cog takes all the tracks from the recent history and re-adds them to the playback queue,
    preserving the chronological order (oldest first). It then clears the history and triggers playback
    if necessary.
    """
    def __init__(self, bot):
        self.bot = bot  # Store the main bot instance for later use

    @commands.command(aliases=["replayhistory"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def playrecent(self, ctx):
        """
        Command to re-add all recently played tracks to the queue.
        
        It retrieves the recent track history, and if non-empty:
          1. Reverses the order (so the oldest tracks are added first).
          2. Adds each track back into the queue.
          3. Clears the history once re-adding is complete.
          4. Sends a confirmation embed to the user.
          5. Updates the context in the Play cog and starts playback if it is not already active.
        
        Args:
            ctx: The command context from which the command is invoked.
        """
        # Retrieve the list of recently played tracks
        recent_tracks = get_recent_tracks()
        
        # If no recent tracks exist, send an embed notifying the user
        if not recent_tracks:
            return await ctx.send(embed=empty_history_embed())
        
        # Reverse the order to ensure the oldest track is added first
        for track in reversed(recent_tracks):
            add_to_queue(track)  # Add each track back into the queue
        
        clear_played()  # Clear the history after re-adding tracks to the queue
        
        # Send a confirmation embed showing that the recent tracks were added successfully
        await ctx.send(embed=success_add_recenplayed_embed(recent_tracks=recent_tracks))
        
        # Get the Play cog to update the global command context and check if playback should begin
        play_cog = self.bot.get_cog('Play')
        if play_cog:
            # Update the last valid context in the Play cog, if possible
            if hasattr(play_cog, "update_context"):
                play_cog.update_context(ctx)
            
            # If the bot's voice client is connected but not currently playing, trigger the next track
            voice_client = ctx.voice_client
            if voice_client and not voice_client.is_playing():
                await play_cog.play_next(ctx)

def setup(bot):
    """Register the PlayRecent cog with the bot."""
    bot.add_cog(PlayRecent(bot))
