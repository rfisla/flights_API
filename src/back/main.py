import pandas as pd
import requests
from src.back.utils import SetAPIParams, Decoding, ReadDataFrames, NotFoundError
from flask import Flask, jsonify, request
import os


class APIRequest:
    def __init__(self, config):
        request = requests.request("GET", config.info['url'], headers=config.info['headers'],
                                   params=config.info['querystring'])
        self.response = request.json()
        try:
            self.results_len = list(self.response['data'][config.info['querystring']['destination']])
        except TypeError as e:
            raise e('Error in the API CALL')

class JsonToDataframe:

    def __init__(self, apicall, config_info):
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


app = Flask(__name__)


@app.route("/", methods=["GET"])
def hello():
    return "Hello World"
#{'currency': 'EUR', 'depart_date': '2022-03-17', 'destination': 'barcelona', 'origin': 'MADRID', 'return_date': '2022-03-17'}
#query = {'currency': 'EUR', 'depart_date': '2022-04', 'destination': 'barcelona', 'origin': 'MADRID', 'return_date': '2022-04'}

@app.route("/streamlit-request", methods=["GET"])
def get_params():
    query = request.args.to_dict()
    config = SetAPIParams(query)

    datasets_charger = ReadDataFrames()
    cities = datasets_charger.city_info
    airlines = datasets_charger.airlines_info

    decoding = Decoding()
    config.info['querystring']['destination'] = decoding.get_city_code(config.destination, cities)
    config.info['querystring']['origin'] = decoding.get_city_code(config.origin, cities)
    #return jsonify({'results': config.info})
    apicall = APIRequest(config)


    df = JsonToDataframe(apicall, config)
    if df.results.empty is False:
        df.results['airline'] = list(map(lambda row: decoding.get_airline_name(row, airlines), df.results['airline']))
        results = df.results.to_json()
        return jsonify(results)
        #df.results.to_csv('src/apicall_df.csv', index=False)
    else:
        return jsonify({'Error': 'Not results founded for the selected dates '})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=int(os.environ.get("PORT", 8504)))

