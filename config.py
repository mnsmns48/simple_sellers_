from pydantic import SecretStr
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    driver_name: str
    username: str
    password: SecretStr
    host: str
    port: int
    echo: bool
    database: str


class Dobrotsen(Settings):
    database: str
    url: str
    city_id: int


general_settings = Settings(_env_file="general.env")
dobrotsen_settings = Dobrotsen(_env_file=["general.env", "dobrotsen/dobrotsen.env"])
