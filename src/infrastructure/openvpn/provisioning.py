import datetime
import subprocess

from src.application.interfaces.vpn import IVPNProvisioningService
from src.domain.vpn.entities import VPNClient


class ShellProvisioningService(IVPNProvisioningService):
    def __init__(self, base_dir: str):
        self.base_dir = base_dir

    async def provision(self, node_id: int, client_name: str) -> VPNClient:
        script = f"{self.base_dir}/addClient.sh"
        subprocess.run([script, client_name], check=True)
        return VPNClient(
            name=client_name,
            node_id=node_id,
            created_at=datetime.datetime.now(datetime.UTC),
        )

    async def revoke(self, node_id: int, client_name: str) -> None:
        script = f"{self.base_dir}/delClient.sh"
        subprocess.run([script, client_name], check=True)
