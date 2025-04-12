import os  # Provides operating system-related functions such as file removal
import disnake  # Discord API wrapper for Python
from disnake.ext import commands  # Framework for creating commands and cogs
import utils.queue_manager as qm  # Module for managing the music queue
from main import inactivity_handler  # InactivityHandler class for auto-disconnect if paused or not playing music
from embeds.music.leave_embed import (
    not_connected_embed,
    forced_disconnect_embed,
    success_embed
)

class Leave(commands.Cog):
    """
    Cog responsible for handling the bot leaving a voice channel.
    
    This includes:
    - Stopping the playback and cleaning up any downloaded files.
    - Clearing the music queue.
    - Disconnecting the bot from the voice channel.
    - Cancelling any inactivity timers related to the voice connection.
    """
    
    def __init__(self, bot):
        self.bot = bot  # Main bot instance reference
        self.inactivity = inactivity_handler  # Reference to the inactivity handler for auto-disconnect support

    async def cleanup_voice_resources(self, vc):
        """
        Stops playback, cleans up downloaded files, clears the music queue, and disconnects the bot.
        
        Args:
            vc: The voice client instance representing the current voice connection.
        """
        if vc is None:
            return

        # Stop the audio playback and release audio resources.
        vc.stop()
        if vc.source:
            print('aaaaaaaaaa')
            try:
                # If the source has an associated filename, remove the downloaded file.
                if vc.source.filename.startswith('youtube') and vc.source.filename:
                    print(vc.source.filename)
                    os.remove(vc.source.filename)
            except Exception as e:
                print(f"Error while removing file: {e}")

        # Clear the music queue and any history of played tracks.
        qm.music_queue.clear()
        qm.clear_played()

        # Disconnect the bot from the voice channel, forcing disconnection.
        await vc.disconnect(force=True)

    @commands.command(aliases=['disconnect', 'stop', 'dc'])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def leave(self, ctx):
        """
        Command to disconnect the bot from the voice channel, stop streaming,
        clear the queue, and remove any downloaded files.
        
        Args:
            ctx: The command context.
        """
        vc = ctx.voice_client  # Get the current voice client for this context
        if vc is None:
            await ctx.send(embed=not_connected_embed())
        else:
            await self.cleanup_voice_resources(vc)
            # Cancel the inactivity timer since the bot is leaving.
            self.inactivity.cancel_inactivity_task()
            await ctx.send(embed=success_embed())

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """
        Listener for voice state updates.
        
        If the bot is unexpectedly disconnected from a voice channel (e.g., via Discord's UI),
        perform cleanup of the queue and audio files.
        
        Args:
            member: The member whose voice state was updated.
            before: The previous voice state.
            after: The new voice state.
        """
        # Check if the updated member is the bot itself.
        if member.id == self.bot.user.id:
            # If the bot was connected and is now disconnected.
            if before.channel is not None and after.channel is None:
                await self.cleanup_voice_resources(before.channel.guild.voice_client)
                # Cancel the inactivity timer because the bot is no longer connected.
                self.inactivity.cancel_inactivity_task()

def setup(bot):
    """
    Registers the Leave cog with the bot.
    
    Args:
        bot: The main bot instance.
    """
    bot.add_cog(Leave(bot))
