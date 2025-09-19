from fastapi import APIRouter
from fastapi.params import Depends
from pydantic import BaseModel

from src.application.vpn.handlers import VPNHandlers
from src.infrastructure.di import get_vpn_handlers

vpn_agent_router = APIRouter(prefix="/vpn-agent", tags=["VPN Agent"])


class ClientRequest(BaseModel):
    name: str


@vpn_agent_router.get("/sessions")
async def get_vpn_sessions(handlers: VPNHandlers = Depends(get_vpn_handlers)):
    return await handlers.list_sessions(node_id=1)


@vpn_agent_router.post("/clients")
async def create_vpn_client(
    req: ClientRequest, handlers: VPNHandlers = Depends(get_vpn_handlers)
):
    return await handlers.provision_client(node_id=1, client_name=req.name)


@vpn_agent_router.delete("/clients/{name}")
async def delete_vpn_client(
    name: str, handlers: VPNHandlers = Depends(get_vpn_handlers)
):
    await handlers.revoke_client(node_id=1, client_name=name)
    return {"status": "revoked"}
