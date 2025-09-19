from pathlib import Path
from typing import Protocol

from src.domain.vpn.entities import VPNClient, VPNSession


class IVPNProvisioningService(Protocol):
    async def provision(self, node_id: int, client_name: str) -> VPNClient: ...

    async def revoke(self, node_id: int, client_name: str) -> None: ...

    async def get_config(self, node_id: int, client_name: str) -> Path: ...


class IVPNMonitoringService(Protocol):
    async def list_sessions(self, node_id: int) -> list[VPNSession]: ...
