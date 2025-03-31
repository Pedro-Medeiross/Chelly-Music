import disnake

def bot_conflict_embed():
    return disnake.Embed(
        title="🚫 Conflito de Bots",
        description="Já existe um bot de música no canal!",
        color=disnake.Color.red()
    )
    
def search_embed(query):
    return disnake.Embed(
        title="🔍 Buscando",
        description=f"Pesquisando por ai por: \n`{query}`",
        color=disnake.Color.orange()
    )

def search_failed_embed(query):
    return disnake.Embed(
        title="🔍 Falha na Busca",
        description=f"Nenhum resultado encontrado para:\n`{query}`",
        color=disnake.Color.orange()
    )

def spotify_error_embed(error):
    return disnake.Embed(
        title="🎵 Erro no Spotify",
        description=f"```py\n{error}\n```",
        color=disnake.Color.red()
    )

def track_added_embed(track_info, position=0):
    embed = disnake.Embed(
        title="⏭ Música Prioritária",
        description=f"**Próxima a tocar:** [{track_info['title']}]({track_info['url']})",
        color=disnake.Color.green()
    )
    if track_info.get('thumbnail'):
        embed.set_thumbnail(url=track_info['thumbnail'])
    if track_info.get('duration'):
        embed.add_field(name="Duração", value=track_info['duration'])
    return embed

def conversion_embed(platform, track):
    return disnake.Embed(
        title="🔀 Conversão Bem-sucedida",
        description=f"Convertido de {platform}:\n`{track}`",
        color=disnake.Color.blue()
    )

def processing_error_embed(error):
    return disnake.Embed(
        title="⚠ Erro de Processamento",
        description=f"```py\n{error}\n```",
        color=disnake.Color.red()
    )
    
def playlist_warning_embed():
    return disnake.Embed(
        title="🔀 Playlist Detectada",
        description="Só é possível adicionar uma música por vez!\nA primeira da playlist será adicionada como próxima na fila.",
        color=disnake.Color.orange()
    )
    
def playlist_spotify_warning_embed():
    return disnake.Embed(
        title="⚠ Playlist do Spotify Não Suportada",
        description="Converta músicas individuais do Spotify!",
        color=disnake.Color.red()
        )
    
def bot_not_connected_embed():
    return disnake.Embed(
        title="🔇 Bot Desconectado",
        description="O bot precisa estar conectado em um canal de voz primeiro!",
        color=disnake.Color.red()
    )

def wrong_channel_embed():
    return disnake.Embed(
        title="🔀 Canal Incorreto",
        description="Você precisa estar no mesmo canal que o bot!",
        color=disnake.Color.orange()
    )
    
def user_not_connected_embed():
    return disnake.Embed(
        title="🎧 Sem Conexão",
        description="Você precisa estar conectado a um canal de voz!",
        color=disnake.Color.red()
    )
    
def connection_failed_embed():
        return disnake.Embed(
        title="❌ Falha na Conexão",
        description="O bot não conseguiu se conectar ao canal!",
        color=disnake.Color.red()
    )