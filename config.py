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


class Cian(Settings):
    database: str
    echo: bool
    table_reg: str
    table_data: str


general_settings = Settings(_env_file="general.env")
dobrotsen_settings = Dobrotsen(_env_file=["general.env", "dobrotsen/dobrotsen.env"])
stomat_settings = Stomat(_env_file=["general.env", "stomatolog_msk_1/stom.env"])
cian_settings = Cian(_env_file=["general.env", "cian/cian.env"])
