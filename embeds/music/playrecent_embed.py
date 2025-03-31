import disnake

def empty_history_embed():
    return disnake.Embed(
                title="Histórico Vazio",
                description="Nenhuma música no histórico para reproduzir novamente",
                color=disnake.Color.orange()
            )
    
    
def success_add_recenplayed_embed(recent_tracks):
    embed = disnake.Embed(
            title="♻️ Histórico Recolocado",
            description=f"**{len(recent_tracks)} músicas** adicionadas à fila\n",
            color=disnake.Color.green()
        )
    embed.add_field(
            name="Ordem de Reprodução",
            value="As músicas serão tocadas na ordem original (mais antigas primeiro)",
            inline=False
        )