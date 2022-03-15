import pandas as pd
import requests
from config.config import ReadConfigFile, Decoding, ReadDataFrames, NotFoundError


class APIRequest:
    def __init__(self):
        request = requests.request("GET", config.info['url'], headers=config.info['headers'],
                                   params=config.info['querystring'])
        self.response = request.json()
        try:
            self.results_len = list(self.response['data'][config.info['querystring']['destination']])
        except TypeError as e:
            raise e('Error in the API CALL')


class JsonToDataframe:

    def __init__(self, json_info, config_info):
        self.json_info = json_info
        self.config_info = config_info
        self.destination = config_info.info['querystring']['destination']

        results = pd.DataFrame()
        results['price'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['price'],
                                         apicall.results_len))
        results['airline'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['airline'],
                                           apicall.results_len))
        results['departure'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['departure_at'],
                                             apicall.results_len))
        results['return'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['return_at'],
                                          apicall.results_len))
        results['Origin'] = config_info.origin
        results['Destination'] = config_info.destination
        self.results = results


if __name__ == "__main__":
    config = ReadConfigFile()

    datasets_charger = ReadDataFrames()
    cities = datasets_charger.city_info
    airlines = datasets_charger.airlines_info

    decoding = Decoding()
    config.info['querystring']['destination'] = decoding.get_city_code(config.destination, cities)
    config.info['querystring']['origin'] = decoding.get_city_code(config.origin, cities)

    apicall = APIRequest()


    df = JsonToDataframe(apicall.response, config)
    if df.results.empty is False:
        df.results['airline'] = list(map(lambda row: decoding.get_airline_name(row, airlines), df.results['airline']))
        df.results.to_csv('src/apicall_df.csv', index=False)
    else:
        print('Not results founded for the selected dates ')


