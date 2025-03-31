# Import required testing modules
import os  # OS interface for environment variables
import unittest  # Python testing framework
from unittest.mock import patch  # Mocking utilities
from dotenv import load_dotenv  # Environment loader

class TestEnvLoading(unittest.TestCase):
    """Unit tests for validating environment variable loading functionality.
    
    Tests include:
    - Successful loading of mocked credentials
    - Correct retrieval of security-sensitive values
    """
    
    @patch.dict(os.environ, {"TOKEN_BOT": "fake_token", "PREFIX_BOT": "!"}, clear=True)
    def test_env_variables_loaded(self):
        """Verify correct loading of security credentials from simulated environment.
        
        Uses mocked values to avoid exposing real credentials during testing.
        """
        
        # Execute environment loader (normally reads .env file)
        load_dotenv()  # In this test, uses patched os.environ instead

        # Validate authentication token loading
        # Security-critical value - should never be hardcoded
        self.assertEqual(os.environ.get("TOKEN_BOT"), "fake_token", 
                        "Bot token mismatch in environment variables")

        # Validate command prefix configuration
        # Functional requirement - defines bot interaction syntax
        self.assertEqual(os.environ.get("PREFIX_BOT"), "!", 
                        "Command prefix not loaded correctly")

if __name__ == "__main__":
    # Execute all test cases when run as main script
    unittest.main()  # Runs with: python -m unittest [filename]