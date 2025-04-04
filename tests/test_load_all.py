# Import required modules
import os  # Operating system interface for file/directory operations
import sys  # Provides access to Python runtime environment
import disnake  # Discord API wrapper for Python
from dotenv import load_dotenv  # Loads environment variables from a .env file
from disnake.ext import commands  # Bot command framework

# Ensure the root directory is added to sys.path (for module imports in tests or Docker)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from .env file (e.g., TOKEN_BOT, PREFIX_BOT)
load_dotenv()

# Configure bot intents (permissions to access specific Discord events and data)
intents = disnake.Intents.all()  # Enable all intents (use with caution)

# Initialize an AutoShardedBot instance for scalable bot operation
client = commands.AutoShardedBot(
    command_prefix=os.getenv('PREFIX_BOT'),  # Command prefix from environment
    intents=intents,  # Permissions
    shard_ids=[0, 1],  # Specific shard IDs
    shard_count=2,  # Total shard count
    help_command=None  # Disable default help command
)

def load_all():
    """Load all cogs (extensions) from the Cogs directory recursively."""

    # Get absolute path to the 'Cogs' directory
    base_dir = os.path.abspath("Cogs")

    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("__"):
                # Build full path to the .py file
                full_path = os.path.join(root, filename)

                # Create a module path relative to the project root
                rel_path = os.path.relpath(full_path, os.path.dirname(base_dir))

                # Convert to Python module path (dot notation) and strip ".py"
                module_path = rel_path.replace(os.sep, ".")[:-3]

                try:
                    # Load the extension using disnake
                    client.load_extension(module_path)
                    print(f"✅ Loaded extension: {module_path}")
                except Exception as e:
                    print(f"❌ Failed to load extension {module_path}: {e}")

# Load all bot extensions before starting the bot
load_all()

# Run the bot using the secret token from environment variables
client.run(os.getenv('TOKEN_BOT'))
