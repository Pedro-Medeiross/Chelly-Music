import disnake
from disnake.ext import commands
from embeds.music.pause_embed import paused_embed, not_playing_embed

class Pause(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="pause")
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286, 732299321965412442, 673335179275796481, 809903409385177108, 1272690192117137449)
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
