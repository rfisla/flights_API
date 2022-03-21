import requests
import pandas as pd


class ConfigParams:
    def __init__(self):
        self.url = "https://iata-and-icao-codes.p.rapidapi.com/airlines"
        self.headers = {
                        'x-rapidapi-host': "iata-and-icao-codes.p.rapidapi.com",
                        'x-rapidapi-key': "af57958cf8msh7a41980e6313f7dp11972ajsn2f30f1957320"
                        }


class Operations:
    def __init__(self, config):
        self.config = config

    def iata_codes_request(self):
        return requests.request("GET", self.config.url, headers=self.config.headers)

    @staticmethod
    def transform_raw_data(self, response_json)->pd.DataFrame:
        airlines_info = pd.read_json(response_json.text).dropna().reset_index(drop=True).iloc[:, 0:2]
        airlines_info.columns = ['IATA code', 'IATA airlines']
        return airlines_info

    @staticmethod
    def save_dataframe(self, airlines_dataset: pd.DataFrame):
        airlines_dataset.to_csv('src/datasets/iata_airlines_codes.csv', index=False)


if __name__ == "__main__":
    config_params = ConfigParams()
    get_data = Operations(config_params)
    response = get_data.iata_codes_request()
    airlines_df = get_data.transform_raw_data(response)
    get_data.save_dataframe(airlines_df)
