import disnake
from disnake.ext import commands
from embeds.music.pause_embed import paused_embed, not_playing_embed

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pause")
    async def pause(self, ctx):
        """
        Pausa a reprodução atual.
        
        Verifica se o bot está conectado e reproduzindo, caso afirmativo, pausa o áudio.
        """
        if not ctx.voice_client or not ctx.voice_client.is_playing():
            return await ctx.send(embed=not_playing_embed())

        ctx.voice_client.pause()
        await ctx.send(embed=paused_embed())

def setup(bot):
    bot.add_cog(Pause(bot))
