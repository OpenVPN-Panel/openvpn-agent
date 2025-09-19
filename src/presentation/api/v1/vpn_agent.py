from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from pydantic import BaseModel
from starlette.responses import FileResponse

from src.application.vpn.handlers import VPNHandlers
from src.infrastructure.di import get_vpn_handlers
from src.infrastructure.exceptions import ClientConfigFileNotFound

vpn_agent_router = APIRouter(prefix="/vpn-agent", tags=["VPN Agent"])


class ClientRequest(BaseModel):
    name: str


@vpn_agent_router.get("/sessions")
async def get_vpn_sessions(handlers: VPNHandlers = Depends(get_vpn_handlers)):
    return await handlers.list_sessions(node_id=1)


@vpn_agent_router.get("/clients/{client_name}/config/download")
async def get_vpn_sessions(
        client_name: str,
        handlers: VPNHandlers = Depends(get_vpn_handlers)
):
    try:
        file_path: Path = await handlers.provisioning.get_config(1, client_name)
        return FileResponse(
            path=file_path,
            filename=f"{client_name}.ovpn",
            media_type="application/octet-stream"
        )
    except ClientConfigFileNotFound as e:
        return HTTPException(status_code=404, detail={e})


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
