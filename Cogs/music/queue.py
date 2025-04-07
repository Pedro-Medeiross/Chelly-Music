import disnake  # Discord API library for Python
from disnake.ext import commands  # Bot command framework for creating cogs and commands
from utils.queue_manager import show_queue, get_current_track  # Functions to retrieve the current queue and track
from embeds.music.queue_embed import (
    create_queue_embed,  # Function to create an embed that displays the music queue
    create_error_embed   # Function to create an embed that displays error messages
)

class QueueView(disnake.ui.View):
    """
    A custom UI view for paginating the music queue.
    
    This view creates interactive buttons that allow users to navigate through different pages of the queue.
    It also supports deleting the message with a dedicated button.
    """
    def __init__(self, queue_pages: list, current_track: dict, timeout: float = 60):
        """
        Initialize the QueueView.
        
        :param queue_pages: List of pages, each page being a sub-list of queue entries.
        :param current_track: Dictionary containing metadata of the currently playing track.
        :param timeout: Duration in seconds after which the view will become inactive.
        """
        super().__init__(timeout=timeout)
        self.current_page = 0  # Index of the current page being displayed
        self.queue_pages = queue_pages  # All queue pages
        self.current_track = current_track  # Metadata of the currently playing track
        self.total_pages = len(queue_pages)  # Total number of pages available
        self.update_buttons()  # Set the initial state for navigation buttons

    def update_buttons(self):
        """
        Update the disabled state of pagination buttons based on the current page index.
        """
        self.previous_page.disabled = self.current_page == 0
        self.next_page.disabled = self.current_page >= self.total_pages - 1

    def get_embed(self) -> disnake.Embed:
        """
        Create and return the embed representing the current queue view.
        
        :return: A disnake.Embed object with the queue details.
        """
        return create_queue_embed(
            current_track=self.current_track,
            queue_page=self.queue_pages[self.current_page] if self.queue_pages else [],
            current_page=self.current_page,
            total_pages=self.total_pages
        )

    @disnake.ui.button(emoji="⬅️", style=disnake.ButtonStyle.blurple)
    async def previous_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """
        Button callback to move to the previous page of the queue.
        
        Updates the current page index, refreshes button states, and edits the message with the new embed.
        """
        self.current_page = max(0, self.current_page - 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @disnake.ui.button(emoji="➡️", style=disnake.ButtonStyle.blurple)
    async def next_page(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """
        Button callback to move to the next page of the queue.
        
        Updates the current page index, refreshes button states, and edits the message with the new embed.
        """
        self.current_page = min(self.total_pages - 1, self.current_page + 1)
        self.update_buttons()
        await interaction.response.edit_message(embed=self.get_embed(), view=self)

    @disnake.ui.button(emoji="🗑️", style=disnake.ButtonStyle.red)
    async def delete_message(self, button: disnake.ui.Button, interaction: disnake.Interaction):
        """
        Button callback to delete the queue message.
        
        This provides users with an option to remove the pagination message from the channel.
        """
        await interaction.message.delete()

class Queue(commands.Cog):
    """
    Cog that handles the queue command to display the current music queue.
    
    This cog retrieves the current track and queued tracks, paginates them, and sends an interactive
    embed with navigation buttons to the channel.
    """
    def __init__(self, bot):
        self.bot = bot  # Reference to the main bot instance

    @commands.command(aliases=["q"])
    @commands.has_any_role(1137297683862802503, 1335963261878665229, 1336673321223192659, 739241340189278279, 733923101506666547, 811070168163680286)
    async def queue(self, ctx):
        """
        Command to display the current music queue.
        
        Retrieves the currently playing track and the queue. It then paginates the queue into chunks
        (with a default page size of 10 items per page) and sends an interactive embed with pagination.
        
        :param ctx: Command context representing the invocation details.
        """
        try:
            current_track = get_current_track() or {}
            raw_queue = show_queue() or []
            
            # Prepare a list of dictionaries with track title and URL for display
            queue_list = [
                {
                    'title': track.get('title', 'Título desconhecido'),
                    'original_url': track.get('original_url', '')
                }
                for track in raw_queue
            ]
            
            # Define the number of items per page
            page_size = 10
            # Split the queue list into multiple pages
            queue_pages = [
                queue_list[i:i + page_size] 
                for i in range(0, len(queue_list), page_size)
            ] or [[]]
            
            # Create an instance of the QueueView with the paginated queue and current track info
            view = QueueView(queue_pages, current_track)
            # Send the initial embed message with the view attached for interactive pagination
            await ctx.send(embed=view.get_embed(), view=view)
        
        except Exception as e:
            # On error, send an error embed and auto-delete the message after 15 seconds
            await ctx.send(embed=create_error_embed(e), delete_after=15)

def setup(bot):
    """
    Register the Queue cog with the bot.
    
    This function adds the Queue cog to the bot's list of cogs, making its commands available.
    """
    bot.add_cog(Queue(bot))
