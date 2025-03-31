import disnake

def missing_query_embed(command_name: str):
    return disnake.Embed(
        title="❌ Argumento Faltando",
        description=f"Você precisa especificar uma música!\nExemplo: `!{command_name} Nome da Música`",
        color=disnake.Color.red()
    ).add_field(
        name="Dica",
        value="• Use aspas para frases longas\n• Cole links do YouTube/Spotify",
        inline=False
    )

def generic_error_embed(error: str):
    return disnake.Embed(
        title="⚠ Erro no Comando",
        description=f"```py\n{error}\n```",
        color=disnake.Color.orange()
    )