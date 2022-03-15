import yaml
import pandas as pd


class NotFoundError(Exception):
    pass


class ReadConfigFile:
    def __init__(self):
        try:
            with open('config/config.yml', 'r') as configfile:
                self.info = yaml.safe_load(configfile)
            self.origin = self.info['querystring']['origin']
            self.destination = self.info['querystring']['destination']
        except FileNotFoundError:
            self.info = 'File not found'


class ReadDataFrames:
    def __init__(self):
        try:
            airlines_info = pd.read_csv('src/iata_airlines_codes.csv', sep=",")
            # airlines_info['IATA code'] = pd.Series(map(lambda select: select[6:].strip(), airlines_info['IATA code']))

            city_info = pd.read_csv('src/city_codes.csv', sep=",", usecols=[0, 2]).dropna().reset_index(drop=True)
            city_info['City/Airport'] = city_info['City/Airport'].str.upper()

            self.airlines_info = airlines_info
            self.city_info = city_info

        except FileNotFoundError:
            raise FileNotFoundError


class Decoding:
    def get_city_code(self, city_name: str, cities_info: pd.DataFrame) -> str:

        try:
            finder = list(filter(lambda search: True if search.find(city_name.upper()) == 0 else False,
                             cities_info['City/Airport']))
            city_code_match = cities_info[cities_info['City/Airport'] == finder[0]]['IATA code'].values[0]
            return city_code_match
        except IndexError:
            return NotFoundError

    def get_airline_name(self, airline_code: str, airlines_info: pd.DataFrame) -> str:
        airline_name_match = airlines_info[airlines_info['IATA code'] == airline_code]['IATA airlines'].values[0]
        return airline_name_match



