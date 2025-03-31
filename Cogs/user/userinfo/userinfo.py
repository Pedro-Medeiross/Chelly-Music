import asyncio
import disnake
import typing
from disnake.ext import commands
from pillow.userinfo_pillow import create_user_info_canvas

class Userinfo(commands.Cog):
    
    def __init__(self, client):
        self.client = client
        
    @commands.cooldown(1, 3, commands.BucketType.user)
    @commands.command(pass_context=True)
    async def userinfo(self, ctx, user: typing.Optional[disnake.Member] = None):
        """
        Show user info on current server
        :param ctx: Command Context
        :param user: Discord member to get info
        """
        
        # Delete the user's message that invoked the command
        await ctx.message.delete()
        
        # Send a message to the channel indicating that the command is being executed
        r = await ctx.send("O Chelly Bot está executando o comando")  # Chelly Bot is executing the command
        
        member = user if user else ctx.author
        
        # Debug print
        print(member)
        
        # Create the image with user info
        buffer = create_user_info_canvas(member)
        
        # Send the image to the channel
        await ctx.send(file=disnake.File(buffer, filename="user_info.png"))

def setup(client):
    client.add_cog(Userinfo(client))
