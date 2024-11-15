class FlightData:
    def __init__(self):
        self.stops = 0

    
    def compare_prices(self, lowest_price, flight_offers):
        for data in flight_offers['data']:
            price = float(data['price']['total'])
            departure_airport_IATA_code = data['itineraries'][0]['segments'][0]['departure']['iataCode']
            departure_time = data['itineraries'][0]['segments'][0]['departure']['at']
            
            arrival_airport_IATA_code = data['itineraries'][0]['segments'][-1]['arrival']['iataCode']
            arrival_time = data['itineraries'][0]['segments'][-1]['arrival']['at']
            self.stops = len(data['itineraries'][0]['segments'])
            if price < lowest_price :
                return price, departure_airport_IATA_code, departure_time,arrival_airport_IATA_code,arrival_time
            

            
