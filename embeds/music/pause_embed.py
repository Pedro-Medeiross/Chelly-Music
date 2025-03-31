import disnake

def paused_embed():
    """Retorna um embed informando que a reprodução foi pausada."""
    return disnake.Embed(
        title="Reprodução pausada",
        description="A faixa atual foi pausada.",
        color=disnake.Color.orange()
    )

def not_playing_embed():
    """Retorna um embed informando que não há nenhuma faixa sendo reproduzida."""
    return disnake.Embed(
        title="Não está tocando",
        description="Nenhuma faixa está sendo reproduzida no momento.",
        color=disnake.Color.red()
    )
