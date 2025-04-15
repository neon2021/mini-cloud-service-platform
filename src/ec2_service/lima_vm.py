import subprocess
import json
import logging
import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LimaVMClient:
    def __init__(self):
        self.lima_home = Path.home() / ".lima"
        self.lima_home.mkdir(parents=True, exist_ok=True)
        self.instances_dir = self.lima_home / "instances"
        self.instances_dir.mkdir(parents=True, exist_ok=True)
        logger.info("Lima VM client initialized")

    def create_instance(self, params) -> Dict[str, Any]:
        try:
            instance_name = params.name
            instance_dir = self.instances_dir / instance_name
            instance_dir.mkdir(parents=True, exist_ok=True)

            # 创建 Lima 配置文件
            lima_config = {
                "images": [
                    {
                        "location": params.image_url,
                        "arch": "x86_64"
                    }
                ],
                "cpus": params.cpu,
                "memory": f"{params.memory}GiB",
                "disk": f"{params.disk}GiB",
                "mounts": [
                    {
                        "location": "~",
                        "writable": True
                    }
                ],
                "ssh": {
                    "localPort": 0,
                    "loadDotSSHPubKeys": True
                },
                "networks": [
                    {
                        "lima": "shared"
                    }
                ]
            }

            config_path = instance_dir / "lima.yaml"
            with open(config_path, "w") as f:
                yaml.dump(lima_config, f)

            # 启动 Lima 实例
            subprocess.run(["limactl", "start", instance_name], check=True)
            logger.info(f"Successfully created instance {instance_name}")
            
            # 获取实例信息
            return self.get_instance(instance_name)
        except Exception as e:
            logger.error(f"Failed to create instance: {str(e)}")
            raise

    def get_instance(self, instance_name: str) -> Dict[str, Any]:
        try:
            result = subprocess.run(
                ["limactl", "list", "--json"],
                capture_output=True,
                text=True,
                check=True
            )
            instances = json.loads(result.stdout)
            
            for instance in instances:
                if instance["name"] == instance_name:
                    return {
                        "name": instance["name"],
                        "status": instance["status"],
                        "cpu": instance["cpus"],
                        "memory": instance["memory"],
                        "disk": instance["disk"],
                        "ssh_port": instance["sshLocalPort"]
                    }
            
            raise Exception(f"Instance {instance_name} not found")
        except Exception as e:
            logger.error(f"Failed to get instance {instance_name}: {str(e)}")
            raise

    def delete_instance(self, instance_name: str) -> None:
        try:
            subprocess.run(["limactl", "delete", instance_name], check=True)
            logger.info(f"Successfully deleted instance {instance_name}")
        except Exception as e:
            logger.error(f"Failed to delete instance {instance_name}: {str(e)}")
            raise

    def start_instance(self, instance_name: str) -> None:
        try:
            subprocess.run(["limactl", "start", instance_name], check=True)
            logger.info(f"Successfully started instance {instance_name}")
        except Exception as e:
            logger.error(f"Failed to start instance {instance_name}: {str(e)}")
            raise

    def stop_instance(self, instance_name: str) -> None:
        try:
            subprocess.run(["limactl", "stop", instance_name], check=True)
            logger.info(f"Successfully stopped instance {instance_name}")
        except Exception as e:
            logger.error(f"Failed to stop instance {instance_name}: {str(e)}")
            raise 