import requests
from dotenv import load_dotenv
import os
from datetime import datetime
from datetime import timedelta
from flight_search import FlightSearch
from data_manager import DataManager
from flight_data import FlightData
from notification_manager import NotificationManager

load_dotenv("credentials.env")

api_key = os.getenv("api_key")
api_secret = os.getenv("api_secret")
sheety_token = os.getenv("sheety_token")
sheety_api_url = os.getenv("sheety_api_url")
amadeus_ciy_api = os.getenv("amadeus_ciy_api")
flight_api = os.getenv("flight_offers_api")

account_sid = os.getenv("account_sid")
auth_token = os.getenv("auth_token")
sender_num = os.getenv("sender_num")
receiver_num = os.getenv("receiver_num")

sender_email = os.getenv("sender_email")
app_password = os.getenv("app_password")


ORIGIN_CITY_IATA = "LON"

data_manager = DataManager(sheety_token, sheety_api_url)
flight_search = FlightSearch(api_key, api_secret)
flight_data = FlightData()
notification_app = NotificationManager(
    account_sid, auth_token, sender_email, app_password
)

departure_date = datetime.now().date() + timedelta(days=1)


def main():
    global departure_date
    emails_list = data_manager.get_customer_emails()
    lowest_prices, country_codes = data_manager.get_prices_and_codes()
    for count in range(6):
        for i, lowest_price in enumerate(lowest_prices):
            flight_offers = flight_search.get_flight_offers(
                flight_api, ORIGIN_CITY_IATA, country_codes[i], departure_date
            )
            best_offer = flight_data.compare_prices(float(lowest_price), flight_offers)
            if best_offer is not None:
                for user_email in emails_list:
                    message_satus = notification_app.send_emails(
                        user_email, flight_data.stops, best_offer
                    )
                    # message_satus = notification_app.send_sms(sender_num,receiver_num, best_offer)
                    print(message_satus)
                    return

        departure_date += timedelta(days=30)
    if country_codes[0] is None:
        # get city names from google sheet and fill iata_codes
        cities = data_manager.get_cities()
        iata_codes = flight_search.get_city_codes(amadeus_ciy_api, cities)
        data_manager.fill_iata_codes(iata_codes)


try:
    main()
except requests.exceptions.HTTPError:
    flight_search.authenticate()
    main()
