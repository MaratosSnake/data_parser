import os

from dotenv import load_dotenv
from requests import Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json
from datetime import datetime
from db import DataBase

load_dotenv()

API_KEY = os.getenv("API_KEY")


def format_symbols(symbols: list[str]) -> list[str]:
    return list(i.upper() for i in symbols)


def convert_date_to_timestamp(date: str) -> int:
    iso_timestamp = date
    dt = datetime.fromisoformat(iso_timestamp.replace('Z', '+00:00'))
    unix_timestamp_seconds = dt.timestamp()
    return int(unix_timestamp_seconds)


def send_request_to_api(url: str, params: dict[str] = None) -> dict[str]:
    if params is None:
        params = dict()
    headers = {
        'Accepts': 'application/json',
        'Accept-Encoding': 'deflate, gzip',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=params)
        data = json.loads(response.text)
        return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    finally:
        session.close()


def get_info_dict(symbols: list[str]) -> dict[str]:
    url = 'https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest'
    parameters = {
        'symbol': ','.join(symbols),
        'convert': 'USDT'
    }
    return send_request_to_api(url, parameters)


def get_fear_and_greed_index() -> dict | None:
    url = 'https://pro-api.coinmarketcap.com/v3/fear-and-greed/latest'
    data = send_request_to_api(url)
    if int(data['status']['error_code']) != 0:
        return None
    return {
        'timestamp': convert_date_to_timestamp(data['data']['update_time']),
        'fear_and_greed_index': data['data']['value']
    }


def add_data_to_data_frames(data: dict[str], symbols: list[str], **kwargs):
    timestamp = convert_date_to_timestamp(data['status']['timestamp'])
    status_code = int(data['status']['error_code'])
    if status_code != 0:
        return
    db = DataBase()

    for symbol in symbols:
        temp_data: dict[str] = data['data'][symbol.upper()][0]['quote']['USDT']
        temp_data.pop('tvl', None)
        temp_data.pop('last_updated', None)
        # cols_order = ['timestamp', *temp_data.keys()]
        temp_data['timestamp'] = timestamp

        db.insert_data(symbol, temp_data)

        # df = pd.DataFrame([temp_data], columns=cols_order)
        #
        # file_path = f'data/{symbol.lower()}.csv'
        # if os.path.exists(file_path):
        #     existed_df = pd.read_csv(file_path)
        #     result = pd.concat([existed_df, df], axis=0)
        #     result.to_csv(file_path, encoding='utf-8', index=False)
        # else:
        #     df.to_csv(file_path, encoding='utf-8', index=False)
    db.close_db()

