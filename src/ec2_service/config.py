import os
from pathlib import Path

# Lima Configuration
LIMA_HOME = Path.home() / ".lima"
INSTANCES_DIR = LIMA_HOME / "instances"

# Default instance configuration
DEFAULT_IMAGE_URL = os.getenv('DEFAULT_IMAGE_URL', 'https://cloud-images.ubuntu.com/releases/22.04/release/ubuntu-22.04-server-cloudimg-amd64.img')
DEFAULT_CPU = int(os.getenv('DEFAULT_CPU', '2'))
DEFAULT_MEMORY = int(os.getenv('DEFAULT_MEMORY', '4'))  # GiB
DEFAULT_DISK = int(os.getenv('DEFAULT_DISK', '20'))  # GiB

# AWS Configuration
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')

# Default instance configuration
DEFAULT_INSTANCE_TYPE = os.getenv('DEFAULT_INSTANCE_TYPE', 't2.micro')
DEFAULT_AMI_ID = os.getenv('DEFAULT_AMI_ID', 'ami-0c55b159cbfafe1f0')  # Amazon Linux 2
DEFAULT_KEY_NAME = os.getenv('DEFAULT_KEY_NAME')
DEFAULT_SECURITY_GROUP_IDS = os.getenv('DEFAULT_SECURITY_GROUP_IDS', '').split(',')
DEFAULT_SUBNET_ID = os.getenv('DEFAULT_SUBNET_ID') 