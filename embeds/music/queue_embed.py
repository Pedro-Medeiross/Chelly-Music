import disnake
from disnake import Embed

def create_queue_embed(current_track: dict, queue_page: list, current_page: int, total_pages: int) -> Embed:
    """Cria embed para exibição da fila de reprodução"""
    embed = Embed(
        title="🎶 Fila de Reprodução",
        color=disnake.Color.blurple()
    )
    
    # Seção da música atual
    current_text = (
        f"**{current_track.get('title', 'Título desconhecido')}**\n"
        f"🔗 [Link da música]({current_track.get('original_url', '')})"
    ) if current_track else "`Nenhuma música tocando no momento`"
    
    embed.add_field(
        name="🎵 Tocando Agora",
        value=current_text,
        inline=False
    )

    # Seção da fila
    if queue_page:
        queue_items = [
            f"**{(current_page * 10) + i + 1}.** {track.get('title', 'Título desconhecido')}\n"
            f"🔗 [Link]({track.get('original_url', '')})"
            for i, track in enumerate(queue_page)
        ]
        queue_text = "\n\n".join(queue_items)
    else:
        queue_text = "`A fila está vazia`"

    page_info = f"Página {current_page + 1}/{total_pages}" if total_pages > 0 else "Página 1/1"
    
    embed.add_field(
        name=f"🔜 Próximas Músicas ({page_info})",
        value=queue_text,
        inline=False
    )
    
    return embed

def create_error_embed(error: Exception) -> Embed:
    """Cria embed para erros na exibição da fila"""
    return Embed(
        title="⚠️ Erro na Fila",
        description=f"```py\n{str(error)[:2000]}\n```",
        color=disnake.Color.red()
    )