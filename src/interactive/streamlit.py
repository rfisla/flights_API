import pathlib
import sys
import pandas as pd
from datetime import date

sys.path.append(str(pathlib.Path().absolute()).split("/src")[0] + "/src")

import streamlit as st
from back.utils import Decoding, ReadDataFrames, gcp_request_get


class DisplayInterface:
    st.set_page_config(page_title="Cheap flights search", layout="wide")
    st.cache(suppress_st_warning=True)

    st.markdown("# Flights search")
    st.markdown("Found the cheapest option!")
    im = "http://villa-groupcorp.com/sites/default/files/styles/full_size/public/flight-hero04c1.jpg?itok=hhscHSGZ"
    st.image(im, width=400)


class UserPlaceChoices:
    def __init__(self):
        st.markdown("### Make your choice")
        self.origin_input = st.text_input("Origin")
        self.destination_input = st.text_input("Destination")


class UserDateOptions:
    def __init__(self):
        options = st.selectbox('Select the kind of search', ("", "Choose a travel month", "Choose a specific date"))
        if options == "Choose a travel month":
            month_departure = st.selectbox('Select departure month', ('01', '02', '03', '04', '05', '06', '07',
                                                                      '08', '09', '10', '11', '12'))
            self.departure_date = '-'.join([str(date.today().year), month_departure])

            month_return = st.selectbox('Select return month', ('01', '02', '03', '04', '05', '06', '07',
                                                                '08', '09', '10', '11', '12'))
            self.return_date = '-'.join([str(date.today().year), month_return])
        elif options == "Choose a specific date":
            self.departure_date = st.date_input('Departure date').isoformat()
            self.return_date = st.date_input('Return date').isoformat()
        else:
            self.return_date=""
            self.departure_date=""


class UserCurrencyOptions:
    def __init__(self):
        self.choice = st.selectbox('Choose a currency', ("EUR", "LIB"))


class PersonalizedSearch:
    def __init__(self, origin_input, destination_input, departure_date, return_date, currency):
        search_button = st.button(label="Search", help="Press to get your selected info")
        if search_button:
            decoding = Decoding()
            cities_info = pd.read_csv('src/datasets/city_codes.csv', sep=",", usecols=[0, 2])\
                .dropna().reset_index(drop=True)
            cities_info['City/Airport'] = cities_info['City/Airport'].str.upper()

            if decoding.get_city_code(origin_input, cities_info) != 'No results' or \
                    decoding.get_city_code(destination_input, cities_info) != 'No results':

                filters_dict = {
                    "origin": origin_input,
                    "destination": destination_input,
                    "return_date": return_date,
                    "depart_date": departure_date,
                    "currency": currency
                    }
                try:
                    api_data = gcp_request_get(filters_dict)
                    results_table = pd.read_json(api_data)
                    st.write('### Results', results_table)
                except Exception:
                    st.write('No results for this search. Try again with another dates')
            else:
                st.write('Origin or destination not recognized. \n'
                         '- Write the city name in english')


if __name__ == "__main__":
    interface = DisplayInterface()
    places = UserPlaceChoices()
    dates = UserDateOptions()
    currency = UserCurrencyOptions()

    PersonalizedSearch(
                       places.origin_input,
                       places.destination_input,
                       dates.departure_date,
                       dates.return_date,
                       currency.choice
                       )
