# Import required modules
import os  # Operating system interface
import sys  # Provides access to Python runtime environment
import disnake  # Discord API wrapper for Python
from dotenv import load_dotenv  # Loads environment variables from a .env file
from disnake.ext import commands  # Bot command framework

# Ensure the root directory is in sys.path (for imports in tests or Docker)
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Load environment variables from the .env file
load_dotenv()

# Configure bot intents (permissions to access Discord data)
intents = disnake.Intents.all()  # Use all intents (be careful with privileged ones)

# Initialize the bot (AutoSharded for scaling if needed)
client = commands.AutoShardedBot(
    command_prefix=os.getenv('PREFIX_BOT'),  # Command prefix from environment
    intents=intents,
    shard_ids=[0, 1],  # Example shard IDs (adjust or remove for testing)
    shard_count=2,     # Total number of shards
    help_command=None  # Disable the default help command
)

def load_all():
    """
    Load all cogs (bot extensions) from the Cogs directory recursively.
    """
    base_dir = os.path.abspath("Cogs")  # Absolute path to Cogs directory

    for root, _, files in os.walk(base_dir):
        for filename in files:
            if filename.endswith(".py") and not filename.startswith("__"):
                full_path = os.path.join(root, filename)

                # Convert file path to Python module path
                rel_path = os.path.relpath(full_path, os.path.dirname(base_dir))
                module_path = rel_path.replace(os.sep, ".")[:-3]  # Strip ".py"

                try:
                    client.load_extension(module_path)
                    print(f"✅ Loaded extension: {module_path}")
                except Exception as e:
                    print(f"❌ Failed to load extension {module_path}: {e}")

# Load all cogs before starting the bot
load_all()

def start_bot():
    """
    Starts the bot. This is separated so tests can import `load_all()` without running the bot.
    """
    token = os.getenv('TOKEN_BOT')
    if not token:
        raise RuntimeError("TOKEN_BOT environment variable not set.")
    client.run(token)

# Only run the bot if this script is executed directly
if __name__ == "__main__":
    start_bot()
