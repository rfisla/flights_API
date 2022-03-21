import pandas as pd
import requests
from src.back.utils import SetAPIParams, Decoding, ReadDataFrames
from src.back.api_response_operations import ExtractInfo, CreateResultsDataframe
from flask import Flask, jsonify, request
import os

"""
querystring= {
              "destination":"-",
              "origin":"Madrid",
              "return_date":"2022-04",
              "depart_date":"2022-04",
              "currency":"EUR"
              }
config = SetAPIParams(querystring)
datasets_charger = ReadDataFrames()
cities = datasets_charger.city_info
# airlines = datasets_charger.airlines_info

decoding = Decoding()
config.info['querystring']['destination'] = decoding.get_city_code(config.destination, cities)
config.info['querystring']['origin'] = decoding.get_city_code(config.origin, cities)
"""
class APIRequest:
    def __init__(self, config):
        query = requests.request("GET", config.info['url'], headers=config.info['headers'],
                                   params=config.info['querystring'])
        self.response = query.json()
        try:
            self.destinations = list(self.response['data'])
        except TypeError as e:
            raise e('Error in the API CALL')

"""
class JsonToDataframe:

    def __init__(self, apicall, config_info):
        self.destination = config_info.info['querystring']['destination']

        results = pd.DataFrame()
        results['Price'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['price'],
                                         apicall.results_len))
        results['Airline'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['airline'],
                                           apicall.results_len))
        results['Departure'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['departure_at'],
                                             apicall.results_len))
        results['Return'] = pd.Series(map(lambda i: apicall.response['data'][self.destination][i]['return_at'],
                                          apicall.results_len))
        results['Origin'] = config_info.origin
        results['Destination'] = config_info.destination
        self.results = results

"""

app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/streamlit-request", methods=["GET"])
def get_params():
    query = request.args.to_dict()
    config = SetAPIParams(query)

    datasets_charger = ReadDataFrames()
    cities = datasets_charger.city_info
    #airlines = datasets_charger.airlines_info

    decoding = Decoding()

    if config.info['querystring']['destination'] != '-':
        config.info['querystring']['destination'] = decoding.get_city_code(config.destination, cities)
    config.info['querystring']['origin'] = decoding.get_city_code(config.origin, cities)

    apicall = APIRequest(config)
    extract_info_from_json = ExtractInfo(apicall.response, apicall.destinations)
    df = CreateResultsDataframe(extract_info_from_json.destination_list,
                                extract_info_from_json.prices_list,
                                extract_info_from_json.airlines_list,
                                extract_info_from_json.departures_list,
                                extract_info_from_json.returns_list)
    #df = JsonToDataframe(apicall, config)

    if df.results.empty is False:
        """
        try:
            df.results['Airline'] = list(map(lambda row: decoding.get_airline_name(row, airlines),
                                             df.results['Airline']))
        except IndexError:
            pass
        """
        results = df.results.to_json()
        return jsonify(results)
    else:
        return jsonify({'Error': 'Not results founded for the selected dates '})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8504)))

