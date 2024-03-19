from dataclasses import dataclass
from environs import Env


@dataclass
class Hidden:
    db_username: str
    db_password: str
    db_local_port: int
    db_name: str
    db_table: str


def load_hidden_vars(path: str):
    env = Env()
    env.read_env()

    return Hidden(
        db_username=env.str("DB_USERNAME"),
        db_password=env.str("DB_PASSWORD"),
        db_local_port=env.int("DB_LOCAL_PORT"),
        db_name=env.str("DB_NAME"),
        db_table=env.str("DB_TABLE")
    )


hidden_s = load_hidden_vars(path='.env')
