import disnake  # Discord API wrapper for Python
from disnake.ext import tasks, commands  # Extensions for bot commands and background tasks
import asyncio  # For asynchronous locks and coroutine management
import logging  # For logging errors and information

logger = logging.getLogger(__name__)  # Create a logger for this module

class QueueWatcher(commands.Cog):
    """
    Cog to monitor the music queue and trigger playback when needed.

    This cog periodically checks if the bot's voice client is idle (not playing or paused)
    while there is still content in the queue. If such a condition is met, it triggers playback.
    """

    def __init__(self, bot, queue_manager):
        """
        Initializes the QueueWatcher cog.

        Args:
            bot: The instance of the bot.
            queue_manager: The manager handling the music queue.
        """
        self.bot = bot
        self.queue_manager = queue_manager
        self.lock = asyncio.Lock()  # Ensures that only one queue check runs at a time
        self._last_ctx = None  # Stored context used for playback commands
        
        # Start the queue check task immediately upon cog initialization
        self.queue_check.start()

    @property
    def last_ctx(self):
        """
        Gets the last valid command context from any relevant Cog.

        Returns:
            A valid commands.Context object if available; otherwise, returns the stored _last_ctx.
        """
        play_cog = self.bot.get_cog('Play')
        if play_cog and play_cog.last_valid_ctx:
            return play_cog.last_valid_ctx
        return self._last_ctx

    @last_ctx.setter
    def last_ctx(self, value):
        """
        Updates the last valid command context in all relevant cogs.

        Args:
            value: The new context to be stored.
        """
        play_cog = self.bot.get_cog('Play')
        if play_cog:
            play_cog.last_valid_ctx = value
        self._last_ctx = value

    @tasks.loop(seconds=30)  # Adjust this interval to 30 seconds if necessary
    async def queue_check(self):
        """
        Task loop that runs every 10 seconds to monitor the voice clients.

        It checks each voice client for conditions that require triggering playback,
        such as when the client is idle and the queue is not empty.
        """
        async with self.lock:  # Prevent concurrent executions of the queue check
            try:
                # Iterate over all voice clients connected to the bot
                for vc in self.bot.voice_clients:
                    # If conditions are met, trigger playback for that voice client
                    if self.should_trigger(vc):
                        await self.trigger_playback(vc)
            except Exception as e:
                logger.error(f"Queue check error: {str(e)}")

    def should_trigger(self, vc):
        """
        Determines whether playback should be triggered for a given voice client.

        Conditions:
            - The voice client exists.
            - It is not currently playing any audio.
            - It is not paused.
            - The music queue is not empty.

        Args:
            vc: The voice client to check.

        Returns:
            True if playback should be triggered; otherwise, False.
        """
        return (
            vc and 
            not vc.is_playing() and 
            not vc.is_paused() and 
            not self.queue_manager.is_empty()
        )

    async def trigger_playback(self, vc):
        """
        Triggers the next track playback if conditions are met.

        Retrieves the 'Play' cog and uses its play_next method with a valid context.

        Args:
            vc: The voice client for which playback should be triggered.
        """
        try:
            play_cog = self.bot.get_cog('Play')
            if play_cog and self.last_ctx:
                # Use the stored context if it is a valid commands.Context,
                # or create a new context if necessary.
                ctx = self.last_ctx if isinstance(self.last_ctx, commands.Context) else await self.create_context(vc)
                
                # Only trigger playback if the voice client is still idle
                if ctx and not ctx.voice_client.is_playing():
                    await play_cog.play_next(ctx)
        except Exception as e:
            logger.error(f"Playback trigger error: {str(e)}")

    async def create_context(self, vc):
        """
        Creates an artificial command context.

        This is useful if no valid context is stored. It attempts to locate a text channel 
        related to the voice channel or uses the guild's system channel to generate a context.
        
        Args:
            vc: The voice client for which context is needed.
        
        Returns:
            A commands.Context object if successful; otherwise, None.
        """
        try:
            guild = vc.guild
            # Try to find a text channel with the same name as the voice channel; otherwise, use the system channel
            channel = disnake.utils.get(guild.text_channels, name=vc.channel.name) or guild.system_channel
            # Send a temporary message to obtain a context from the bot
            temp_msg = await channel.send("Obtendo contexto para reprodução...")
            return await self.bot.get_context(temp_msg)
        except Exception as e:
            logger.warning(f"Context creation failed: {str(e)}")
            return None

    @queue_check.before_loop
    async def before_check(self):
        """
        Waits until the bot is fully ready before starting the queue check loop.
        """
        await self.bot.wait_until_ready()

def setup(bot):
    """
    Registers the QueueWatcher cog with the bot.

    Args:
        bot: The instance of the bot.
    """
    from utils import queue_manager  # Import the queue manager module
    bot.add_cog(QueueWatcher(bot, queue_manager))
