# Import required modules
import os  # Operating system interface for file/directory operations
import disnake  # Discord API wrapper for Python
from dotenv import load_dotenv  # Environment variables loader
from disnake.ext import commands  # Bot commands framework
from extra_modules.music.inactivity_handler import InactivityHandler # Class of Inactive Handle support for auto disconect if paused or not playing music
from utils import queue_manager # File of queue and queue utils

# Load environment variables from .env file (contains TOKEN_BOT and PREFIX_BOT)
load_dotenv()

# Configure bot intents (permissions to access specific Discord events/data)
intents = disnake.Intents.all()  # Enable all intents (use with caution in production)

# Initialize an AutoShardedBot instance with configuration
client = commands.AutoShardedBot(
    command_prefix=os.environ.get('PREFIX_BOT'),  # Get bot prefix from environment
    intents=intents,  # Apply configured intents
    shard_ids=[0, 1],  # Specific shard IDs to run (for large bot scaling)
    shard_count=2,  # Total number of shards across all instances
    help_command=None  # Disable default help command (custom implementation possible)
)

# Starts an unique stance of Handler
inactivity_handler = InactivityHandler(client, queue_manager)

def load_all():
    """Load all available cogs recursively from the Cogs directory"""
    
    def recursive_load(directory):
        """Recursively load Python files as bot extensions/cogs"""
        for root, _, files in os.walk(directory):
            for filename in files:
                # Process only Python files
                if filename.endswith('.py'):
                    # Convert file path to Python module notation
                    # os.path.relpath: Get relative path from starting directory
                    # replace(os.sep, '.'): Convert path separators to package dots
                    module = os.path.relpath(root, directory).replace(os.sep, '.')
                    
                    # Load the cog using disnake's extension system
                    # Format: Cogs.{subdirectory}.{filename}
                    # [:-3] removes the .py extension
                    client.load_extension(f'Cogs.{module}.{filename[:-3]}')
                    print(f'Module: {module} loaded from {filename}')

    # Start recursive loading from the Cogs directory
    recursive_load('./Cogs')

# Execute cog loader before starting the bot
load_all()

# Start the bot using the token from environment variables
# This is a blocking call - code execution stops here until bot shutdown
client.run(os.environ.get('TOKEN_BOT'))