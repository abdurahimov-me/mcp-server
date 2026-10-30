from pathlib import Path
from typing import Literal

from pydantic import Field, SecretStr, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


ENV_FILE = Path(__file__).resolve().parents[2] / ".env"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        env_ignore_empty=True,
        extra="ignore",
        frozen=True,
    )

    host: str = Field(default="127.0.0.1", validation_alias="MCP_HOST")
    port: int = Field(default=8000, ge=1, le=65535, validation_alias="MCP_PORT")
    auth_mode: Literal["none", "jwt"] = Field(default="none", validation_alias="MCP_AUTH_MODE")
    jwt_secret_key: SecretStr | None = Field(default=None, validation_alias="JWT_SECRET_KEY")
    jwt_issuer: str | None = Field(default=None, validation_alias="MCP_JWT_ISSUER")
    jwt_audience: str | None = Field(default=None, validation_alias="MCP_JWT_AUDIENCE")

    @field_validator("auth_mode", mode="before")
    @classmethod
    def normalize_auth_mode(cls, value: str) -> str:
        return value.lower()

    @model_validator(mode="after")
    def require_jwt_secret(self) -> "Settings":
        if self.auth_mode == "jwt" and self.jwt_secret_key is None:
            raise ValueError("JWT_SECRET_KEY is required when MCP_AUTH_MODE=jwt")
        return self


SETTINGS = Settings()
