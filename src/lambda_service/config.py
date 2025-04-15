import os
from pathlib import Path

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Lambda Configuration
LAMBDA_ROLE_ARN = os.getenv('LAMBDA_ROLE_ARN')  # Required for Lambda function creation
DEFAULT_RUNTIME = 'python3.9'

FUNCTIONS_DIR = Path(os.getenv("LAMBDA_FUNCTIONS_DIR", "~/.lambda-functions")).expanduser()
FUNCTIONS_DIR.mkdir(parents=True, exist_ok=True)

# Runtime Configuration
DEFAULT_TIMEOUT = int(os.getenv("LAMBDA_TIMEOUT", "30"))  # seconds
DEFAULT_MEMORY_LIMIT = int(os.getenv("LAMBDA_MEMORY_LIMIT", "128"))  # MB 