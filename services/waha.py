import requests
import os
from decouple import config

os.environ["WAHA_API_KEY"] = config("WAHA_API_KEY")

class Waha: 
    def __init__(self): 
        self.__api_url = "http://waha:3000"

    def get_history_messages(self, chatId, limit):
        try:
            url = f"{self.__api_url}/api/default/chats/{chatId}/messages?=limit={limit}&downloadMedia=false" 
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": os.environ["WAHA_API_KEY"]
            }

            response = requests.get(url, headers=headers)
            return response.json()

        except Exception as e:
            print("Error getting history messages:", e)
            return []
    
    def send_message(self, chatId, message): 
        try: 
            url = f"{self.__api_url}/api/sendText"
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": os.environ["WAHA_API_KEY"]
            }
            payload = {
                'session': 'default',
                'chatId': chatId,
                'text': message
            }
        
            requests.post(url, json=payload, headers=headers)

        except Exception as e:
            print("Error sending message:", e)

