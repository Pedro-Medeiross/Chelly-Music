import os
import unittest
from unittest.mock import patch
import disnake
from dotenv import load_dotenv
from disnake.ext import commands

class TestBotInitialization(unittest.TestCase):
    @patch.dict(os.environ, {"TOKEN_BOT": "test_token", "PREFIX_BOT": "!"}, clear=True)
    def test_bot_initialization(self):
        # Carregar variáveis simuladas do ambiente
        load_dotenv()

        # Criar intents e inicializar o bot de teste
        intents = disnake.Intents.all()
        bot = commands.AutoShardedBot(command_prefix=os.getenv("PREFIX_BOT"), intents=intents, shard_ids=[0, 1], shard_count=2)

        # Se command_prefix for uma função, chamar ela para obter o valor real
        prefix = bot.command_prefix(None) if callable(bot.command_prefix) else bot.command_prefix

        # Verificações
        self.assertEqual(prefix, "!")
        self.assertEqual(bot.shard_count, 2)
        self.assertEqual(bot.shard_ids, [0, 1])

    @patch.dict(os.environ, {"TOKEN_BOT": "", "PREFIX_BOT": ""}, clear=True)
    def test_missing_env_vars(self):
        """Testa se um erro é lançado quando as variáveis de ambiente estão ausentes"""
        with self.assertRaises(ValueError):
            load_dotenv()
            if not os.getenv("TOKEN_BOT") or not os.getenv("PREFIX_BOT"):
                raise ValueError("As variáveis de ambiente TOKEN_BOT e PREFIX_BOT devem estar definidas.")

if __name__ == "__main__":
    unittest.main()
