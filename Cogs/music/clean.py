import disnake
from disnake.ext import commands
from embeds.music.clean_embed import (
    clean_success_embed,  # Embed indicating successful deletion of messages
    clean_failure_embed,  # Embed indicating failure in deleting messages
    no_messages_embed     # Embed indicating no messages were found to delete
)

class Clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="clean")
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def clean(self, ctx, limit: int = None):
        """
        Removes the bot's messages from the channel where the command was executed.

        If a limit is provided, only that number of messages will be scanned.
        Otherwise, the bot will attempt to delete all its messages found in the last 1000 records.
        """
        # Delete the command message to keep the chat clean
        await ctx.message.delete()

        def is_bot_message(message):
            return message.author == self.bot.user

        try:
            # Set the number of messages to scan
            scan_limit = limit if limit is not None else 1000
            # Purge the bot's messages from the channel
            deleted = await ctx.channel.purge(limit=scan_limit, check=is_bot_message)

            if not deleted:
                # If no messages were deleted, send an embed indicating this
                await ctx.send(embed=no_messages_embed(), delete_after=5)
            else:
                # If messages were deleted, send an embed with the count of deleted messages
                await ctx.send(embed=clean_success_embed(len(deleted)), delete_after=5)
        except Exception as e:
            # If an error occurs during deletion, send an embed with the error message
            await ctx.send(embed=clean_failure_embed(str(e)), delete_after=5)

def setup(bot):
    bot.add_cog(Clean(bot))
