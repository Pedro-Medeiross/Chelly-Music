import disnake

def success_playing_now_embed(
    current_track: str,
    duration_str: str,
    playing_time: str,
    progress_bar: str,
    current_vol: str,
    is_playing: bool
):
    if is_playing:
        reproducao = 'Reprodução ativa'
    else:
        reproducao = 'Reprodução pausada'
    return disnake.Embed(
        title="🎶  Tocando Agora",
        color=disnake.Color.from_rgb(40, 215, 155),  # Verde spotify
        description=(
            f"**🎻 │ Faixa:** \n`{current_track}`\n\n"
            f"**⏳ │ Progresso:**\n"
            f"{progress_bar}\n\n"
            f"**⌛ │ Duração Total:** `{duration_str}`"
        )
    ).set_thumbnail(
        url="https://cdn.discordapp.com/attachments/1081985250923651229/1339409398455599145/spectre.gif"
    ).add_field(
        name="📡 │ Status",
        value=f"```{reproducao} · 🔊 Volume: {current_vol}%```",
        inline=False
    ).set_footer(
        text="🎹 Música proporcionada por Chelly Music",
        icon_url="https://cdn.discordapp.com/attachments/1081985250923651229/1339409389748228116/e86b3f97d1364ae0fe4cdbb48cb388b4.gif"
    )
    
    
def no_playing_music_embed():
    return disnake.Embed(
      title="❌ Sem Música",
        description="O bot precisa estar tocando alguma música primeiro!",
        color=disnake.Color.red()
    )

def no_data_music_embed():
    return disnake.Embed(
      title="❌ Erro ao processar",
        description="Dados da música incompletos!",
        color=disnake.Color.red()
    )