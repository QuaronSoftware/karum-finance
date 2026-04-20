from pydantic import Field, validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

class Wallets(BaseModel):
    # ByBit
    bybit_secret: str
    bybit_api_key: str
    bybit_base_url: str

    # OKX
    okx_secret: str
    okx_api_key: str
    okx_passphrase: str
    okx_base_url: str

    # Monobank
    mono_api_key: str
    mono_base_url: str

    # Price provider
    price_provider_api_key: str
    price_provider_base_url: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_nested_delimiter="__",
        case_sensitive=False,
        extra="ignore",
    )

    wallets: Wallets = Field()
    main_currency: str = Field('USD', description="Main currency")
    service_name: str = Field(default="detalon-backend")
    log_level: str = Field(default="INFO", pattern=r"^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$")
    category_path: str = Field(default='categories.json')

    database_url: str = Field(..., description="PostgreSQL connection string")
    bot_token: str = Field(..., description="Telegram bot token")
    admin_id: int = Field(..., description="Telegram admin user ID")
    # jwt_secret: str = Field(...)

    @validator("database_url", "bot_token", pre=True)
    def validate_not_empty(cls, v):
        if not v:
            raise ValueError("Cannot be empty")
        return v


def load_settings() -> AppSettings:
    return AppSettings()  # type: ignore