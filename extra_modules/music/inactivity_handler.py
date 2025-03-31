import os  # Provides functions for interacting with the operating system (e.g., file removal)
import disnake  # Discord API wrapper for Python
import time  # Module for time-related functions, used here to track elapsed time
from disnake.ext import tasks, commands  # Extensions for creating commands and running background tasks
from embeds.music.auto_disconnect_embed import (
    paused_timeout_embed,
    inactivity_timeout_embed
)

class InactivityHandler(commands.Cog):
    """
    A Cog for managing bot inactivity in voice channels.
    
    This class periodically checks the bot's activity in voice channels and disconnects
    if it has been inactive (neither playing nor paused) for 3 minutes or paused for 5 minutes.
    """

    def __init__(self, bot, queue_manager):
        """
        Initializes the InactivityHandler.
        
        Args:
            bot: The instance of the bot.
            queue_manager: The queue manager responsible for handling the music queue.
        """
        self.bot = bot
        self.queue_manager = queue_manager
        self.first_channel = None  # Stores the channel where the bot first connected

    def start_inactivity_task(self, channel):
        """
        Starts the inactivity timer if it's not already running.
        
        Also stores the channel where the bot is connected to send disconnection messages.
        """
        if not self.inactivity_timer.is_running():
            self.inactivity_timer.start()
            self.first_channel = channel

    def cancel_inactivity_task(self):
        """
        Cancels the inactivity timer task if it is currently running.
        """
        if self.inactivity_timer.is_running():
            self.inactivity_timer.cancel()

    @tasks.loop(seconds=30)
    async def inactivity_timer(self):
        """
        A loop that runs every 30 seconds to check for inactivity or prolonged pause.
        
        The bot will disconnect from the voice channel if it has been paused for 5 minutes
        or inactive (neither playing nor paused) for 3 minutes.
        """
        for vc in self.bot.voice_clients:
            # Skip check if the bot has just connected or is currently downloading content
            if hasattr(vc, 'just_connected') and vc.just_connected:
                vc.just_connected = False
                continue

            current_time = time.time()

            if vc.is_paused():
                # If pause start time isn't recorded, record it now
                if not hasattr(vc, 'pause_start_time'):
                    vc.pause_start_time = current_time
                else:
                    # Disconnect if paused for 5 minutes (300 seconds) or more
                    if current_time - vc.pause_start_time >= 300:
                        if self.first_channel:
                            await self.first_channel.send(embed=paused_timeout_embed())
                            self.first_channel = None
                        await self.cleanup_voice_resources(vc)
                        continue
            else:
                # If not paused, remove the pause start time marker if it exists
                if hasattr(vc, 'pause_start_time'):
                    del vc.pause_start_time

            if not vc.is_playing() and not vc.is_paused():
                # Record inactivity start time if not already set
                if not hasattr(vc, 'inactivity_start_time'):
                    vc.inactivity_start_time = current_time
                else:
                    # Disconnect if inactive for 3 minutes (180 seconds) or more
                    if current_time - vc.inactivity_start_time >= 180:
                        if self.first_channel:
                            await self.first_channel.send(embed=inactivity_timeout_embed())
                            self.first_channel = None
                        await self.cleanup_voice_resources(vc)
                        continue
            else:
                # Remove inactivity marker if the bot is playing or paused
                if hasattr(vc, 'inactivity_start_time'):
                    del vc.inactivity_start_time

    async def cleanup_voice_resources(self, vc):
        """
        Cleans up resources and disconnects the bot from the voice channel.
        
        Args:
            vc: The voice client instance to disconnect.
        """
        if vc is None:
            return

        # Stop any ongoing audio playback
        vc.stop()
        if vc.source:
            try:
                # Call source cleanup if available to free internal buffers/resources
                if hasattr(vc.source, "cleanup"):
                    vc.source.cleanup()
                # Remove any downloaded file associated with the source
                if hasattr(vc.source, "filename") and vc.source.filename:
                    os.remove(vc.source.filename)
            except Exception as e:
                print(f"Error during cleanup: {e}")

        # Clear the music queue and played tracks from the queue manager
        self.queue_manager.music_queue.clear()
        self.queue_manager.clear_played()
        # Force disconnect from the voice channel
        await vc.disconnect(force=True)

    @inactivity_timer.before_loop
    async def before_inactivity(self):
        """
        Waits until the bot is ready before starting the inactivity timer loop.
        """
        await self.bot.wait_until_ready()

def setup(bot):
    """
    Sets up the InactivityHandler cog.
    
    Args:
        bot: The instance of the bot.
    """
    from utils import queue_manager
    bot.add_cog(InactivityHandler(bot, queue_manager))
