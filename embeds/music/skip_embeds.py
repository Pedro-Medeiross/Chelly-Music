import disnake

def not_playing_embed():
    """Embed exibido quando não há nenhuma música tocando."""
    return disnake.Embed(
        title="Pular",
        description="Nenhuma faixa está sendo reproduzida no momento.",
        color=disnake.Color.red()
    )

def invalid_index_embed(max_index: int):
    """Embed exibido quando o índice informado é inválido."""
    return disnake.Embed(
        title="Índice inválido",
        description=f"Índice inválido. Forneça um número entre 1 e {max_index}.",
        color=disnake.Color.red()
    )

def confirmation_embed():
    """Embed exibido solicitando confirmação para pular a música atual."""
    return disnake.Embed(
        title="Pular confirmação",
        description="Você quer pular a faixa atual? Reaja com 👍 para pular.",
        color=disnake.Color.blue()
    )

def skip_vote_timeout_embed():
    """Embed exibido quando o tempo para votar expira."""
    return disnake.Embed(
        title="Tempo limite para pular votação",
        description="Tempo limite para pular votação esgotado.",
        color=disnake.Color.orange()
    )

def skip_success_embed(index: int):
    """Embed exibido quando a música é pulada com sucesso."""
    return disnake.Embed(
        title="Faixa pulada",
        description=f"Pular para a faixa {index}.",
        color=disnake.Color.green()
    )

def not_enough_votes_embed():
    """Embed exibido quando não há votos suficientes para pular a música."""
    return disnake.Embed(
        title="Não há votos suficientes",
        description="Não há votos suficientes para pular a faixa atual.",
        color=disnake.Color.red()
    )
