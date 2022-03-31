import pathlib
import sys
import pandas as pd
from datetime import date
import streamlit as st

sys.path.append(str(pathlib.Path().absolute()).split("/src")[0] + "/src")

from back.utils import Decoding, ReadDataFrames
from interactive.front_utils import get_request, get_results


class DisplayInterface:
    st.set_page_config(page_title="Cheap flights search", layout="wide")
    st.cache(suppress_st_warning=True)

    st.markdown("# Flights search")
    st.markdown("#### Find the cheapest option!")
    im = "http://villa-groupcorp.com/sites/default/files/styles/full_size/public/flight-hero04c1.jpg?itok=hhscHSGZ"
    st.image(im, width=400)


class UserPlaceChoices:
    def __init__(self):
        st.markdown("### Make your choice")
        self.origin_input = st.text_input("Origin")
        self.destination_input = st.text_input("Destination "
                                               "(Write  '-'  if you want to check all possible destinations)")


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
            self.return_date = ""
            self.departure_date = ""


class UserCurrencyOptions:
    def __init__(self):
        self.choice = st.selectbox('Choose a currency', ("EUR", "LIB"))


class PersonalizedSearch:
    def __init__(self, origin_input, destination_input, departure_date, return_date, currency):
        search_button = st.button(label="Search", help="Press to get your selected info")
        if search_button:
            decoding = Decoding()
            cities_info = pd.read_csv('src/datasets/city_codes.csv', sep=",", usecols=[0, 1, 2])\
                .dropna().reset_index(drop=True)
            cities_info['City/Airport'] = list(
                map(lambda city, country: ', '.join([city, country]), cities_info['City/Airport'], cities_info['Country']))
            cities_info.drop(['Country'], axis=1, inplace=True)
            cities_info['City/Airport'] = cities_info['City/Airport'].str.upper()

            if decoding.get_city_code(origin_input, cities_info) != 'No results':

                filters_dict = {
                    "origin": origin_input,
                    "destination": destination_input,
                    "return_date": return_date,
                    "depart_date": departure_date,
                    "currency": currency
                    }
                #try:
                request = get_request(filters_dict)
                api_data = get_results(request)
                results_table = pd.read_json(api_data)
                st.markdown('###' f' Destinations from {origin_input}')
                st.write(results_table)
                #except Exception:
                    #st.write('No results for this search. Try again with another dates')
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
