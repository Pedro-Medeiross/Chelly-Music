import disnake  # Importing the Disnake library for Discord API interactions
from disnake.ext import commands  # Importing the commands extension from Disnake
from utils.queue_manager import get_recent_tracks  # Function to retrieve recently played tracks
from embeds.music.recentplayed_embed import (
    create_history_embed,  # Function to create an embed displaying the history
    create_history_empty_embed,  # Function to create an embed indicating an empty history
    create_history_error_embed  # Function to create an embed for error messages
)

class HistoryPaginationView(disnake.ui.View):
    """
    A custom UI view for paginating the history of recently played tracks.
    
    This view creates interactive buttons that allow users to navigate through different pages
    of the recently played tracks list.
    """
    def __init__(self, tracks: list, timeout: float = 60.0):
        """
        Initialize the HistoryPaginationView.
        
        :param tracks: List of recently played tracks.
        :param timeout: Duration in seconds after which the view will become inactive.
        """
        super().__init__(timeout=timeout)
        self.page = 1  # Current page index
        self.tracks = tracks  # List of tracks to paginate
        self.total_pages = max(1, (len(tracks) + 10 - 1) // 10)  # Calculate total pages (10 tracks per page)
        self.update_buttons()  # Set the initial state for navigation buttons

    def update_buttons(self):
        """
        Update the disabled state of pagination buttons based on the current page index.
        """
        self.children[0].disabled = self.page == 1  # Disable 'previous' if on the first page
        self.children[1].disabled = self.page == self.total_pages  # Disable 'next' if on the last page

    def get_embed(self):
        """
        Create and return the embed representing the current history page.
        
        :return: A disnake.Embed object with the history details.
        """
        return create_history_embed(self.page, self.total_pages, self.tracks)

    @disnake.ui.button(emoji="⬅️", style=disnake.ButtonStyle.blurple)
    async def previous_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """
        Button callback to move to the previous page of the history.
        
        Updates the current page index, refreshes button states, and edits the message with the new embed.
        """
        self.page = max(1, self.page - 1)  # Decrement page index but not below 1
        self.update_buttons()  # Refresh button states
        await interaction.response.edit_message(embed=self.get_embed(), view=self)  # Update the message

    @disnake.ui.button(emoji="➡️", style=disnake.ButtonStyle.blurple)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """
        Button callback to move to the next page of the history.
        
        Updates the current page index, refreshes button states, and edits the message with the new embed.
        """
        self.page = min(self.total_pages, self.page + 1)  # Increment page index but not above total_pages
        self.update_buttons()  # Refresh button states
        await interaction.response.edit_message(embed=self.get_embed(), view=self)  # Update the message

class RecentPlayed(commands.Cog):
    """
    Cog that handles the recentplayed command to display the history of played tracks.
    
    This cog retrieves the recently played tracks, paginates them, and sends an interactive
    embed with navigation buttons to the channel.
    """
    def __init__(self, bot):
        self.bot = bot  # Reference to the main bot instance

    @commands.command(aliases=["history", "recent"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def recentplayed(self, ctx):
        """
        Command to display the history of recently played tracks.
        
        Retrieves the recently played tracks, paginates them into chunks (10 tracks per page),
        and sends an interactive embed with pagination buttons.
        
        :param ctx: Command context representing the invocation details.
        """
        try:
            recent_tracks = get_recent_tracks()  # Fetch recently played tracks
            
            if not recent_tracks:
                # If no tracks have been played recently, send an embed indicating an empty history
                return await ctx.send(embed=create_history_empty_embed())

            # Create an instance of the HistoryPaginationView with the list of recent tracks
            view = HistoryPaginationView(recent_tracks)
            # Send the initial embed message with the view attached for interactive pagination
            await ctx.send(embed=view.get_embed(), view=view)

        except Exception as e:
            # On error, send an error embed and auto-delete the message after 15 seconds
            await ctx.send(embed=create_history_error_embed(e), delete_after=15)

def setup(bot):
    """
    Register the RecentPlayed cog with the bot.
    
    This function adds the RecentPlayed cog to the bot's list of cogs, making its commands available.
    """
    bot.add_cog(RecentPlayed(bot))
