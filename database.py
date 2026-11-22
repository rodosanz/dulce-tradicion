import psycopg2
import config


def conectar():
    return psycopg2.connect(
        host=config.host,
        database=config.database,
        user=config.user,
        password=config.password
    )