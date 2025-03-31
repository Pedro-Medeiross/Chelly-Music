import disnake

def lyrics_found_embed(title: str, artist: str, lyrics: str, url: str):
    """
    Retorna um embed com a letra da música encontrada (para letras curtas).
    """
    embed = disnake.Embed(
        title=f"Lyrics: {title} - {artist}",
        description=lyrics,
        color=disnake.Color.blue()
    )
    embed.add_field(name="Leia a letra completa", value=f"[Clique aqui]({url})", inline=False)
    embed.set_footer(text="Letra fornecida por Genius")
    return embed

def lyrics_not_found_embed(song: str):
    """
    Retorna um embed informando que a letra da música não foi encontrada.
    """
    return disnake.Embed(
        title="Letra não encontrada",
        description=f"Não consegui encontrar a letra para **{song}**.",
        color=disnake.Color.red()
    )

def lyrics_error_embed(error: str):
    """
    Retorna um embed informando que ocorreu um erro ao buscar a letra.
    """
    return disnake.Embed(
        title="Erro ao buscar letra",
        description=f"Ocorreu um erro: {error}",
        color=disnake.Color.red()
    )

def no_playing_music_embed():
    """
    Retorna um embed informando que não há nenhuma música tocando.
    """
    return disnake.Embed(
        title="Nenhuma Música Tocando",
        description="Não há nenhuma música tocando no momento.",
        color=disnake.Color.orange()
    )
