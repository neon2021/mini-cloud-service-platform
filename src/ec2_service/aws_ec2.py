import boto3
import logging
from typing import Optional, Dict, Any
from . import config

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSEC2Client:
    def __init__(self):
        try:
            self.ec2 = boto3.client(
                'ec2',
                aws_access_key_id=config.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=config.AWS_SECRET_ACCESS_KEY,
                region_name=config.AWS_REGION
            )
            logger.info("Successfully connected to AWS EC2")
        except Exception as e:
            logger.error(f"Failed to connect to AWS EC2: {str(e)}")
            raise

    def create_instance(self, params) -> Dict[str, Any]:
        try:
            response = self.ec2.run_instances(
                ImageId=params.ami_id,
                InstanceType=params.instance_type,
                MinCount=1,
                MaxCount=1,
                KeyName=params.key_name,
                SecurityGroupIds=params.security_group_ids,
                SubnetId=params.subnet_id,
                TagSpecifications=[{
                    'ResourceType': 'instance',
                    'Tags': [{'Key': 'Name', 'Value': params.name}]
                }]
            )
            instance_id = response['Instances'][0]['InstanceId']
            logger.info(f"Successfully created instance {instance_id}")
            return response
        except Exception as e:
            logger.error(f"Failed to create instance: {str(e)}")
            raise

    def get_instance(self, instance_id: str) -> Dict[str, Any]:
        try:
            response = self.ec2.describe_instances(InstanceIds=[instance_id])
            return response['Reservations'][0]['Instances'][0]
        except Exception as e:
            logger.error(f"Failed to get instance {instance_id}: {str(e)}")
            raise

    def delete_instance(self, instance_id: str) -> None:
        try:
            self.ec2.terminate_instances(InstanceIds=[instance_id])
            logger.info(f"Successfully deleted instance {instance_id}")
        except Exception as e:
            logger.error(f"Failed to delete instance {instance_id}: {str(e)}")
            raise

    def start_instance(self, instance_id: str) -> None:
        try:
            self.ec2.start_instances(InstanceIds=[instance_id])
            logger.info(f"Successfully started instance {instance_id}")
        except Exception as e:
            logger.error(f"Failed to start instance {instance_id}: {str(e)}")
            raise

    def stop_instance(self, instance_id: str) -> None:
        try:
            self.ec2.stop_instances(InstanceIds=[instance_id])
            logger.info(f"Successfully stopped instance {instance_id}")
        except Exception as e:
            logger.error(f"Failed to stop instance {instance_id}: {str(e)}")
            raise 