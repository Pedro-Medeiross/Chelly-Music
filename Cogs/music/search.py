import asyncio
import disnake
from disnake.ext import commands
import yt_dlp as youtube_dlp
from utils.queue_manager import add_to_queue, get_next  # Functions for managing the queue
from embeds.music.search_embeds import (
    voice_channel_error_embed,  # Embed for error when user is not in a voice channel
    youtube_not_found_embed,    # Embed for when no YouTube results are found
    track_added_embed,          # Embed for confirming a track was added
    searching_embed,            # Embed for confirming bot is searching
    search_results_embed,       # Embed for return the results
    timeout_embed,              # Embed for not selection in time
    cancel_embed,               # Embed for cancel request
    error_embed,                # Embed for errors
    success_embed               # Embed for success add
)

# yt-dlp configuration options for extracting audio from YouTube
ytdl_format_options = {
    'format': 'bestaudio/best',                # Select the best available audio quality
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',  # Template for output filename
    'restrictfilenames': True,                 # Restrict filenames to ASCII characters and avoid special characters
    'noplaylist': False,                       # Allow playlists to be processed
    'nocheckcertificate': True,                # Do not check SSL certificates
    'ignoreerrors': False,                     # Stop on errors
    'logtostderr': False,                      # Do not log messages to stderr
    'quiet': True,                             # Suppress verbose output
    'no_warnings': True,                       # Suppress warnings
    'default_search': 'auto',                  # Automatically search if the input is not a URL
    'source_address': '0.0.0.0'                  # Bind to an IPv4 address to avoid potential issues with IPv6
}
ytdl = youtube_dlp.YoutubeDL(ytdl_format_options)

class Search(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command(aliases=['find'])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
    async def search(self, ctx, *, query: str):
        """
        Search command:
        - Verifies if the user is in a voice channel.
        - Performs a search on YouTube and displays the first 3 results in an embed.
        - Adds reactions for the user to select an option or cancel.
        - Upon selection, adds the track to the queue, clears reactions, edits the embed, and if the bot is not playing, starts playback.
        """
        # Check if the user is connected to a voice channel
        if not ctx.author.voice or not ctx.author.voice.channel:
            return await ctx.send(embed=voice_channel_error_embed())

        # Send an embed message to indicate that the search is in progress
        msg = await ctx.send(embed=searching_embed())

        # Perform the search using "ytsearch3:" to obtain 3 results from YouTube
        try:
            data = ytdl.extract_info(f"ytsearch3:{query}", download=False)
            results = data.get("entries", [])
            if not results:
                return await msg.edit(embed=youtube_not_found_embed())
        except Exception as e:
            await msg.edit(content="Error occurred while searching on YouTube.")
            print(f"Error during search: {e}")
            return

        # Build the embed message with the 3 search results
        await msg.edit(embed=search_results_embed(results))

        # Add reaction emojis for user selection
        reactions = ['1️⃣', '2️⃣', '3️⃣', '❌']
        for emoji in reactions:
            await msg.add_reaction(emoji)

        # Define a check function to validate that the reaction is from the command author and is valid
        def check(reaction, user):
            return user == ctx.author and str(reaction.emoji) in reactions and reaction.message.id == msg.id

        # Wait for the user's reaction with a timeout of 60 seconds
        try:
            reaction, _ = await self.bot.wait_for("reaction_add", timeout=60.0, check=check)
        except asyncio.TimeoutError:
            await msg.edit(embed=timeout_embed())
            await msg.clear_reactions()
            return

        # If the user cancels the operation by reacting with ❌
        if str(reaction.emoji) == '❌':
            await msg.edit(embed=cancel_embed())
            return

        # Map the reaction emojis to the corresponding result index
        option_mapping = {'1️⃣': 0, '2️⃣': 1, '3️⃣': 2}
        chosen_index = option_mapping.get(str(reaction.emoji))
        if chosen_index is None or chosen_index >= len(results):
            await msg.edit(embed=error_embed())
            return

        # Retrieve the chosen video information
        chosen_video = results[chosen_index]
        track_title = chosen_video.get("title", "No title")
        # Add the selected track to the queue
        add_to_queue({"original_url": chosen_video.get("webpage_url"), "title": track_title})

        # Clear all reactions from the message
        await msg.clear_reactions()

        # Update the embed to indicate that the track was successfully added to the queue
        await msg.edit(embed=success_embed())

        # If the bot is not currently playing, invoke the play command to start playback
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            await ctx.invoke(self.bot.get_command('play'))

def setup(bot):
    bot.add_cog(Search(bot))
