import disnake

def queue_cleared_embed():
    """
    Retorna um embed informando que a fila de reprodução foi limpa com sucesso.
    """
    return disnake.Embed(
        title="Fila Limpa",
        description="A fila de reprodução foi limpa com sucesso.",
        color=disnake.Color.green()
    )

def queue_empty_embed():
    """
    Retorna um embed informando que não há músicas na fila para serem apagadas.
    """
    return disnake.Embed(
        title="Fila Vazia",
        description="Não há músicas na fila para serem apagadas.",
        color=disnake.Color.orange()
    )
