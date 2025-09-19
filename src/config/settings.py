import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(sys.path[1])


class Settings(BaseSettings):
    mgmt_address: str = "127.0.0.1"
    mgmt_port: int = 55555
    scripts_dir: str = "/root/openvpn/scripts"

    # model_config = SettingsConfigDict(
    #     env_file=ROOT_PATH / ".env",
    #     env_file_encoding="utf-8",
    #     env_prefix="",
    #     env_nested_delimiter="_",
    # )


settings = Settings()