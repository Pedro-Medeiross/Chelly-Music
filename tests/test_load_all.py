# Import required modules
import os  # Operating system interface for file/directory operations
import disnake  # Discord API wrapper for Python
from dotenv import load_dotenv  # Environment variables loader
from disnake.ext import commands  # Bot commands framework

# Load environment variables from .env file (contains TOKEN_BOT and PREFIX_BOT)
load_dotenv()  # Requires python-dotenv package

# Configure bot intents (permissions to access specific Discord events/data)
intents = disnake.Intents.all()  # Enable all intents (warning: security consideration)

# Initialize an AutoShardedBot instance with configuration
client = commands.AutoShardedBot(
    command_prefix=os.environ.get('PREFIX_BOT'),  # Get bot prefix from environment variables
    intents=intents,  # Apply configured permissions
    shard_ids=[0, 1],  # Specific shard IDs for horizontal scaling
    shard_count=2,  # Total shards in cluster (should match Discord's recommendation)
    help_command=None  # Disable default help command
)

def load_all():
    """Load all available cogs recursively from the Cogs directory"""
    
    def recursive_load(directory):
        """Recursively discover and load Python files as bot extensions"""
        # os.walk generates directory tree (root, dirs, files)
        for root, _, files in os.walk(directory):
            for filename in files:
                # Filter Python files only
                if filename.endswith('.py'):
                    # Convert filesystem path to Python module path
                    # 1. Get relative path from base directory
                    relative_path = os.path.relpath(root, directory)
                    # 2. Replace OS separators with Python dot notation
                    python_path = relative_path.replace(os.sep, '.')
                    # 3. Remove .py extension and build full module path
                    full_module = f'Cogs.{python_path}.{filename[:-3]}'
                    
                    # Load extension using disnake's system
                    client.load_extension(full_module)  # Equivalent to importlib

    # Start recursive loading from Cogs directory
    recursive_load('./Cogs')  # Path relative to execution location

# Initialize cog loading process
load_all()  # Must be called before bot starts

# Start bot connection to Discord
# Warning: This is a blocking call - code after this won't execute
client.run(os.environ.get('TOKEN_BOT'))  # Get secret token from environment