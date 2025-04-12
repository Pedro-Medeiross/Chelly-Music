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
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
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