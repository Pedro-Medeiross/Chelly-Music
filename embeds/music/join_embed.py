import disnake

def already_in_channel_embed():
    return disnake.Embed(
        title="⏺ Já Estou Aqui",
        description="Já estou conectado ao seu canal de voz!",
        color=disnake.Color.blue()
    )

def busy_embed():
    return disnake.Embed(
        title="⚠ Canal Ocupado",
        description="Estou ocupado em outro canal de voz!",
        color=disnake.Color.orange()
    )

def connect_first_embed():
    return disnake.Embed(
        title="❌ Sem Conexão",
        description="Entre em um canal de voz primeiro!",
        color=disnake.Color.red()
    )

def conflict_embed():
    return disnake.Embed(
        title="🚫 Conflito de Bots",
        description="Já existe um bot de música neste canal!",
        color=disnake.Color.red()
    )

def join_success_embed(channel):
    return disnake.Embed(
        title="✅ Conexão Bem-sucedida",
        description=f"Conectado a {channel.mention}!", # Menção do canal
        color=disnake.Color.green()
    )

def connection_failed_embed(error):
    return disnake.Embed(
        title="💥 Falha na Conexão",
        description=f"Erro ao conectar:\n```{error}```",
        color=disnake.Color.red()
    )