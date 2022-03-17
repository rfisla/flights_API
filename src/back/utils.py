import yaml
import pandas as pd
import requests


class NotFoundError(Exception):
    pass


class SetAPIParams:
    def __init__(self, query):
        try:
            with open('../interactive/config.yml', 'r') as configfile:
                self.info = yaml.safe_load(configfile)
            self.query = query
            self.info['querystring'] = self.query
            self.origin = self.query['origin']
            self.destination = self.query['destination']
        except FileNotFoundError:
            self.info = 'File not found'


class ReadDataFrames:
    def __init__(self):
        try:
            airlines_info = pd.read_csv('../datasets/iata_airlines_codes.csv', sep=",")
            # airlines_info['IATA code'] = pd.Series(map(lambda select: select[6:].strip(), airlines_info['IATA code']))

            city_info = pd.read_csv('../datasets/city_codes.csv', sep=",", usecols=[0, 2]).dropna().reset_index(drop=True)
            city_info['City/Airport'] = city_info['City/Airport'].str.upper()

            self.airlines_info = airlines_info
            self.city_info = city_info

        except FileNotFoundError:
            raise FileNotFoundError

class Decoding:
    def get_city_code(self, city_name: str, cities_info: pd.DataFrame) -> str:
        finder = list(filter(lambda search: True if search.find(city_name.upper()) == 0 else False,
                             cities_info['City/Airport']))
        if len(finder) != 0:
            city_code_match = cities_info[cities_info['City/Airport'] == finder[0]]['IATA code'].values[0]
            return city_code_match
        else:
            return 'No results'


    def get_airline_name(self, airline_code: str, airlines_info: pd.DataFrame) -> str:
        airline_name_match = airlines_info[airlines_info['IATA code'] == airline_code]['IATA airlines'].values[0]
        return airline_name_match

def gcp_request_get(query):
    url = "http://127.0.0.1:8504/streamlit-request"
    response = requests.get(url, params=query)
    return response.json()