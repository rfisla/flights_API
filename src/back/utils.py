import yaml
import pandas as pd
import requests


class NotFoundError(Exception):
    pass


class SetAPIParams:
    def __init__(self, query):
        try:
            with open('../back/config.yml', 'r') as configfile:
                self.info = yaml.safe_load(configfile)
            self.info["destination"] = query['destination']
            self.info["origin"] = query["origin"]
            self.info["return_date"] = query["return_date"]
            self.info["depart_date"] = query["depart_date"]
            self.info["currency"] = query["currency"]
        except FileNotFoundError:
            self.info = 'File not found'


class ReadDataFrames:
    def __init__(self):
        try:
            airlines_info = pd.read_csv('../datasets/iata_airlines_codes.csv', sep=",")
            city_info = pd.read_csv('../datasets/city_codes.csv', sep=",", usecols=[0, 1, 2])\
                .dropna().reset_index(drop=True)
            city_info['City/Airport'] = list(
                map(lambda city, country: ', '.join([city, country]), city_info['City/Airport'], city_info['Country']))
            city_info.drop(['Country'], axis=1, inplace=True)
            city_info['City/Airport'] = city_info['City/Airport'].str.upper()

            self.airlines_info = airlines_info
            self.city_info = city_info

        except FileNotFoundError:
            raise FileNotFoundError


class Decoding:
    @staticmethod
    def get_city_code(city_name: str, cities_info: pd.DataFrame) -> str:
        finder = list(filter(lambda search: True if search.find(city_name.upper()) == 0 else False,
                             cities_info['City/Airport']))
        if len(finder) != 0:
            city_code_match = cities_info[cities_info['City/Airport'] == finder[0]]['IATA code'].values[0]
            return city_code_match
        else:
            return 'No results'

    @staticmethod
    def get_city_name(city_code: str, cities_info: pd.DataFrame) -> str:
        finder = list(filter(lambda search: True if search.find(city_code) == 0 else False,
                             cities_info['IATA code']))
        if len(finder) != 0:
            city_code_match = cities_info[cities_info['IATA code'] == finder[0]]['City/Airport'].values[0]
            return city_code_match
        else:
            return city_code

    @staticmethod
    def get_airline_name(airline_code: str, airlines_info: pd.DataFrame) -> str:
        try:
            airline_name_match = airlines_info[airlines_info['IATA code'] == airline_code]['IATA airlines'].values[0]
            return airline_name_match
        except IndexError:
            return airline_code




