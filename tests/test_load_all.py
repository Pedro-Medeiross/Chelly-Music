import os
import unittest
from unittest.mock import patch, MagicMock

class TestLoadAll(unittest.TestCase):
    @patch("os.walk")
    @patch("disnake.ext.commands.AutoShardedBot.load_extension")
    def test_load_all(self, mock_load_extension, mock_os_walk):
        # Simulando estrutura de arquivos na pasta "modules"
        mock_os_walk.return_value = [
            ("./modules", ["subdir"], ["file1.py", "file2.py"]),
            ("./modules/subdir", [], ["file3.py"]),
        ]

        # Criando um bot mockado da própria classe AutoShardedBot
        from disnake.ext.commands import AutoShardedBot
        mock_bot = MagicMock(spec=AutoShardedBot)

        # Função que carrega extensões corretamente
        def recursive_load(directory, bot_instance):
            for root, _, files in os.walk(directory):
                for filename in files:
                    if filename.endswith('.py'):
                        module = os.path.relpath(os.path.join(root, filename), directory)
                        module = module.replace(os.sep, ".")[:-3]  # Remove .py no final
                        bot_instance.load_extension(f'modules.{module}')

        # Chamando a função com o mock_bot correto
        recursive_load('./modules', mock_bot)

        # Verifica se os arquivos certos foram carregados
        expected_calls = [
            "modules.file1",
            "modules.file2",
            "modules.subdir.file3",
        ]
        actual_calls = [call.args[0] for call in mock_bot.load_extension.call_args_list]

        self.assertListEqual(expected_calls, actual_calls)

if __name__ == "__main__":
    unittest.main()
