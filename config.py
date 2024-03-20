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


class Stomat(Settings):
    database: str
    tablename: str


general_settings = Settings(_env_file="general.env")
dobrotsen_settings = Dobrotsen(_env_file=["general.env", "dobrotsen/dobrotsen.env"])
stomat_settings = Stomat(_env_file=["general.env", "stomatolog_msk_1/stom.env"])
