import asyncio
import disnake
from disnake.ext import commands
from embeds.music.volume_embed import (
    current_volume_embed,  # Embed to show the current volume level
    volume_updated_embed,  # Embed to confirm that the volume has been updated
    not_playing_embed,     # Embed to indicate that no track is playing
    invalid_volume_embed   # Embed to indicate an invalid volume value was provided
)

class Volume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="volume", aliases=["vol"])
    async def volume(self, ctx, volume: int = None):
        """
        Adjusts the volume of the current track.
        
        - If a volume value is provided, it adjusts the volume directly.
        - Otherwise, it starts an interactive menu using reactions to increase or decrease the volume.
        """
        # Check if the bot is connected to a voice channel and if it is currently playing audio
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send(embed=not_playing_embed())
        
        source = ctx.voice_client.source
        # Ensure the current audio source supports volume adjustment (e.g., using PCMVolumeTransformer)
        if not hasattr(source, "volume"):
            return await ctx.send("The current audio source does not support volume adjustments.")

        # Direct mode: if a volume value is provided, adjust the volume immediately
        if volume is not None:
            if volume < 0 or volume > 100:
                return await ctx.send(embed=invalid_volume_embed())
            source.volume = volume / 100.0  # Normalize volume to a 0.0 - 1.0 scale
            return await ctx.send(embed=volume_updated_embed(volume))
        
        # Interactive mode: no volume value provided; show current volume and allow interactive adjustments
        current_volume = int(source.volume * 100)
        msg = await ctx.send(embed=current_volume_embed(current_volume))
        # Add reaction emojis for increasing, decreasing, confirming, or canceling the volume adjustment
        reactions = ["🔼", "🔽", "✅", "❌"]
        for emoji in reactions:
            await msg.add_reaction(emoji)

        # Define a check function to validate that the reaction is from the command invoker and is valid
        def check(reaction, user):
            return (
                user == ctx.author and
                str(reaction.emoji) in reactions and
                reaction.message.id == msg.id
            )
        
        # Interactive loop for volume adjustments
        while True:
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=30.0, check=check)
            except asyncio.TimeoutError:
                # On timeout, finalize the volume adjustment with the current volume
                await msg.edit(embed=volume_updated_embed(current_volume))
                break
            
            # Remove the user's reaction to allow multiple adjustments
            await msg.remove_reaction(reaction.emoji, user)
            
            if str(reaction.emoji) == "🔼":
                # Increase volume by 10%, ensuring it does not exceed 100%
                current_volume = min(current_volume + 10, 100)
                source.volume = current_volume / 100.0
                await msg.edit(embed=current_volume_embed(current_volume))
            elif str(reaction.emoji) == "🔽":
                # Decrease volume by 10%, ensuring it does not drop below 0%
                current_volume = max(current_volume - 10, 0)
                source.volume = current_volume / 100.0
                await msg.edit(embed=current_volume_embed(current_volume))
            elif str(reaction.emoji) == "✅":
                # Confirm the volume setting and exit the interactive loop
                await msg.edit(embed=volume_updated_embed(current_volume))
                break
            elif str(reaction.emoji) == "❌":
                # Cancel the volume adjustment and notify the user
                await msg.edit(embed=disnake.Embed(
                    title="Volume Adjustment Cancelled",
                    description=f"The volume remains at **{current_volume}%**.",
                    color=disnake.Color.orange()
                ))
                break
        
        # Attempt to clear all reactions from the message for a clean interface
        try:
            await msg.clear_reactions()
        except Exception:
            pass

def setup(bot):
    bot.add_cog(Volume(bot))
