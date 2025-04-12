import os  # Provides functions for interacting with the operating system (e.g., file management)
import disnake  # Discord API wrapper for Python, used for creating and managing bot interactions
import time  # Provides time-related functions (e.g., to measure elapsed time)
import subprocess  # Allows running external commands (used here to run ffprobe)
import json  # Used to parse JSON data returned by external commands
from disnake.ext import commands  # Framework for creating Discord bot commands and cogs
from utils.queue_manager import get_current_track  # Function to retrieve the current track (if needed)
from embeds.music.currentplaying_embed import (
    success_playing_now_embed,  # Embed for displaying the currently playing track successfully
    no_playing_music_embed,     # Embed for when no music is currently playing
    no_data_music_embed         # Embed for when required track data is missing
)

def find_music_file():
    """
    Search the current directory for a music file that starts with "youtube" and
    has one of the specified audio file extensions (.mp3, .webm, .m4a).
    
    Returns:
        str or None: The first matching file name if found; otherwise, None.
    """
    # List all files in the project's root directory
    for file in os.listdir("."):
        # Check if the file name starts with "youtube" and ends with a valid audio extension
        if file.startswith("youtube") and file.endswith((".mp3", ".webm", ".m4a")):
            return file  # Return the first matching file found
    return None  # No matching file was found

def create_progress_bar(elapsed: float, duration: float, length: int = 25) -> str:
    """
    Create a progress bar string representing the elapsed time of the track.
    
    Args:
        elapsed (float): Elapsed time in seconds.
        duration (float): Total duration of the track in seconds.
        length (int): The total length (number of characters) of the progress bar.
    
    Returns:
        str: A formatted progress bar with the elapsed and total time.
    """
    # If duration is zero or negative, return a default bar without progress
    if duration <= 0:
        return "▬▬▬▬▬▬▬▬▬▬"
    
    # Calculate the proportion of elapsed time relative to the total duration
    progress = min(elapsed / duration, 1.0)
    # Determine how many segments of the progress bar should be filled
    filled = int(round(length * progress))
    
    # Build the progress bar using characters:
    # "▰" for filled segments and "▱" for empty segments.
    bar = [
        "▰" if i < filled else "▱" 
        for i in range(length)
    ]
    
    # Add an indicator (🔘) at the current progress position.
    # If no segments are filled, place the indicator at the start.
    bar[filled-1 if filled > 0 else 0] = "🔘"
    
    # Format the elapsed and total duration into MM:SS format
    elapsed_str = time.strftime("%M:%S", time.gmtime(elapsed))
    total_str = time.strftime("%M:%S", time.gmtime(duration))
    
    # Return the final formatted progress bar with a newline and time indicators
    return f"**{''.join(bar)}**\n`{elapsed_str} / {total_str}`"

def get_duration_ffmpeg(file_path):
    """
    Retrieve the duration of a media file using ffprobe (part of the FFmpeg suite).
    
    Args:
        file_path (str): Path to the media file.
    
    Returns:
        int: Duration of the file in seconds, or 0 if an error occurs.
    """
    try:
        # Run ffprobe with the required arguments to get JSON formatted metadata
        result = subprocess.run(
            ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # Parse the JSON output from ffprobe
        metadata = json.loads(result.stdout)
        # Extract the duration (in seconds) from the metadata
        duration = float(metadata["format"]["duration"])
        return int(duration)  # Return duration as an integer
    except Exception as e:
        # Print error message if ffprobe fails to retrieve duration
        print(f"Erro ao obter a duração: {e}")
        return 0

class CurrentPlaying(commands.Cog):
    """
    A Cog that defines the 'currentplaying' command, which displays the currently
    playing track along with a progress bar and other related information.
    """
    def __init__(self, bot):
        # Store the bot instance for later use in commands
        self.bot = bot

    @commands.command(aliases=["np", "nowplaying"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def currentplaying(self, ctx):
        """
        Command to display the currently playing track.
        
        It checks if there is a voice client connected and playing audio.
        If a track is playing, it retrieves relevant details and sends an embed
        with a progress bar and time information.
        
        Args:
            ctx: The context of the command invocation.
        """
        # Retrieve the voice client associated with the context
        voice_client = ctx.voice_client
        
        # If no voice client is connected, or if no track is playing, send an error embed
        if not voice_client or (not voice_client.is_playing() and not voice_client.is_paused()) or not voice_client.source:
            return await ctx.send(embed=no_playing_music_embed())

        # Get the current audio source from the voice client
        source = voice_client.source
        # Retrieve the track title and duration from the audio source metadata
        current_track = source.title
        duration = source.duration

        # Check if the necessary data (duration and start_time) is available
        if not duration or not hasattr(source, 'start_time'):
            return await ctx.send(embed=no_data_music_embed())
        
        # Calculate the elapsed time by subtracting the start time from the current time
        elapsed = time.time() - source.start_time
        # Format elapsed time and total duration into MM:SS strings
        elapsed_str = f"{int(elapsed // 60)}:{int(elapsed % 60):02d}"
        duration_str = f"{int(duration // 60)}:{int(duration % 60):02d}"
        
        # Calculate the current volume as a percentage (assuming volume is a float between 0 and 1)
        current_vol = voice_client.source.volume * 100
        
        # Create a visual progress bar representing the current track's progress
        progress_bar = create_progress_bar(elapsed, duration)
        
        #Check if bot is playing music or queue is paused
        is_playing = voice_client.is_playing()
        
        # Send an embed to the channel with details about the currently playing track
        await ctx.send(embed=success_playing_now_embed(
            current_track, 
            duration_str, 
            elapsed_str, 
            progress_bar,
            current_vol,
            is_playing
        ))

def setup(bot):
    """
    Function to set up the CurrentPlaying cog.
    
    This is called by the bot to add this cog to its collection of cogs.
    """
    bot.add_cog(CurrentPlaying(bot))
