import concurrent.futures  # For executing blocking operations using a thread pool
import os  # For file system operations
import time  # For tracking playback time
import disnake  # Discord API wrapper for Python
import yt_dlp as youtube_dlp  # Library for downloading/extracting information from YouTube (fork of yt-dlp)
import asyncio  # For asynchronous programming support
from dotenv import load_dotenv  # To load environment variables from a .env file
from disnake.ext import commands  # Command framework for creating cogs (extensions) for Discord bots
from spotipy import Spotify  # Spotify API client
from spotipy.oauth2 import SpotifyClientCredentials  # Spotify client credentials authentication
from utils.queue_manager import add_to_queue, get_next, add_to_played  # Utility functions for managing the music queue
from main import inactivity_handler  # Inactivity tracking system for automatic disconnection
from embeds.music.play_embed import (
    success_playing_now_embed,
    voice_channel_error_embed,
    already_connected_embed,
    connection_failed_embed,
    spotify_not_found_embed,
    youtube_not_found_embed,
    track_added_embed,
    download_error_embed,
    playback_error_embed,
    empty_playlist_embed,
    added_playlist_tracks_embed,
    processing_spotify_playlist,
    processing_youtube_playlist,
    same_voice_channel_error_embed
)

# Load environment variables from the .env file
load_dotenv()

start_time = time.time()  # Record the start time for tracking purposes

# ======================
# INITIAL CONFIGURATIONS
# ======================

# Define the project root by going up two directories from the current file's directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
# Construct the path to the cookies file
cookies_file = os.path.join(project_root, 'cookies.txt')
# Raise an error if the cookies file does not exist
if not os.path.isfile(cookies_file):
    raise FileNotFoundError(f'Arquivo de cookies não encontrado: {cookies_file}')

# ======================
# SPOTIFY CONFIGURATION
# ======================

# Initialize Spotify client with client credentials from environment variables
sp = Spotify(auth_manager=SpotifyClientCredentials(
    client_id=os.getenv('SPOTIFY_CLIENT_ID'),
    client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')
))

# ======================
# YT-DLP CONFIGURATION
# ======================

# Options for yt-dlp to specify format, file naming, and other preferences
ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0',  # Bind to IPv4 address
    'cookiefile': cookies_file  # Use the cookies file for authenticated requests
}

# Options for ffmpeg to ensure proper streaming and reconnection behavior
ffmpeg_options = {
    'options': '-vn -reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5'
}

# Initialize yt-dlp with the provided options
ytdl = youtube_dlp.YoutubeDL(ytdl_format_options)
# Create a thread pool executor with a maximum of 4 workers for yt-dlp tasks
yt_executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

# ======================
# AUDIO CLASS: YTDLSource
# ======================

class YTDLSource(disnake.PCMVolumeTransformer):
    """
    A class that wraps an audio source for playback in Discord.
    Extends PCMVolumeTransformer to allow volume control.
    """
    def __init__(self, source, *, data, volume=0.5, original_url=None, filename=None):
        # Initialize the parent class with the audio source and volume
        super().__init__(source, volume)
        self.data = data  # Store metadata extracted from yt-dlp
        self.title = data.get('title')  # Track title
        self.duration = data.get('duration')  # Track duration in seconds
        self.url = data.get('url')  # URL of the audio stream
        self.original_url = original_url or self.url  # Original URL provided
        self.filename = filename  # Local filename if the track was downloaded
        self.start_time = None  # Time when playback starts

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        """
        Asynchronously creates a YTDLSource instance from a URL.
        Uses a thread pool to run the blocking yt-dlp extraction.
        """
        loop = loop or asyncio.get_event_loop()
        # Run yt-dlp extraction in a separate thread
        data = await loop.run_in_executor(
            yt_executor,
            lambda: ytdl.extract_info(url, download=not stream)
        )
        # If data contains a playlist, select the first entry
        if 'entries' in data:
            data = data['entries'][0]
        # Prepare filename if not streaming
        filename = ytdl.prepare_filename(data) if not stream else None
        return cls(
            disnake.FFmpegPCMAudio(filename or data['url'], **ffmpeg_options),
            data=data,
            original_url=url,
            filename=filename
        )

# ======================
# MAIN MUSIC COG (OPTIMIZED)
# ======================

class Play(commands.Cog):
    """
    Main cog for music playback. Handles playing, queuing, and playlist processing.
    """
    def __init__(self, bot):
        self.bot = bot
        self.first_channel = None  # The first channel used for playback (for inactivity tracking)
        self.inactivity = inactivity_handler  # Handler for inactivity to auto-disconnect
        self.last_valid_ctx = None  # Last valid context used for commands
        self.play_lock = asyncio.Lock()  # Lock to avoid race conditions in playback
        self.info_cache = {}  # Cache for track metadata to reduce redundant downloads
        # Dictionary containing URLs for embed icons used in various messages
        self.embed_icons = {
            'error': 'https://i.imgur.com/7F6G3ZZ.png',
            'music': 'https://i.imgur.com/qk0hK0q.png',
            'playlist': 'https://i.imgur.com/5XyWZ3J.png'
        }

    async def ensure_no_other_bot(self, ctx):
        """
        Checks if there is another bot in the user's voice channel.
        Sends an error message if found.
        """
        if ctx.author.voice and ctx.author.voice.channel:
            for member in ctx.author.voice.channel.members:
                if member.bot and member != self.bot.user:
                    await ctx.send(embed=connection_failed_embed())
                    return False
        return True

    def update_context(self, ctx):
        """
        Updates the last valid command context.
        Also updates context for the QueueWatcher cog if it exists.
        """
        self.last_valid_ctx = ctx
        if watcher := self.bot.get_cog('QueueWatcher'):
            watcher.last_ctx = ctx

    @commands.command(aliases=['p', 'playmusic'])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def play(self, ctx, *, query: str = None):
        """
        Main command for playing music.
        If no query is provided, it checks the queue and starts playback.
        """
        self.update_context(ctx)

        # Ensure the user is connected to a voice channel
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.send(embed=voice_channel_error_embed())
        
        # Ensure the user is connected to same channel
        if ctx.author.voice.channel != ctx.guild.voice_client.channel:
            return await ctx.send(embed=same_voice_channel_error_embed())

        # If no query is provided, try to start playing the next track
        if not query:
            # Connect to the voice channel if not already connected
            if ctx.voice_client is None:
                if not await self.ensure_no_other_bot(ctx):
                    return
                await ctx.invoke(self.bot.get_command('join'))
                if ctx.voice_client is None:
                    return await ctx.send(embed=connection_failed_embed())
            
            # If nothing is playing, start the next track in the queue
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)
            return

        async with ctx.typing():
            # Connect to the voice channel if not already connected
            if ctx.voice_client is None:
                if not await self.ensure_no_other_bot(ctx):
                    return
                await ctx.invoke(self.bot.get_command('join'))
                if ctx.voice_client is None:
                    return await ctx.send(embed=connection_failed_embed())

            vc = ctx.voice_client
            vc.just_connected = True  # Flag to indicate recent connection

            try:
                # Handle different types of queries based on URL content
                if "spotify.com" in query:
                    await self.handle_spotify(ctx, query)
                elif "youtube.com/playlist" in query:
                    await self.add_youtube_playlist(ctx, query)
                else:
                    await self.handle_youtube(ctx, query)
            except Exception as e:
                # Send an error embed if any exception occurs during processing
                await ctx.send(embed=download_error_embed(str(e)))

        # If no source is set, attempt to play the next track
        if not ctx.voice_client.source:
            await self.play_next(ctx)

    async def handle_spotify(self, ctx, query):
        """
        Processes Spotify links.
        If a playlist is detected, calls the playlist handler;
        otherwise, searches for a track and processes it.
        """
        if "playlist" in query:
            await self.add_spotify_playlist(ctx, query)
        else:
            track_info = self.get_spotify_track_info(query)
            if not track_info:
                return await ctx.send(embed=spotify_not_found_embed())
            title, search_query = track_info
            youtube_url = self.get_youtube_url(search_query)
            if not youtube_url:
                return await ctx.send(embed=spotify_not_found_embed())
            await self.process_track(ctx, youtube_url, title)

    async def handle_youtube(self, ctx, query):
        """
        Processes YouTube queries.
        Determines if the query is a direct URL or search term and processes accordingly.
        """
        if "youtube.com" in query or "youtu.be" in query:
            url = query
        else:
            url = self.get_youtube_url(query)
            if not url:
                return await ctx.send(embed=youtube_not_found_embed())
        await self.process_track(ctx, url)

    async def process_track(self, ctx, url: str, title: str = None):
        """
        Processes a single track.
        Extracts track info using yt-dlp, caches it, adds the track to the queue,
        and initiates playback if nothing is playing.
        """
        try:
            # Check if the track info is already cached
            if url in self.info_cache:
                info = self.info_cache[url]
            else:
                loop = asyncio.get_event_loop()
                # Extract track information in a separate thread
                info = await loop.run_in_executor(
                    yt_executor,
                    lambda: ytdl.extract_info(url, download=False)
                )
                self.info_cache[url] = info

            # If the result is a playlist, take the first entry
            if "entries" in info:
                info = info["entries"][0]

            track_title = title or info.get('title', 'Unknown Track')
            add_to_queue({"original_url": url, "title": track_title})
            global x  # Global message variable used to update the user
            x = await ctx.send(embed=track_added_embed(track_title))
            
            # If nothing is playing, start the next track
            if not ctx.voice_client.is_playing():
                await self.play_next(ctx)

        except youtube_dlp.utils.DownloadError as e:
            await ctx.send(embed=download_error_embed(str(e)))

    async def add_spotify_playlist(self, ctx, url):
        """
        Handles adding a Spotify playlist.
        Retrieves tracks from the playlist, searches for each on YouTube, and adds them to the queue.
        """
        results = sp.playlist_tracks(url)
        total_tracks = len(results['items'])
        if total_tracks == 0:
            return await ctx.send(embed=empty_playlist_embed())

        await ctx.send(embed=processing_spotify_playlist(total_tracks=total_tracks))
        added_count = 0
        first_track = True

        for item in results['items']:
            track = item['track']
            search_query = f"{track['name']} {track['artists'][0]['name']}"
            youtube_url = self.get_youtube_url(search_query)
            if youtube_url:
                try:
                    # Play immediately if it's the first track and nothing is playing
                    if first_track and not ctx.voice_client.is_playing():
                        await self.process_track(ctx, youtube_url, track['name'])
                        first_track = False
                    else:
                        add_to_queue({"original_url": youtube_url, "title": track['name']})
                        await x.edit(embed=track_added_embed(title=track['name'], artist=track['artists'][0]['name']))
                    added_count += 1
                except:
                    pass

        await ctx.send(embed=added_playlist_tracks_embed(added_count))
    
    async def add_youtube_playlist(self, ctx, url):
        """
        Handles adding a YouTube playlist.
        Extracts playlist information and adds each track to the queue.
        """
        data = ytdl.extract_info(url, download=False)
        total_tracks = len(data['entries'])
        if total_tracks == 0:
            return await ctx.send(embed=empty_playlist_embed())

        await ctx.send(embed=processing_youtube_playlist(total_tracks=total_tracks))
        added_count = 0
        first_track = True

        for entry in data['entries']:
            youtube_url = entry['webpage_url']
            try:
                # Play immediately if it's the first track and nothing is playing
                if first_track and not ctx.voice_client.is_playing():
                    await self.process_track(ctx, youtube_url)
                    first_track = False
                else:
                    add_to_queue({"original_url": youtube_url, "title": entry['title']})
                    await x.edit(embed=track_added_embed(title=entry['title']))
                added_count += 1
            except:
                pass

        await ctx.send(embed=added_playlist_tracks_embed(added_count))

    async def play_next(self, ctx=None):
        """
        Plays the next track in the queue.
        Uses a lock to ensure that only one track is processed at a time.
        """
        async with self.play_lock:
            ctx = ctx or self.last_valid_ctx
            # If no valid context or something is already playing, do nothing
            if not ctx or ctx.voice_client.is_playing():
                return

            await asyncio.sleep(0.5)  # Small delay to ensure previous track is finished
            if ctx.voice_client.is_playing():
                return

            track_info = get_next()  # Get next track from the queue
            if not track_info:
                return

            try:
                url = track_info["original_url"]
                # Check if track info is cached; if not, extract and cache it
                if url in self.info_cache:
                    info = self.info_cache[url]
                else:
                    loop = asyncio.get_event_loop()
                    info = await loop.run_in_executor(
                        yt_executor,
                        lambda: ytdl.extract_info(url, download=False)
                    )
                    self.info_cache[url] = info

                # Create a new player source from the URL
                new_player = await YTDLSource.from_url(url, loop=self.bot.loop, stream=False)
                new_player.start_time = time.time()
                
                # Start playback and set a callback for when the track ends
                ctx.voice_client.play(
                    new_player,
                    after=lambda e: self.bot.loop.create_task(self.on_track_end(ctx, new_player))
                )
                
                duration = new_player.duration or 0
                await ctx.send(embed=success_playing_now_embed(
                    current_track=new_player.title,
                    duration_str=f"{duration//60}:{duration%60:02}",
                    playing_time="0:00",
                    current_vol=str(int(new_player.volume * 100)),
                    is_playing=True
                ))
            except Exception as e:
                # Send a playback error message and try playing the next track
                await ctx.send(embed=playback_error_embed(str(e)))
                await self.play_next(ctx)

    async def on_track_end(self, ctx, player):
        """
        Callback function when a track ends.
        Updates inactivity tracking, cleans up downloaded files, and triggers the next track.
        """
        self.inactivity.first_channel = ctx.channel  # Set the channel for inactivity monitoring
        add_to_played(player)  # Mark the track as played
        # Remove the downloaded file if it exists
        if player.filename and os.path.exists(player.filename):
            try:
                os.remove(player.filename)
            except Exception as e:
                print(f"Erro ao limpar arquivo: {str(e)}")
        await self.play_next(ctx)

    def get_spotify_track_info(self, url):
        """
        Retrieves track information from Spotify given a track URL.
        Returns the track's name and a combined search query with the artist.
        """
        try:
            track = sp.track(url)
            return track['name'], f"{track['name']} {track['artists'][0]['name']}"
        except:
            return None

    def get_youtube_url(self, query):
        """
        Searches YouTube for the given query and returns the URL of the first result.
        """
        try:
            results = ytdl.extract_info(f"ytsearch:{query}", download=False)['entries']
            return results[0]['webpage_url'] if results else None
        except:
            return None

def setup(bot):
    # Register the Play cog with the bot
    bot.add_cog(Play(bot))
