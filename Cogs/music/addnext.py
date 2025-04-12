import os  # Provides functions for interacting with the operating system
import disnake  # Discord API wrapper for Python
import yt_dlp as youtube_dl  # YouTube downloader library (yt-dlp fork)
import asyncio  # Enables asynchronous programming
from dotenv import load_dotenv  # Loads environment variables from a .env file
from disnake.ext import commands  # Framework for creating Discord bot commands
from utils.queue_manager import add_to_queue, get_next  # Functions to manage the music queue
from spotipy import Spotify  # Spotify API client
from spotipy.oauth2 import SpotifyClientCredentials  # Handles Spotify authentication
from embeds.music.addnext_embed import (  # Import various embed functions for rich Discord messages
    bot_conflict_embed,
    search_failed_embed,
    spotify_error_embed,
    track_added_embed,
    conversion_embed,
    processing_error_embed,
    bot_not_connected_embed,
    wrong_channel_embed,
    playlist_warning_embed,
    user_not_connected_embed,
    search_embed,
    playlist_spotify_warning_embed
)

# Load environment variables from the .env file
load_dotenv()

# Retrieve secure configuration values from environment variables
spotify_client_id = os.getenv('SPOTIFY_CLIENT_ID')
spotify_client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')

# Set up the Spotify client with proper credentials
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=spotify_client_id,
    client_secret=spotify_client_secret
))

# Configuration options for yt-dlp to extract the best available audio
ytdl_format_options = {
    'format': 'bestaudio/best',  # Download best quality audio
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',  # Template for output filename
    'restrictfilenames': True,  # Restrict filenames to ASCII characters
    'noplaylist': True,  # Always avoid downloading playlists
    'nocheckcertificate': True,  # Do not check SSL certificates
    'ignoreerrors': False,  # Stop processing if an error occurs
    'logtostderr': False,  # Do not log messages to stderr
    'quiet': True,  # Run in quiet mode (suppress output)
    'no_warnings': True,  # Suppress warnings
    'default_search': 'auto',  # Automatically detect search queries
    'source_address': '0.0.0.0',  # Bind to this IP address when making network requests
    'force-ipv4': True,  # Force IPv4 usage
    'cookiefile': 'cookies.txt'  # Path to a cookie file if needed
}

# Options for ffmpeg when processing audio streams
ffmpeg_options = {
    'options': '-vn -loglevel warning'  # Disable video, show warnings only
}

# Initialize the yt-dlp downloader with the defined options
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class EnhancedYTDLSource(disnake.PCMVolumeTransformer):
    """Audio source with extended metadata support"""

    def __init__(self, source, *, data, original_url=None):
        # Initialize parent PCMVolumeTransformer with the audio source
        super().__init__(source)
        self.data = data  # Raw data dictionary from yt-dlp
        self.title = data.get('title')  # Track title
        # Use the provided original URL or fallback to the extracted URL
        self.url = original_url or data.get('url') # Direct audio stream URL
        self.original_url = original_url or self.url  # Original source URL
        self.duration = data.get('duration')  # Track duration in seconds
        self.thumbnail = data.get('thumbnail')  # URL to the track thumbnail

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=True):
        """
        Asynchronously creates an EnhancedYTDLSource from a given URL.

        Args:
            url (str): The URL to extract information from.
            loop (asyncio.AbstractEventLoop, optional): The event loop to use.
            stream (bool, optional): Whether to stream the audio (True) or download it.

        Returns:
            tuple: A tuple containing the audio source and a metadata dictionary.
        """
        # Use the provided event loop or get the current one
        loop = loop or asyncio.get_event_loop()
        # Run the yt-dlp extraction in an executor to avoid blocking the event loop
        raw_data = await loop.run_in_executor(
            None, lambda: ytdl.extract_info(url, download=not stream)
        )

        is_playlist = False
        if 'entries' in raw_data:
            # Check if the source is a real YouTube playlist
            is_playlist = raw_data.get('extractor', '').lower() == 'youtube:playlist'
            data = raw_data['entries'][0]  # Use the first entry of the playlist
        else:
            data = raw_data  # Use the raw data directly if it's a single video

        # Create an instance of EnhancedYTDLSource using FFmpegPCMAudio
        return cls(
            disnake.FFmpegPCMAudio(data['url'], **ffmpeg_options),
            data=data,
            original_url=url
        ), {
            'title': data.get('title'),
            'duration': cls.format_duration(data.get('duration')),
            'thumbnail': data.get('thumbnail'),
            'url': url,
            'is_playlist': is_playlist  # Indicates if the source was part of a playlist
        }

    @staticmethod
    def format_duration(seconds):
        """
        Format a duration given in seconds into a MM:SS string.

        Args:
            seconds (int): Duration in seconds.

        Returns:
            str: Formatted duration as "minutes:seconds".
        """
        if not seconds:
            return "N/A"
        minutes, seconds = divmod(seconds, 60)
        return f"{int(minutes)}:{int(seconds):02d}"


class AddNext(commands.Cog):
    """Advanced queue management system for prioritized music addition"""

    def __init__(self, bot):
        self.bot = bot  # Reference to the bot instance

    async def check_bot_presence(self, ctx):
        """
        Check if there are other bots (besides the current one) in the user's voice channel.

        Args:
            ctx: The command context.

        Returns:
            bool: False if another bot is present; True otherwise.
        """
        # Ensure the user is connected to a voice channel
        if ctx.author.voice and ctx.author.voice.channel:
            channel = ctx.author.voice.channel
            # Check if any other bot (excluding the current bot) is in the channel
            if any(member.bot and member != self.bot.user for member in channel.members):
                await ctx.send(embed=bot_conflict_embed())
                return False
        return True

    @commands.command(aliases=['addnext', 'insert', 'add_next'])\\\\\\
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def priority_queue(self, ctx, *, query):
        """
        Command to add a song with priority to the queue.

        Args:
            ctx: The command context.
            query (str): The search query or URL for the track.
        """
        try:
            # 1. Check if the user is connected to a voice channel
            if not ctx.author.voice or not ctx.author.voice.channel:
                await ctx.send(embed=user_not_connected_embed())
                return

            # 2. Check if the bot is connected to a voice channel
            if not ctx.voice_client:
                await ctx.send(embed=bot_not_connected_embed())
                return

            # 3. Ensure the user and bot are in the same voice channel
            if ctx.voice_client.channel.id != ctx.author.voice.channel.id:
                await ctx.send(embed=wrong_channel_embed())
                return

            # 4. Check for conflicts with other bots in the channel
            if not await self.check_bot_presence(ctx):
                return

            # Intelligent source routing based on the query content
            if "spotify.com" in query:
                await self.process_spotify(ctx, query)
            else:
                await self.process_query(ctx, query)

        except Exception as e:
            # Send an error embed if an unexpected error occurs
            await ctx.send(embed=processing_error_embed(str(e)))

    async def process_spotify(self, ctx, url):
        """
        Process a Spotify URL, converting it into a YouTube search query.

        Args:
            ctx: The command context.
            url (str): The Spotify track URL.
        """
        try:
            # Warn the user if a Spotify playlist is provided instead of a single track
            if 'playlist' in url.lower():
                await ctx.send(embed=playlist_spotify_warning_embed())
                return

            # Extract the Spotify track ID from the URL
            track_id = url.split('/')[-1].split('?')[0]
            track = sp.track(track_id)  # Retrieve track information from Spotify
            # Create a search query combining track name and primary artist
            search_query = f"{track['name']} {track['artists'][0]['name']}"

            # Inform the user about the conversion from Spotify to YouTube search
            await ctx.send(embed=conversion_embed("Spotify", f"{track['name']} - {track['artists'][0]['name']}"))
            # Process the resulting query as a normal YouTube search
            await self.process_query(ctx, search_query, platform="spotify")

        except Exception as e:
            # Send a Spotify error embed if something goes wrong
            await ctx.send(embed=spotify_error_embed(e))

    async def process_query(self, ctx, query, platform="youtube"):
        """
        Process a search query or URL, fetch track information, and add it to the queue.

        Args:
            ctx: The command context.
            query (str): The search query or URL.
            platform (str): The source platform ("youtube" by default, "spotify" if converted).
        """
        try:
            # If the query is not a valid URL, send a search embed indicating a search is being performed
            if not query.startswith(('http://', 'https://')):
                await ctx.send(embed=search_embed(query))

            # Search YouTube for a matching URL
            youtube_url = await self.search_youtube(query)
            if not youtube_url:
                await ctx.send(embed=search_failed_embed(query))
                return

            # Retrieve the audio player and metadata using the EnhancedYTDLSource class
            player, metadata = await EnhancedYTDLSource.from_url(
                youtube_url,
                loop=self.bot.loop
            )

            # If the metadata indicates the result is a playlist, warn the user
            if metadata['is_playlist']:
                await ctx.send(embed=playlist_warning_embed())

            # Add the track to the queue with priority (next in queue)
            add_to_queue(player, next_in_queue=True)
            await self.update_context(ctx)
            # Inform the user that the track was successfully added
            await ctx.send(embed=track_added_embed(metadata))

            # Send a second warning if the track is from a playlist
            if metadata['is_playlist']:
                await ctx.send(embed=playlist_warning_embed())

        except youtube_dl.DownloadError as e:
            # Handle errors related to YouTube downloading
            error_msg = f"YouTube error: {str(e)}"
            print(error_msg)
            await ctx.send(embed=processing_error_embed(error_msg))
        except Exception as e:
            # Handle any unexpected errors
            error_msg = f"Unexpected error: {str(e)}"
            print(error_msg)
            await ctx.send(embed=processing_error_embed(error_msg))

    async def search_youtube(self, query):
        """
        Perform an optimized YouTube search.

        Args:
            query (str): The search query or URL.

        Returns:
            str or None: The URL of the first video result or None if no result is found.
        """
        try:
            # If the query is not a valid URL, prepend 'ytsearch:' to perform a YouTube search
            if not query.startswith(('http://', 'https://')):
                query = f'ytsearch:{query}'

            # Run the yt-dlp extraction in an executor to avoid blocking
            data = await self.bot.loop.run_in_executor(
                None,
                lambda: ytdl.extract_info(query, download=False)
            )

            # Process different types of results
            if 'entries' in data:
                # The result is either a search result or a playlist; take the first entry
                first_entry = data['entries'][0]
                return first_entry.get('webpage_url') if first_entry else None
            else:
                # The result is a direct video URL
                return data.get('webpage_url')

        except Exception as e:
            # Print detailed error information for debugging purposes
            print(f"Detailed search error: {str(e)}")
            return None
    
    async def update_context(self, ctx):
        """Atualiza contexto globalmente"""
        play_cog = self.bot.get_cog('Play')
        watcher_cog = self.bot.get_cog('QueueWatcher')
        
        if play_cog:
            play_cog.update_context(ctx)
        if watcher_cog:
            watcher_cog.last_ctx = ctx

# Function to set up the cog; called by the bot to add this cog
def setup(bot):
    bot.add_cog(AddNext(bot))
