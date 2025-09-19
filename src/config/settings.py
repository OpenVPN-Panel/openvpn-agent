import sys
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

ROOT_PATH = Path(sys.path[1])


class Settings(BaseSettings):
    mgmt_address: str
    mgmt_port: int
    scripts_dir: str

    model_config = SettingsConfigDict(
        env_file=ROOT_PATH / ".env",
        env_file_encoding="utf-8",
        env_prefix="",
        env_nested_delimiter="_",
    )


settings = Settings()
