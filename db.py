import psycopg2
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()


class DataBase:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port="5432",
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            sslmode="require"
        )
        self.cursor = self.conn.cursor()

    def create_table(self, name: str):
        if not name.isalnum():
            raise ValueError("Имя таблицы должно содержать только буквы, цифры и подчеркивания.")

        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS "{name}" (
    id SERIAL PRIMARY KEY,
    timestamp NUMERIC NOT NULL,
    price NUMERIC NOT NULL,
    volume_24h NUMERIC,
    volume_change_24h NUMERIC,
    percent_change_1h NUMERIC,
    percent_change_24h NUMERIC,
    percent_change_7d NUMERIC,
    percent_change_30d NUMERIC,
    percent_change_60d NUMERIC,
    percent_change_90d NUMERIC,
    market_cap NUMERIC,
    market_cap_dominance NUMERIC,
    fully_diluted_market_cap NUMERIC
);
        """
        self.cursor.execute(create_table_query)
        self.conn.commit()

    def insert_data(self, table_name: str, data: dict):
        # Проверка имени таблицы
        if not table_name.isalnum():
            raise ValueError("Имя таблицы должно содержать только буквы, цифры и подчеркивания.")

        self.create_table(table_name)

        # Формирование списка столбцов и значений
        columns = ', '.join(data.keys())
        values = ', '.join(['%s'] * len(data))

        # SQL-запрос для вставки данных
        insert_query = f"""
        INSERT INTO "{table_name}" ({columns})
        VALUES ({values});
        """

        # Выполнение запроса с передачей данных
        self.cursor.execute(insert_query, list(data.values()))
        self.conn.commit()

    def drop_table_if_exists(self, table_name: str):
        # Проверка имени таблицы
        if not table_name.isalnum():
            raise ValueError("Имя таблицы должно содержать только буквы, цифры и подчеркивания.")

        # SQL-запрос для удаления таблицы, если она существует
        drop_query = f"""
        DROP TABLE IF EXISTS "{table_name}";
        """

        # Выполнение запроса
        self.cursor.execute(drop_query)
        self.conn.commit()

    def close_db(self):
        self.cursor.close()
        self.conn.close()


