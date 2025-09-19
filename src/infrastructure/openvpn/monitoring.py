import asyncio
from datetime import datetime

from src.application.interfaces.vpn import IVPNMonitoringService
from src.domain.vpn.entities import VPNSession


class TelnetMonitoringService(IVPNMonitoringService):
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 55555,
    ):
        self.host = host
        self.port = port

    async def list_sessions(self, node_id: int) -> list[VPNSession]:
        reader, writer = await asyncio.open_connection(self.host, self.port)

        line = await reader.readline()
        print("GREETING:", line.decode().strip())

        writer.write(b"status 3\n")
        await writer.drain()

        sessions: list[VPNSession] = []

        while True:
            line = await reader.readline()
            if not line:
                break

            decoded = line.decode().strip()

            if decoded.startswith("CLIENT_LIST"):
                parts = decoded.split("\t")
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

            elif decoded == "END":  # правильный стоп
                break

        writer.write(b"exit\n")
        await writer.drain()

        writer.close()
        await writer.wait_closed()

        return sessions
