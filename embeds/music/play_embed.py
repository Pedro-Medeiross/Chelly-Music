import disnake

def success_playing_now_embed(
    current_track: str,
    duration_str: str,
    playing_time: str,
    current_vol: str,
    is_playing: bool
):
    
    reproducao = "Reprodução ativa" if is_playing else "Reprodução pausada"
    embed = disnake.Embed(
        title="🎶 Tocando Agora",
        color=disnake.Color.from_rgb(40, 215, 155),
        description=(
            f"**🎻 │ Faixa:**\n`{current_track}`\n\n"
            f"**⌛ │ Duração Total:** `{duration_str}`"
        )
    )
    embed.set_footer(
        text="🎹 Música proporcionada por Chelly Music",
    )
    return embed

def no_playing_music_embed():
    return disnake.Embed(
        title="❌ Sem Música",
        description="O bot precisa estar tocando alguma música primeiro!",
        color=disnake.Color.red()
    )

def no_data_music_embed():
    return disnake.Embed(
        title="❌ Erro ao Processar",
        description="Dados da música incompletos!",
        color=disnake.Color.red()
    )

def voice_channel_error_embed():
    return disnake.Embed(
        title="❌ Canal de Voz",
        description="Você deve estar em um canal de voz para tocar música!",
        color=disnake.Color.red()
    )

def already_connected_embed():
    return disnake.Embed(
        title="❌ Não é possivel conectar",
        description="Estou sendo usado em outro canal de voz.",
        color=disnake.Color.red()
    )

def connection_failed_embed():
    return disnake.Embed(
        title="❌ Falha na Conexão",
        description="Falha ao conectar no canal de voz.",
        color=disnake.Color.red()
    )

def empty_playlist_embed():
    return disnake.Embed(
        title="❌ Playlist Vazia",
        description="A playlist não contém faixas.",
        color=disnake.Color.red()
    )

def track_added_embed(title: str, artist: str = ""):
    description = f"Adicionado à fila: **{title}**"
    if artist:
        description += f" por **{artist}**"
    return disnake.Embed(
        title="✅ Faixa Adicionada",
        description=description,
        color=disnake.Color.green()
    )

def track_queued_embed(title: str):
    return disnake.Embed(
        title="✅ Faixa na Fila",
        description=f'Faixa enfileirada: **{title}**',
        color=disnake.Color.green()
    )

def download_error_embed(error_message: str):
    return disnake.Embed(
        title="❌ Erro de Download",
        description=f"Download error: {error_message}",
        color=disnake.Color.red()
    )

def playback_error_embed(error_message: str):
    return disnake.Embed(
        title="❌ Erro de Reprodução",
        description=f"Playback error: {error_message}",
        color=disnake.Color.red()
    )

def added_playlist_tracks_embed(count: int):
    return disnake.Embed(
        title="✅ Playlist Adicionada",
        description=f"Adicionados **{count}** faixas à fila.",
        color=disnake.Color.green()
    )

def spotify_not_found_embed():
    return disnake.Embed(
        title="❌ Música Não Encontrada",
        description="Não foi possível encontrar a música no YouTube.",
        color=disnake.Color.red()
    )

def youtube_not_found_embed():
    return disnake.Embed(
        title="❌ Música Não Encontrada",
        description="Could not find the music on YouTube.",
        color=disnake.Color.red()
    )

def adding_playlist_embed():
    return disnake.Embed(
            title="🎶 Adicionando Playlist",
            description="Adicionando as músicas da playlist...",
            color=disnake.Color.blue()
        )
    
def processing_spotify_playlist(total_tracks: int):
    return disnake.Embed(
            title="⏳ Processando Playlist do Spotify",
            description=f"Adicionando {total_tracks} músicas...",
            color=disnake.Color.blue()
    )
    
def processing_youtube_playlist(total_tracks: int):
    return disnake.Embed(
            title="⏳ Processando Playlist do YouTube",
            description=f"Adicionando {total_tracks} músicas...",
            color=disnake.Color.blue()
        )