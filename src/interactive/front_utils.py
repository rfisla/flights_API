import requests


def get_request(request):
    url = "http://127.0.0.1:8504/streamlit-request"
    response = requests.get(url, params=request)
    return response.json()


def get_results(params):
    url = "http://127.0.0.1:8504/api_call"
    response = requests.get(url, params=params)
    return response.json()
