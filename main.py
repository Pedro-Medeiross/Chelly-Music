import os
import disnake
from dotenv import load_dotenv
from disnake.ext import commands

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Define todos os intents necessários
intents = disnake.Intents.all()

# Cria uma instância do AutoShardedBot com os prefixos e intents definidos
client = commands.AutoShardedBot(command_prefix=os.environ.get('prefix'), intents=intents, shard_ids=[0, 1],
                                 shard_count=2, help_command=None)

def load_all():
    # Função recursiva para percorrer todas as subpastas
    def recursive_load(directory):
        for root, _, files in os.walk(directory):
            for filename in files:
                if filename.endswith('.py'):
                    module = os.path.relpath(root, directory).replace(os.sep, '.')
                    client.load_extension(f'modules.{module}.{filename[:-3]}')

    # Chama a função recursiva a partir do diretório 'modulos'
    recursive_load('./modules')

# Carrega todas as extensões
load_all()

# Inicia o bot com o token definido nas variáveis de ambiente
client.run(os.environ.get('token'))