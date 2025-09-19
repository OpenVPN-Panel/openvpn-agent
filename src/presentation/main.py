from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from src.presentation.api.v1.vpn_agent import vpn_agent_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(title="OpenVPN Agent", lifespan=lifespan)
app.include_router(vpn_agent_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8001)
