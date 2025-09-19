import datetime
import subprocess
from pathlib import Path

from src.application.interfaces.vpn import IVPNProvisioningService
from src.domain.vpn.entities import VPNClient
from src.infrastructure.exceptions import (
    ClientConfigFileNotFound,
    ClientConfigFileAlreadyExist,
)


class ShellProvisioningService(IVPNProvisioningService):
    def __init__(self, base_dir: str, client_config_dir: str):
        self.base_dir = base_dir
        self.client_config_dir = client_config_dir

    async def provision(self, node_id: int, client_name: str) -> VPNClient:
        script = f"{self.base_dir}/addClient.sh"
        try:
            subprocess.run(["bash", script, client_name], check=True)
        except subprocess.CalledProcessError as e:
            if e.returncode == 1:
                raise ClientConfigFileAlreadyExist(
                    f"Client {client_name} already exists"
                )
            raise

        return VPNClient(
            name=client_name,
            node_id=node_id,
            created_at=datetime.datetime.now(datetime.UTC),
        )

    async def revoke(self, node_id: int, client_name: str) -> None:
        script = f"{self.base_dir}/delClient.sh"
        subprocess.run(["bash", script, client_name], check=True)

    async def get_config(self, node_id: int, client_name: str) -> Path:
        file_path = Path(f"/root/openvpn/client-configs/files/{client_name}.ovpn")
        if not file_path.exists():
            raise ClientConfigFileNotFound(f"not found client config file: {file_path}")

        return file_path
