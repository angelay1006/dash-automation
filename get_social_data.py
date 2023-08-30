import requests
import json

# Getting our credentials
with open('my-config.json') as config_file:
    config = json.load(config_file)

# Don't forget to update this in config.json when required! 
temp_access_token = config['meta_api']['temp_access_token']
# meta #######################
client_id = config['meta_api']['client_id'] # app_id
client_secret = config['meta_api']['client_secret'] # app secret 


def get_long_lived_user_token(temp_token, client_id, client_secret):
    """
    Gets our long-lived user access token, valid for 60 days 
    Return: response format on success below
    {
        "access_token": "LONG-LIVED-USER-ACCESS-TOKEN",
        "token_type": "bearer",
        "expires_in": SECONDS-UNTIL-TOKEN-EXPIRES
    }
    """
    grant_type = 'fb_exchange_token'
    fb_exchange_token = temp_token

    params = (
        ('grant_type', grant_type),
        ('client_id', client_id),
        ('client_secret', client_secret),
        ('fb_exchange_token', fb_exchange_token),
    )

    return requests.get('https://graph.facebook.com/v17.0/oauth/access_token', params=params).json()


def get_fb_access_token():
    return temp_access_token
def get_ig_access_token():
    return temp_access_token


long_lived_user_token = get_long_lived_user_token(get_fb_access_token(), client_id, client_secret)
long_lived_user_token = {'access_token': f'{get_fb_access_token()}', 'token_type': 'bearer'}
long_lived_user_token = long_lived_user_token['access_token']


def get_page_access_token():
    """
    Using long-lived user access token (UAT) to get page access token (PAT)
    Since we use long-lived UAT, PAT has no expiration date
    """
    params = (
        ('access_token', long_lived_user_token),
    )

    try:
        page_req = requests.get(f'https://graph.facebook.com/v17.0/{app_scoped_user_id}/accounts', params=params).json()
    
        if 'error' not in page_req:
            page_access_token = page_req['data']
        else: 
            raise ValueError('Access token has expired, please replace it!')
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f'An error occurred while making the request: {e}')
    
    return page_access_token

# first we figure out what our app_scoped_user_id is: 
# https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived/ 
access_token = config['meta_api']['long_lived_user_access_token']
try:
    res = requests.get(f"https://graph.facebook.com/v17.0/me?access_token={access_token}").json()
    app_scoped_user_id = res['id']
except requests.exceptions.RequestException as e:
    raise RuntimeError(f'An error occurred while making the request: {e}')


def get_tokens():
    """
    generate and return long-lived user access token and page access token.
    """
    page_access_token = get_page_access_token()
    return long_lived_user_token, page_access_token



