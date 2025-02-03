import pytest
import disnake
from disnake.ext import commands
from disnake.ext.commands import Bot
from ping import Ping

@pytest.fixture
def bot():
    intents = disnake.Intents.all()
    bot = Bot(command_prefix='!', intents=intents)
    bot.add_cog(Ping(bot))
    return bot

@pytest.mark.asyncio
async def test_ping_command(bot, mocker):
    # Create a mock context
    ctx = mocker.Mock()
    ctx.message.delete = mocker.AsyncMock()
    ctx.send = mocker.AsyncMock(return_value=mocker.Mock(delete=mocker.AsyncMock()))

    # Mock latency
    bot.latency = 0.1234
    
    # Invoke the command
    await bot.get_command('ping').callback(ctx)
    
    # Assert message deleted
    ctx.message.delete.assert_called_once()
    
    # Assert ping response sent
    ctx.send.assert_called_once_with(f"O ping é {bot.latency * 1000:.2f}ms")
    
    # Assert response message deleted
    sent_message = await ctx.send()
    sent_message.delete.assert_called_once()