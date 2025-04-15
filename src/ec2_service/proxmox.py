from proxmoxer import ProxmoxAPI
from . import config
import urllib3
import logging
from typing import Optional, Dict, Any

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 禁用 SSL 警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class ProxmoxClient:
    def __init__(self):
        try:
            # 确保主机地址格式正确
            host = config.PROXMOX_HOST
            if not host.startswith('https://') and not host.startswith('http://'):
                host = f'https://{host}'
            if ':8006' not in host:
                host = f'{host}:8006'
            
            self.proxmox = ProxmoxAPI(
                host,
                user=config.PROXMOX_USER,
                password=config.PROXMOX_PASSWORD,
                verify_ssl=False,  # 禁用 SSL 验证
                timeout=30  # 增加超时时间
            )
            self.node = self.proxmox.nodes('pve')
            logger.info("Successfully connected to Proxmox server")
        except Exception as e:
            logger.error(f"Failed to connect to Proxmox server: {str(e)}")
            raise

    def create_instance(self, params) -> Dict[str, Any]:
        try:
            vmid = self._get_next_vmid()
            result = self.node.qemu.post(
                newid=vmid,
                name=params.name,
                clone=params.template_id,
                cores=params.cpu,
                memory=params.memory,
                full=1,
                net0='virtio,bridge=vmbr0',  # 添加网络配置
                scsi0='local-lvm:32',  # 添加存储配置
                agent=1  # 启用 QEMU Guest Agent
            )
            logger.info(f"Successfully created instance with vmid {vmid}")
            return result
        except Exception as e:
            logger.error(f"Failed to create instance: {str(e)}")
            raise

    def get_instance(self, vmid: int) -> Dict[str, Any]:
        try:
            return self.node.qemu(vmid).status.current.get()
        except Exception as e:
            logger.error(f"Failed to get instance {vmid}: {str(e)}")
            raise

    def delete_instance(self, vmid: int) -> None:
        try:
            self.node.qemu(vmid).delete()
            logger.info(f"Successfully deleted instance {vmid}")
        except Exception as e:
            logger.error(f"Failed to delete instance {vmid}: {str(e)}")
            raise

    def start_instance(self, vmid: int) -> None:
        try:
            self.node.qemu(vmid).status.start.post()
            logger.info(f"Successfully started instance {vmid}")
        except Exception as e:
            logger.error(f"Failed to start instance {vmid}: {str(e)}")
            raise

    def stop_instance(self, vmid: int) -> None:
        try:
            self.node.qemu(vmid).status.stop.post()
            logger.info(f"Successfully stopped instance {vmid}")
        except Exception as e:
            logger.error(f"Failed to stop instance {vmid}: {str(e)}")
            raise

    def _get_next_vmid(self) -> int:
        vmid = 100
        while True:
            try:
                self.node.qemu(vmid).status.current.get()
                vmid += 1
            except:
                return vmid 