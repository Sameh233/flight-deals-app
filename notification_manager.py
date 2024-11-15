from twilio.rest import Client
import smtplib

class NotificationManager:
    def __init__(self,account_sid, auth_token, sender_email, app_password):
        self.sid = account_sid
        self.token = auth_token
        self.sender_email = sender_email
        self.app_password = app_password
        
    
    def send_sms(self, sender, receiver, offer: list):
        client = Client(self.sid, self.token)
        message = client.messages.create(
            body= f"Low price alert! Only £{offer[0]} to fly from {offer[1]} at {offer[2]} to {offer[3]}, and arrive at {offer[4]}",
            from_= sender,
            to= receiver,
        )
        return message.status


    def send_emails(self, user_email, number_of_stops, offer: list):
        with smtplib.SMTP("smtp.gmail.com") as  connection :
            connection.starttls()
            connection.login(user= self.sender_email, password= self.app_password)
            if number_of_stops > 1 :
                connection.sendmail(from_addr= self.sender_email, to_addrs= user_email, 
                                msg= f"Subject: good deal!\n\nLow price alert! Only £{offer[0]} to fly from {offer[1]} to {offer[3]}, with {number_of_stops} stop(s) departing on {offer[2]} and arriving at {offer[4]}".encode('utf-8'))
            else: 
                connection.sendmail(from_addr= self.sender_email, to_addrs= user_email, 
                                msg= f"Subject: good deal!\n\nLow price alert! Only £{offer[0]} to fly from {offer[1]} to {offer[3]}, departing on {offer[2]} and arriving at {offer[4]}".encode('utf-8'))
            return "Email successfully sent!"
                
            
