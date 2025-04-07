import disnake
from disnake.ext import commands
import os
import lyricsgenius
from embeds.music.lyrics_embed import (
    lyrics_found_embed,
    lyrics_not_found_embed,
    lyrics_error_embed,
    no_playing_music_embed
)

# Obtém o token da API do Genius a partir das variáveis de ambiente
GENIUS_ACCESS_TOKEN = os.getenv("GENIUS_ACCESS_TOKEN")
if not GENIUS_ACCESS_TOKEN:
    raise Exception("GENIUS_ACCESS_TOKEN não configurado nas variáveis de ambiente.")

# Inicializa o cliente Genius; remove cabeçalhos de seção da letra para simplificar a exibição
genius = lyricsgenius.Genius(GENIUS_ACCESS_TOKEN, timeout=15, retries=3, remove_section_headers=True)

class Lyrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="lyrics", aliases=["letra"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def lyrics(self, ctx, *, song: str = None):
        """
        Busca a letra completa da música e a envia no chat.
        
        Se nenhum parâmetro for fornecido, usa o título da música que está tocando.
        """
        # Se o usuário não informar uma query, tenta usar a música que está tocando
        if song is None:
            if not ctx.voice_client or not ctx.voice_client.is_playing() or not hasattr(ctx.voice_client.source, "title"):
                return await ctx.send(embed=no_playing_music_embed())
            song = ctx.voice_client.source.title

        await ctx.send(f"🔍 Buscando a letra completa de **{song}**...")

        try:
            found_song = genius.search_song(song)
            if not found_song:
                return await ctx.send(embed=lyrics_not_found_embed(song))
            
            full_lyrics = found_song.lyrics
            title = found_song.title
            artist = found_song.artist
            url = found_song.url

            # Se a letra for muito longa para um embed, envia como arquivo
            if len(full_lyrics) > 2048:
                embed = disnake.Embed(
                    title=f"Lyrics: {title} - {artist}",
                    description="A letra é muito longa e foi enviada como arquivo anexo.",
                    color=disnake.Color.blue()
                )
                embed.set_footer(text="Letra fornecida por Genius")
                file = disnake.File(fp=full_lyrics.encode("utf-8"), filename="lyrics.txt")
                await ctx.send(embed=embed, file=file)
            else:
                embed = lyrics_found_embed(title, artist, full_lyrics, url)
                await ctx.send(embed=embed)
        except Exception as e:
            await ctx.send(embed=lyrics_error_embed(str(e)))

def setup(bot):
    bot.add_cog(Lyrics(bot))
