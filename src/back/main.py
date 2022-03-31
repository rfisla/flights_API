import requests
from src.back.utils import SetAPIParams, Decoding, ReadDataFrames
from src.back.api_response_operations import ExtractInfo, CreateResultsDataframe
from flask import Flask, jsonify, request
import os


class APIRequest:
    def __init__(self, config):
        headers = {'x-rapidapi-host': config['x-rapidapi-host'],
                   'x-rapidapi-key': config['x-rapidapi-key'],
                   'X-Access-Token': config['X-Access-Token']}
        params = {'destination': config['destination'], "origin": config["origin"], "return_date":
            config["return_date"], "depart_date": config["depart_date"], "currency": config["currency"]}
        query = requests.request("GET", config['url'], headers=headers,
                                 params=params)
        self.response = query.json()


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"


@app.route("/streamlit-request", methods=["GET"])
def get_query_params():
    query = request.args.to_dict()
    config = SetAPIParams(query)

    datasets_charger = ReadDataFrames()
    cities = datasets_charger.city_info

    decoding = Decoding()

    if config.info['destination'] != '-':
        config.info['destination'] = decoding.get_city_code(config.info['destination'], cities)
    config.info['origin'] = decoding.get_city_code(config.info['origin'], cities)

    return jsonify(config.info)


@app.route("/api_call", methods=["GET"])
def get_results():
    config = request.args

    apicall = APIRequest(config)
    try:
        list(apicall.response['data'])
    except TypeError as e:
        raise e('Error in the API CALL')
    extract_info_from_json = ExtractInfo(apicall.response, apicall.response['data'])
    df = CreateResultsDataframe(extract_info_from_json.destination_list,
                                extract_info_from_json.prices_list,
                                extract_info_from_json.airlines_list,
                                extract_info_from_json.departures_list,
                                extract_info_from_json.returns_list)

    if df.results.empty is False:
        results = df.results.to_json()
        return jsonify(results)
    else:
        return jsonify({'Error': 'Not results founded for the selected dates '})


if __name__ == "__main__":
    app.run()
