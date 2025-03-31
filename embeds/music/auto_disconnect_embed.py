import disnake

def paused_timeout_embed():
    return disnake.Embed(
        title="⏸️ Desconexão por Pausa Prolongada",
        description="```diff\n- O bot estava pausado por mais de 5 minutos```",
        color=disnake.Color.orange()
    ).add_field(
        name="Ações Realizadas",
        value="```• Conexão encerrada\n• Fila de músicas limpa\n• Arquivos temporários removidos```",
        inline=False
    )

def inactivity_timeout_embed():
    return disnake.Embed(
        title="🔇 Desconexão por Inatividade",
        description="```diff\n- Nenhuma atividade detectada por 3 minutos```",
        color=disnake.Color.red()
    ).add_field(
        name="Status da Limpeza",
        value="```• Reprodução interrompida\n• Recursos de áudio liberados\n• Canal de voz deixado```",
        inline=False
    )