# Import required modules
import os  # File system operations
from disnake.ext import commands, tasks  # Bot framework and background tasks

class AutoCleanup(commands.Cog):
    """Automatic file cleanup system for managing temporary files.
    
    Features:
    - Periodic file deletion (5-minute intervals)
    - Voice activity awareness
    - Safe file pattern matching
    - Error handling for file operations
    """
    
    def __init__(self, bot):
        """Initialize cog with bot reference and start cleanup task."""
        self.bot = bot
        self.cleanup_files.start()  # Start background task on cog load

    @tasks.loop(minutes=2)  # Runs every 2 minutes (adjust for needs)
    async def cleanup_files(self):
        """Main cleanup routine targeting 'youtube*' files in project root.
        
        Safety checks:
        - Skips cleanup during voice activity
        - Confirms file patterns before deletion
        - Handles file operation errors
        """
        
        # Skip cleanup if bot is in voice channel
        if self.bot.voice_clients:
            return

        # Use current working directory as project root
        project_root = os.getcwd()  # Consider using configurable path

        for filename in os.listdir(project_root):
            # Target files starting with 'youtube' (potential temp files)
            if filename.startswith("youtube") and not self.bot.voice_clients:
                file_path = os.path.join(project_root, filename)
                try:
                    os.remove(file_path)
                    print(f"removendo {file_path}")
                except Exception as e:
                    # Handle common errors: file in use, permissions
                    print(f"[Cleanup] Error removing {file_path}: {e}")

    @cleanup_files.before_loop
    async def before_cleanup(self):
        """Ensure bot is ready before starting cleanup tasks."""
        await self.bot.wait_until_ready()  # Prevent premature execution

def setup(bot):
    """Standard cog registration for disnake."""
    bot.add_cog(AutoCleanup(bot))  # Add cleanup system to bot