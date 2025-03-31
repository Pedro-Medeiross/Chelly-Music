import disnake
from disnake import Embed

def create_history_embed(page: int, total_pages: int, tracks: list) -> Embed:
    """Cria embed paginado para o histórico de reprodução"""
    start_idx = (page - 1) * 10
    end_idx = start_idx + 10
    page_tracks = tracks[start_idx:end_idx]

    embed = Embed(
        title="⏳ Histórico de Reprodução",
        color=disnake.Color.blurple(),
        description=f"Página **{page}** de **{total_pages}**"
    )
    
    for i, track in enumerate(page_tracks, start=start_idx + 1):
        embed.add_field(
            name=f"{i}. {track.title}",
            value=f"[🔗 Link]({track.original_url})",
            inline=False
        )
    
    embed.set_footer(text="Navegue usando os botões abaixo")
    return embed

def create_history_empty_embed() -> Embed:
    """Embed para histórico vazio"""
    return Embed(
        title="Histórico Vazio",
        description="🎵 Nenhuma música foi tocada recentemente",
        color=disnake.Color.blue()
    )

def create_history_error_embed(error: Exception = None) -> Embed:
    """Embed para erros no histórico"""
    embed = Embed(
        title="⚠️ Erro no Histórico",
        color=disnake.Color.red()
    )
    if error:
        embed.description = f"```{str(error)[:2000]}```"
    else:
        embed.description = "Ocorreu um erro ao carregar o histórico"
    return embed