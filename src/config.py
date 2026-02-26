"""
Configuration settings for AI Research Co-Pilot
"""

import os
from dotenv import load_dotenv

load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_API_BASE = os.getenv("OPENAI_API_BASE")

# Model Options
MODEL_OPTIONS = {
    "Llama 3.3 70B (Fast & Balanced)": "meta-llama/Llama-3.3-70B-Instruct",
    "DeepSeek V3 (Best Reasoning)": "deepseek-ai/DeepSeek-V3-0324",
    "Qwen3 235B (Ultra Large)": "Qwen/Qwen3-235B-A22B-Instruct-2507"
}

# Default Settings
DEFAULT_MODEL = "meta-llama/Llama-3.3-70B-Instruct"
DEFAULT_TEMPERATURE = 0.7
DEFAULT_MAX_TOKENS = 2000
MAX_SEARCH_RESULTS = 5

# Search Keywords for Web Search Trigger
SEARCH_KEYWORDS = [
    'latest', 'current', 'now', 'today', 'recent', 'news',
    '2025', '2026', 'this year', 'update'
]

# File Upload Settings
SUPPORTED_FILE_TYPES = ['pdf', 'docx', 'txt']
MAX_FILE_SIZE_MB = 10