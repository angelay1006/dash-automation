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


# oauth/access_token?grant_type=fb_exchange_token&client_id=1355495781848077&client_secret=e9f6fed43b1c63ebde246186196aa4f9&fb_exchange_token=EAATQ0PSSVA0BO2qo7hJ7YtP61Lkcaaaj1ySEBWvKULc0fDY2QEXNi3OjaYC0AjtIwn7OGiY2cuOQfHQxpc8eyf3ZAmCZA3s8FfYXlJgckG7ZAvnAx0DFZCdhIHTcObSZCllwpxb3XwWKdlwKqYCKRCuDWZC1KeFNyjrk6zbYoQ14VSZC3qHv10dl2EZC9FVhJOIMmdVZCe5ZAInLlCrqdIuNNluX6u
def get_long_lived_user_access_token():
    """
    Gets our long-lived user access token, valid for 60 days 
    Return: response format on success below
    {
        "access_token": "LONG-LIVED-USER-ACCESS-TOKEN",
        "token_type": "bearer",
        "expires_in": SECONDS-UNTIL-TOKEN-EXPIRES
    }
    """

    params = (
        ('grant_type', 'fb_exchange_token'),
        ('client_id', config["meta_api"]["client_id"]),
        ('client_secret', config["meta_api"]["client_secret"]),
        ('fb_exchange_token', config["meta_api"]["temp_access_token"]),
    )

    res = requests.get('https://graph.facebook.com/v17.0/oauth/access_token', params=params).json()
    long_lived_user_access_token = res['access_token']

    return long_lived_user_access_token



def get_fb_access_token():
    return temp_access_token
def get_ig_access_token():
    return temp_access_token


long_lived_user_token = get_long_lived_user_access_token()
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
# access_token = config['meta_api']['long_lived_user_access_token']
access_token = get_long_lived_user_access_token()


try:
    res = requests.get(f"https://graph.facebook.com/v17.0/me?access_token={access_token}").json()
except requests.exceptions.RequestException as e:
    raise RuntimeError(f'An error occurred while making the request: {e}')

app_scoped_user_id = res["id"]

def get_tokens():
    """
    generate and return long-lived user access token and page access token.
    """
    page_access_token = get_page_access_token()
    return long_lived_user_token, page_access_token



