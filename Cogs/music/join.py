from disnake.ext import commands  # Import the Discord command framework for creating bot commands and cogs
from main import inactivity_handler # Class of Inactive Handle support for auto disconect if paused or not playing music
from embeds.music.join_embed import (  # Import custom embed templates for various voice join responses
    already_in_channel_embed,
    busy_embed,
    connect_first_embed,
    conflict_embed,
    join_success_embed,
    connection_failed_embed
)

class Join(commands.Cog):
    """
    Cog for managing voice channel connections with conflict prevention and rich embed responses.

    Features:
    - Detects conflicting music bots in the same voice channel.
    - Validates that the user is connected to a voice channel.
    - Provides user-friendly responses using custom embed messages.
    - Handles errors during connection attempts.
    """
    
    def __init__(self, bot):
        self.bot = bot  # Store the main bot instance for later use
        self.inactivity = inactivity_handler

    async def check_bot_conflict(self, ctx) -> bool:
        """
        Check for competing music bots in the user's voice channel.

        Args:
            ctx: The command context containing the author and their voice state.

        Returns:
            bool: True if no conflicting bot is found, False otherwise.
        """
        # Get the voice channel that the command author is connected to
        channel = ctx.author.voice.channel
        
        # Efficiently check if any other bot (with a specific naming convention) is in the channel.
        # This ignores the current bot and looks for bots whose name includes "Chelly Music".
        has_conflict = any(
            member.bot and member.id != self.bot.user.id  # Ignore the current bot itself
            and "Chelly Music" in member.name  # Check for the specific bot naming pattern
            for member in channel.members
        )
        
        # Return True if there is no conflict, False if a conflicting bot is detected.
        return not has_conflict

    @commands.command(aliases=['j'])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def join(self, ctx):
        """
        Command to have the bot join the user's voice channel with detailed feedback.

        Workflow:
        1. Check if the bot is already connected to any voice channel.
        2. Validate that the user is connected to a voice channel.
        3. Verify there are no conflicting bots in the user's channel.
        4. Attempt to connect to the voice channel, handling errors if they occur.

        Args:
            ctx: The command context.
        """
        
        # Step 1: Check if the bot is already connected to a voice channel.
        if ctx.voice_client:
            # If the bot is in the same channel as the user, send an "already in channel" embed;
            # otherwise, send a "busy" embed indicating the bot is connected elsewhere.
            embed = (already_in_channel_embed() 
                     if ctx.voice_client.channel == ctx.author.voice.channel 
                     else busy_embed())
            await ctx.send(embed=embed)
            return

        # Step 2: Validate that the user is connected to a voice channel.
        if not ctx.author.voice:
            # If the user is not in any voice channel, prompt them to connect first.
            await ctx.send(embed=connect_first_embed())
            return

        # Step 3: Check for conflicting music bots in the user's voice channel.
        if not await self.check_bot_conflict(ctx):
            # If a conflict is detected, notify the user using a conflict embed.
            await ctx.send(embed=conflict_embed())
            return

        # Step 4: Attempt to connect the bot to the user's voice channel.
        try:
            # Retrieve the voice channel the user is in.
            channel = ctx.author.voice.channel
            # Connect the bot to the voice channel.
            await channel.connect()
            vc = ctx.voice_client
            vc.just_connected = True
            # Start/Restar the timer on new music play
            self.inactivity.start_inactivity_task(channel=ctx.channel)
            # Notify the user of a successful connection using a success embed.
            await ctx.send(embed=join_success_embed(channel))
            
        except Exception as e:
            # If an error occurs (such as permission issues or timeouts), send an error embed.
            await ctx.send(embed=connection_failed_embed(e))

def setup(bot):
    """
    Register the Join cog with the bot.

    Args:
        bot: The main bot instance.
    """
    # Add the Join cog to the bot's collection of cogs, making its commands available.
    bot.add_cog(Join(bot))
