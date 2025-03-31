import disnake

def not_connected_embed():
    """Embed exibido quando o bot não está conectado a um canal de voz."""
    return disnake.Embed(
        title="Não conectado",
        description="Não estou conectado a um canal de voz.",
        color=disnake.Color.red()
    )

def not_paused_embed():
    """Embed exibido quando a reprodução não está pausada."""
    return disnake.Embed(
        title="Não pausado",
        description="A reprodução não está pausada.",
        color=disnake.Color.orange()
    )

def resumed_embed():
    """Embed exibido quando a reprodução é retomada com sucesso."""
    return disnake.Embed(
        title="Reprodução retomada",
        description="A reprodução foi retomada.",
        color=disnake.Color.green()
    )
