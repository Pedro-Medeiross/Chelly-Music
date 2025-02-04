import sys
import os

# Adiciona o diretório raiz do projeto ao sys.path para garantir que o Python o encontre
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import os
from disnake.ext import commands
from main import client, load_all

def test_load_all(mocker):
    # Mocking os.walk to prevent actual file system operations
    mocker.patch('os.walk', return_value=[
        ('modules', [], ['test_module.py'])
    ])
    # Mocking client.load_extension to avoid actual loading
    mocker.patch.object(client, 'load_extension')
    
    load_all()
    client.load_extension.assert_called_with('modules..test_module')

def test_bot_initialization():
    assert client.command_prefix == os.environ.get('PREFIX_BOT')
    assert isinstance(client, commands.AutoShardedBot)
    assert client.shard_count == 2
    assert client.help_command is None
