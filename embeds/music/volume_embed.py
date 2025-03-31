import disnake

def current_volume_embed(volume: int):
    """
    Retorna um embed mostrando o volume atual e as instruções para ajustar.
    """
    return disnake.Embed(
        title="Controle de volume",
        description=(
            f"Volume atual: **{volume}%**\n\n"
            "Reaja com 🔼 para aumentar ou 🔽 para diminuir o volume.\n"
            "Reaja com ✅ para confirmar ou ❌ para cancelar."
        ),
        color=disnake.Color.blurple()
    )

def volume_updated_embed(volume: int):
    """
    Retorna um embed informando que o volume foi atualizado.
    """
    return disnake.Embed(
        title="Volume Atualizado",
        description=f"O volume foi definido para **{volume}%**.",
        color=disnake.Color.green()
    )

def not_playing_embed():
    """
    Retorna um embed informando que não há faixa sendo reproduzida.
    """
    return disnake.Embed(
        title="Não está tocando",
        description="Nenhuma faixa está tocando no momento para ajustar o volume.",
        color=disnake.Color.red()
    )

def invalid_volume_embed():
    """
    Retorna um embed informando que o valor informado é inválido.
    """
    return disnake.Embed(
        title="Volume inválido",
        description="Forneça um valor de volume entre 0 e 100.",
        color=disnake.Color.red()
    )
