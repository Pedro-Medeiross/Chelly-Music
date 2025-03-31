import disnake

def clean_success_embed(deleted_count: int):
    """
    Retorna um embed informando quantas mensagens do bot foram apagadas.
    """
    return disnake.Embed(
        title="Limpeza Concluída",
        description=f"Foram deletadas {deleted_count} mensagens do bot.",
        color=disnake.Color.green()
    )

def clean_failure_embed(error: str):
    """
    Retorna um embed informando que ocorreu um erro durante a limpeza.
    """
    return disnake.Embed(
        title="Falha na Limpeza",
        description=f"Ocorreu um erro: {error}",
        color=disnake.Color.red()
    )

def no_messages_embed():
    """
    Retorna um embed informando que não há mensagens do bot para serem apagadas.
    """
    return disnake.Embed(
        title="Nenhuma Mensagem Encontrada",
        description="Não há mensagens do bot para serem apagadas neste canal.",
        color=disnake.Color.orange()
    )
