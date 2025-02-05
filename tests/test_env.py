import os
import unittest
from unittest.mock import patch
from dotenv import load_dotenv

class TestEnvLoading(unittest.TestCase):
    @patch.dict(os.environ, {"TOKEN_BOT": "fake_token", "PREFIX_BOT": "!"}, clear=True)
    def test_env_variables_loaded(self):
        load_dotenv()
        self.assertEqual(os.environ.get("TOKEN_BOT"), "fake_token")
        self.assertEqual(os.environ.get("PREFIX_BOT"), "!")

if __name__ == "__main__":
    unittest.main()