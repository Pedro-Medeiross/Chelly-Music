import asyncio
from disnake.ext import commands
from utils.queue_manager import music_queue  # Queue management for music tracks
from embeds.music.skip_embeds import (
    not_playing_embed,         # Embed for when no music is playing
    invalid_index_embed,       # Embed for invalid track index
    confirmation_embed,        # Embed requesting skip confirmation
    skip_vote_timeout_embed,   # Embed for skip vote timeout
    skip_success_embed,        # Embed for successful skip
    not_enough_votes_embed     # Embed for insufficient skip votes
)

class Skip(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['s', 'next'])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def skip(self, ctx, index: int = 1):
        """
        Skips to a specific track in the queue or initiates a vote to skip the current track.
        - Checks if music is currently playing.
        - Validates the provided track index.
        - Removes tracks up to the specified index.
        - Initiates a vote for skipping with reactions.
        - Skips the track if the vote passes.
        """
        # Check if the bot is currently playing music
        if not ctx.voice_client.is_playing():
            await ctx.send(embed=not_playing_embed())
            return

        # Validate the provided index
        if index > len(music_queue) or index < 1:
            await ctx.send(embed=invalid_index_embed(len(music_queue)))
            return

        # Remove tracks from the queue up to the specified index
        del music_queue[:index - 1]

        # Send confirmation embed and add reaction for voting
        confirmation_message = await ctx.send(embed=confirmation_embed())
        await confirmation_message.add_reaction("👍")

        # Check function to validate reactions
        def check(reaction, user):
            return (
                user != self.bot.user
                and str(reaction.emoji) == "👍"
                and user in ctx.voice_client.channel.members
            )

        try:
            # Wait for a reaction with a timeout of 30 seconds
            reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
        except asyncio.TimeoutError:
            # Send timeout embed if no reaction is received in time
            await ctx.send(embed=skip_vote_timeout_embed())
            return

        # Determine the number of votes required to skip
        required_votes = (len(ctx.voice_client.channel.members) - 1) // 2
        if reaction.count >= required_votes:
            ctx.voice_client.stop()  # Stop the current track
            await ctx.send(embed=skip_success_embed(index))
        else:
            await ctx.send(embed=not_enough_votes_embed())

def setup(bot):
    bot.add_cog(Skip(bot))