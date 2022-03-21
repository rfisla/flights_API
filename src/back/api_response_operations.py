from src.back.utils import  Decoding, ReadDataFrames
from abc import ABC
import pandas as pd


class JsonOperations(ABC):
    def __init__(self):
        self.decoding = Decoding()
        self.datasets = ReadDataFrames()
        self.prices_list = []
        self.destination_list = []
        self.airlines_list = []
        self.departures_list = []
        self.returns_list = []
        self.results = pd.DataFrame()


class ExtractInfo(JsonOperations):
    def __init__(self, response: dict, destinations: list):
        JsonOperations.__init__(self)
        self.response = response
        self.destinations = destinations
        for code in self.destinations:
            try:
                self.prices_list.append(response['data'][code]['0']['price'])
                self.destination_list.append(self.decoding.get_city_name(code, self.datasets.city_info))
                self.airlines_list.append(response['data'][code]['0']['airline'])
                self.departures_list.append(response['data'][code]['0']['departure_at'])
                self.returns_list.append(response['data'][code]['0']['return_at'])
            except KeyError:
                pass
            try:
                self.prices_list.append(response['data'][code]['1']['price'])
                self.destination_list.append(self.decoding.get_city_name(code, self.datasets.city_info))
                self.airlines_list.append(response['data'][code]['1']['airline'])
                self.departures_list.append(response['data'][code]['1']['departure_at'])
                self.returns_list.append(response['data'][code]['1']['return_at'])
            except KeyError:
                pass
            try:
                self.prices_list.append(response['data'][code]['2']['price'])
                self.destination_list.append(self.decoding.get_city_name(code, self.datasets.city_info))
                self.airlines_list.append(response['data'][code]['2']['airline'])
                self.departures_list.append(response['data'][code]['2']['departure_at'])
                self.returns_list.append(response['data'][code]['2']['return_at'])
            except KeyError:
                pass
            try:
                self.prices_list.append(response['data'][code]['3']['price'])
                self.destination_list.append(self.decoding.get_city_name(code, self.datasets.city_info))
                self.airlines_list.append(response['data'][code]['3']['airline'])
                self.departures_list.append(response['data'][code]['3']['departure_at'])
                self.returns_list.append(response['data'][code]['3']['return_at'])
            except KeyError:
                pass


class CreateResultsDataframe(JsonOperations):
    def __init__(self, destination_list: list,
                 prices_list: list,
                 airlines_list: list,
                 departures_list: list,
                 returns_list: list):

        JsonOperations.__init__(self)
        self.results['destination'] = destination_list
        self.results['prices'] = prices_list
        self.results['Airline'] = list(
            map(lambda airline_code: self.decoding.get_airline_name(airline_code, self.datasets.airlines_info),
                airlines_list))
        self.results['Departure'] = departures_list
        self.results['Return'] = returns_list



