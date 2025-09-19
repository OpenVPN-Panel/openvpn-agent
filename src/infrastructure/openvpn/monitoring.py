import asyncio
from datetime import datetime

from src.application.interfaces.vpn import IVPNMonitoringService
from src.domain.vpn.entities import VPNSession


class TelnetMonitoringService(IVPNMonitoringService):
    def __init__(
        self,
        host: str = "55.55.55.55",
        port: int = 555,
    ):
        self.host = host
        self.port = port

    async def list_sessions(self, node_id: int) -> list[VPNSession]:
        reader, writer = await asyncio.open_connection(self.host, self.port)
        writer.write(b"status 3\n")
        await writer.drain()

        sessions: list[VPNSession] = []

        async for line in reader:
            line = line.decode().strip()
            if line.startswith("CLIENT_LIST"):
                parts = line.strip().split("\t")
                print(parts)
                (
                    _,
                    name,
                    real_ip,
                    virt_ip,
                    virt_ipv6,
                    bytes_recv,
                    bytes_sent,
                    conn_since,
                    _,
                    username,
                    client_id,
                    peer_id,
                    cipher,
                ) = parts

                sessions.append(
                    VPNSession(
                        client_name=name,
                        real_ip=real_ip,
                        virtual_ip=virt_ip,
                        bytes_recv=bytes_recv,
                        bytes_sent=bytes_sent,
                        connected_since=datetime.strptime(
                            conn_since, "%Y-%m-%d %H:%M:%S"
                        ),
                        cipher=cipher,
                    )
                )
            elif line.startswith("ROUTING_TABLE"):
                break

        writer.write(b"exit\n")
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        return sessions
