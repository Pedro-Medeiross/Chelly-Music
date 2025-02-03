import os
import pytest
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
    assert client.command_prefix == os.environ.get('prefix')
    assert isinstance(client, commands.AutoShardedBot)
    assert client.shard_count == 2
    assert client.help_command is None
