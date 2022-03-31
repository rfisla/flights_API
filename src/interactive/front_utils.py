import requests


def get_request(request):
    url = "https://api-cheapflights.herokuapp.com/streamlit-request"
    response = requests.get(url, params=request)
    return response.json()


def get_results(params):
    url = "https://api-cheapflights.herokuapp.com/api_call"
    response = requests.get(url, params=params)
    return response.json()
