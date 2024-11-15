import requests

class DataManager:
    def __init__(self, token : str, url : str):
        self.token = token
        self.api_url = url
        self.prices_endpoint = '/prices'
        self.users_endpoint = '/users'
    
    
    def get_data(self):
        sheety_api_response = requests.get(url= self.api_url + self.prices_endpoint, headers= {'Authorization' : self.token})
        sheety_api_response.raise_for_status()
        return sheety_api_response.json()
        
    
    def get_cities(self):
        data = self.get_data()
        cities_list = [ row['city'] for row in data['prices']]
        self.id_list = [ row['id'] for row in data['prices']]
        return cities_list
    
    def get_prices_and_codes(self): 
        data = self.get_data()
        iata_list = [ row['iataCode'] for row in data['prices']]
        prices_list = [ row['lowestPrice'] for row in data['prices']]
        return prices_list, iata_list
    
    
    def get_customer_emails(self):
        sheety_users = requests.get(url= self.api_url + self.users_endpoint, headers= {'Authorization' : self.token})
        sheety_users.raise_for_status()
        users_data = sheety_users.json()
        emails_list = [row['whatIsYourEmailAddress ?'] for row in users_data['users']]
        return emails_list
             
    
    def fill_iata_codes(self, iata_codes : list):
        for i, code in enumerate(iata_codes):
            body = {
            "price": {
                "iataCode": code,
            },
            } 
        
            sheety_post_response = requests.put(url= f'{self.api_url}{self.prices_endpoint}/{self.id_list[i]}', headers= {'Authorization' : self.token}, json= body)
            sheety_post_response.raise_for_status()
            print(sheety_post_response.json())
  
            
        
    