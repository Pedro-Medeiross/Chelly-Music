import disnake
from disnake.ext import commands
from embeds.music.resume_embed import (
    not_connected_embed,  # Embed indicating the bot is not connected to a voice channel
    not_paused_embed,     # Embed indicating the audio is not currently paused
    resumed_embed         # Embed confirming the audio has been resumed
)

class Resume(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="resume")
    async def resume(self, ctx):
        """
        Resumes the current audio playback if it is paused.
        """
        # Check if the bot is connected to a voice channel
        if not ctx.voice_client:
            return await ctx.send(embed=not_connected_embed())

        # Check if the audio is currently paused
        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()  # Resume playback
            await ctx.send(embed=resumed_embed())
        else:
            await ctx.send(embed=not_paused_embed())

def setup(bot):
    bot.add_cog(Resume(bot))