from src.application.interfaces.vpn import (
    IVPNProvisioningService,
    IVPNMonitoringService,
)
from src.domain.vpn.entities import VPNClient, VPNSession


class VPNHandlers:
    def __init__(
        self,
        provisioning: IVPNProvisioningService,
        monitoring: IVPNMonitoringService,
    ):
        self.provisioning = provisioning
        self.monitoring = monitoring

    async def provision_client(self, node_id: str, client_name: str) -> VPNClient:
        return await self.provisioning.provision(node_id, client_name)

    async def revoke_client(self, node_id: int, client_name: str) -> None:
        await self.provisioning.revoke(node_id, client_name)

    async def list_sessions(self, node_id: int) -> list[VPNSession]:
        return await self.monitoring.list_sessions(node_id)
