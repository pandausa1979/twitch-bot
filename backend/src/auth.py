import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TwitchAuth:
    def __init__(self):
        self.client_id = os.getenv('CLIENT_ID')
        self.client_secret = os.getenv('CLIENT_SECRET')
        self.token = None
        
    def get_app_access_token(self):
        """Get an app access token using client credentials flow"""
        url = 'https://id.twitch.tv/oauth2/token'
        params = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'grant_type': 'client_credentials'
        }
        
        response = requests.post(url, params=params)
        if response.status_code == 200:
            data = response.json()
            self.token = data['access_token']
            return self.token
        else:
            raise Exception(f"Failed to get access token: {response.text}")
            
    def validate_token(self):
        """Validate the current access token"""
        if not self.token:
            return False
            
        url = 'https://id.twitch.tv/oauth2/validate'
        headers = {
            'Authorization': f'OAuth {self.token}'
        }
        
        response = requests.get(url, headers=headers)
        return response.status_code == 200
        
    def get_token(self):
        """Get a valid access token, refreshing if necessary"""
        if not self.token or not self.validate_token():
            return self.get_app_access_token()
        return self.token 