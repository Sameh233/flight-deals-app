import requests
import json


class FlightSearch:
    def __init__(self, api_key : str, api_secret : str):
        self.api_key = api_key
        self.api_secret = api_secret
        with open('token.json', mode= 'r') as file:
            self.token = json.load(file)['token']
                 
        self.headers = {
            'Authorization' : self.token   
        }
      
    
    def get_city_codes(self, api_url : str, cities : list):
        iata_codes_list = []
        for city in cities:
            response = requests.get(url= api_url, headers= self.headers, params= {'keyword' : city, 'max' :  1} )
            response.raise_for_status()
            iata_code = response.json()['data'][0]['iataCode']
            iata_codes_list.append(iata_code)
        return iata_codes_list
    
    
    def get_flight_offers(self, flight_api, location_code, destination_code, departure_date,number_of_adults = 1):
        parameters = {
            'originLocationCode' : location_code, 
            'destinationLocationCode' :  destination_code,
            'departureDate' : departure_date,
            'adults' : number_of_adults,
            'currencyCode' : 'GBP',
            'max' : 4
            } 
        
        flight_api_response = requests.get(url= flight_api, headers= self.headers, params= parameters )
        flight_api_response.raise_for_status()
        return flight_api_response.json()
        
    
    def authenticate(self):
        auth_body = { 
        'grant_type': 'client_credentials',
        'client_id': self.api_key,
        'client_secret': self.api_secret
        }
    
        response = requests.post(url= 'https://test.api.amadeus.com/v1/security/oauth2/token', 
                        headers= {'Content-Type': 'application/x-www-form-urlencoded'}, 
                        data = auth_body )  
        response.raise_for_status()
        
        json_response = response.json()
        self.token = f'{json_response['token_type']} {json_response['access_token']}'
        
        with open('token.json', mode= 'w') as file:
            json.dump({'token' : self.token }, file)
        
        
        
    