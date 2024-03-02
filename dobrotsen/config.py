import os
from dataclasses import dataclass

from environs import Env


@dataclass
class Hidden:
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    url: str
    city_id: str


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()

    return Hidden(
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        url=env.str("URL"),
        city_id=env.str("CITY_ID"),
    )


hidden = load_hidden_vars(path='.env')
