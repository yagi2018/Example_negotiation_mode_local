# AgentConnect: https://github.com/agent-network-protocol/AgentConnect
# Author: GaoWei Chang
# Email: chgaowei@gmail.com
# Website: https://agent-network-protocol.com/
#
# This project is open-sourced under the MIT License. For details, please see the LICENSE file.

# Configuration file for tests
import os
from pathlib import Path
from dotenv import load_dotenv

# Get the project root directory (assuming tests folder is directly under root)
#ROOT_DIR = Path(__file__).parent.parent.parent
ROOT_DIR = Path(__file__).parent

# Load environment variables from root .env file
load_dotenv(ROOT_DIR / '.env')

# Azure OpenAI configurations
# AZURE_OPENAI_API_KEY = os.getenv('AZURE_OPENAI_API_KEY')
# AZURE_OPENAI_ENDPOINT = os.getenv('AZURE_OPENAI_ENDPOINT')
# AZURE_OPENAI_DEPLOYMENT = os.getenv('AZURE_OPENAI_DEPLOYMENT')
# AZURE_OPENAI_MODEL_NAME = os.getenv('AZURE_OPENAI_MODEL_NAME')

# OpenRouter - DeepSeek API configurations
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = os.getenv('OPENROUTER_BASE_URL')
OPENROUTER_MODEL_NAME = os.getenv('OPENROUTER_MODEL_NAME')

def validate_config():
    """Validate that all required environment variables are set"""
    required_vars = [
        # 'AZURE_OPENAI_API_KEY',
        # 'AZURE_OPENAI_ENDPOINT',
        # 'AZURE_OPENAI_DEPLOYMENT',
        # 'AZURE_OPENAI_MODEL_NAME'
        'OPENROUTER_API_KEY',
        'OPENROUTER_BASE_URL',
        'OPENROUTER_MODEL_NAME'
    ]
    
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}") 