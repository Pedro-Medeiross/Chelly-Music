import disnake

def voice_channel_error_embed():
    embed = disnake.Embed(
        title="Erro",
        description="Você precisa estar em um canal de voz para usar este comando.",
        color=disnake.Color.red()
    )
    return embed

def not_connected_embed():
    embed = disnake.Embed(
        title="Não Conectado",
        description="O bot não está conectado a um canal de voz.",
        color=disnake.Color.orange()
    )
    return embed

def youtube_not_found_embed():
    embed = disnake.Embed(
        title="Nenhum Resultado",
        description="Não foram encontrados resultados para a sua busca no YouTube.",
        color=disnake.Color.orange()
    )
    return embed

def track_added_embed(track_title):
    embed = disnake.Embed(
        title="Música Adicionada",
        description=f"**{track_title}** foi adicionada à fila.",
        color=disnake.Color.green()
    )
    return embed

def search_results_embed(results):
    embed = disnake.Embed(
        title="Resultados da Busca",
        color=disnake.Color.blurple()
    )
    description = ""
    for idx, video in enumerate(results[:3]):
        title = video.get("title", "Sem título")
        link = video.get("webpage_url", "")
        duration = video.get("duration", "N/A")
        description += f"{idx+1}. [{title}]({link}) - {duration}\n"
    embed.description = description
    embed.set_footer(text="Reaja com 1️⃣, 2️⃣ ou 3️⃣ para escolher, ou ❌ para cancelar.")
    return embed

def timeout_embed():
    embed = disnake.Embed(
        title="Tempo Esgotado",
        description="Você não reagiu a tempo.",
        color=disnake.Color.red()
    )
    return embed

def cancel_embed():
    embed = disnake.Embed(
        title="Busca Cancelada",
        description="Operação cancelada.",
        color=disnake.Color.orange()
    )
    return embed

def error_embed():
    embed = disnake.Embed(
        title="Erro",
        description="Opção inválida.",
        color=disnake.Color.red()
    )
    return embed

def searching_embed():
    """
    Retorna um embed informando que a busca está em andamento.
    """
    return disnake.Embed(
        title="Procurando...",
        description="Por favor, aguarde enquanto procuro os resultados.",
        color=disnake.Color.blue()
    )

def success_embed(track_title: str):
    """
    Retorna um embed informando que a faixa foi adicionada à fila.
    """
    return disnake.Embed(
        title="Faixa adicionada",
        description=f"**{track_title}** foi adicionado à fila.",
        color=disnake.Color.green()
    )