from dataclasses import dataclass
from datetime import datetime
from typing import NewType

VPNNodeID = NewType("VPNNodeID", int)


@dataclass
class VPNNode:
    id: VPNNodeID | None
    name: str  # Название / alias
    host: str  # IP или FQDN
    port: int = 1194  # mgmt порт или api порт
    created_at: datetime | None = None


@dataclass
class VPNClient:
    name: str
    node_id: int
    created_at: datetime
    revoked: bool = False


@dataclass
class VPNSession:
    client_name: str
    real_ip: str
    virtual_ip: str
    bytes_recv: int
    bytes_sent: int
    connected_since: datetime
    cipher: str
