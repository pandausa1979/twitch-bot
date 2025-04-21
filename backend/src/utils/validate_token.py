import os
import requests
from dotenv import load_dotenv

def validate_token(token):
    """Validate a Twitch TMI token"""
    # Remove 'oauth:' prefix if present
    clean_token = token.replace('oauth:', '')
    
    url = 'https://id.twitch.tv/oauth2/validate'
    headers = {
        'Authorization': f'OAuth {clean_token}'
    }
    
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            print("Token is valid!")
            print(f"Client ID: {data.get('client_id')}")
            print(f"Login: {data.get('login')}")
            print(f"Scopes: {', '.join(data.get('scopes', []))}")
            print(f"User ID: {data.get('user_id')}")
            print(f"Expires In: {data.get('expires_in')} seconds")
            return True
        else:
            print(f"Token validation failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Error validating token: {str(e)}")
        return False

if __name__ == "__main__":
    load_dotenv()
    token = os.getenv('TWITCH_TMI_TOKEN')
    if not token:
        print("No token found in environment variables")
        exit(1)
    
    print(f"Validating token: {token[:10]}...")
    validate_token(token) 