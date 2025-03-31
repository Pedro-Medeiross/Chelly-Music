import disnake

def success_embed():
    return disnake.Embed(
        title="🎶  Desconexão Concluída",
        description="**Todas as operações foram finalizadas com sucesso!**",
        color=disnake.Color.green()
    ).add_field(
        name="📋 Ações Realizadas",
        value=(
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            "• ⏹️ Reprodução interrompida\n"
            "• 🗑️ Arquivos temporários removidos\n"
            "• 📭 Conexão de voz encerrada\n"
            "⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
        ),
        inline=False
    ).set_footer(
        text="Pronto para nova conexão!",
    )

def not_connected_embed():
    return disnake.Embed(
        title="🔇 Sem Conexão Ativa",
        description="**Não estou conectado a nenhum canal de voz no momento**",
        color=disnake.Color.red()
    ).add_field(
        name="O que fazer?",
        value=(
            "➺ Entre em um canal de voz\n"
            "➺ Use `/play` para iniciar a música\n"
            "➺ Verifique as permissões do canal"
        ),
        inline=False
    ).set_author(
        name="Sistema de Áudio Chelly",
    )

def forced_disconnect_embed():
    return disnake.Embed(
        title="⚠️  Desconexão Administrativa",
        description="**Conexão interrompida por ação manual**",
        color=disnake.Color.orange()
    ).add_field(
        name="Medidas Tomadas",
        value=(
            "▸ Interrupção imediata do áudio\n"
            "▸ Liberação de recursos do sistema\n"
            "▸ Reset completo da fila musical"
        ),
        inline=False
    ).add_field(
        name="Detalhes",
        value="*Ação realizada através do menu de contexto ou comando de moderação*",
        inline=False
    )