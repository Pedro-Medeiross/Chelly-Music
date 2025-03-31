from disnake.ext import commands
from embeds.music.errors.error_embeds import missing_query_embed

class AddNextCommandErrorHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """Centraliza o tratamento de erros"""
        
        # Erro específico para comandos de música addnext
        if isinstance(error, commands.MissingRequiredArgument):
            if ctx.command.name in ['addnext', 'insert', 'add_next', 'priority_queue']:
                await ctx.send(embed=missing_query_embed(ctx.command.name))
                return
            
def setup(bot):
    bot.add_cog(AddNextCommandErrorHandler(bot))