import requests
import pandas as pd


url = "https://iata-and-icao-codes.p.rapidapi.com/airlines"

headers = {
    'x-rapidapi-host': "iata-and-icao-codes.p.rapidapi.com",
    'x-rapidapi-key': "af57958cf8msh7a41980e6313f7dp11972ajsn2f30f1957320"
    }

response = requests.request("GET", url, headers=headers)

airlines_info = pd.read_json(response.text).dropna().reset_index(drop=True).iloc[:, 0:2]
airlines_info.columns = ['IATA code', 'IATA airlines']
airlines_info.to_csv('src/iata_airlines_codes.csv', index = False)