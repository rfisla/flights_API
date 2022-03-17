import pathlib
import sys
import pandas as pd
import requests

sys.path.append(str(pathlib.Path().absolute()).split("/src")[0] + "/src")

import streamlit as st
from back.utils import Decoding, ReadDataFrames, gcp_request_get

st.set_page_config(page_title="Cheap flights search", layout="wide")
st.cache(suppress_st_warning=True)

st.markdown("# Flights search")
st.markdown("Found the cheapest option!")
im = "http://villa-groupcorp.com/sites/default/files/styles/full_size/public/flight-hero04c1.jpg?itok=hhscHSGZ"
st.image(im, width=400)

st.markdown("### Make your choice")
origin_input = st.text_input("Origin")
destination_input = st.text_input("Destination")

departure_date = st.text_input('Departure date')
return_date = st.text_input('Return date')

#departure_date = st.date_input('Departure date')
#return_date = st.date_input('Return date')

currency = st.selectbox('Choose a currency', ("EUR", "LIB"))

search_button = st.button(label="Search", help="Press to get your selected info")
if search_button:
    decoding = Decoding()
    cities_info = pd.read_csv('src/datasets/city_codes.csv', sep=",", usecols=[0, 2]).dropna().reset_index(drop=True)
    cities_info['City/Airport'] = cities_info['City/Airport'].str.upper()

    if decoding.get_city_code(origin_input, cities_info) != 'No results' and \
            decoding.get_city_code(destination_input, cities_info) != 'No results':

        filters_dict = {
            "origin": origin_input,
            "destination": destination_input,
            "return_date": return_date,
            "depart_date": departure_date,
            "currency": currency
        }
        api_data = gcp_request_get(filters_dict)
        st.markdown(api_data)

    else:
        st.markdown('No results for the places selected')

