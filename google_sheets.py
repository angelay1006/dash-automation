import gspread
from google.oauth2.service_account import Credentials
from facebook import Facebook
from instagram import Instagram
import get_social_data
import json


# Getting our credentials
with open('my-config.json') as config_file:
    config = json.load(config_file)

json_keyfile_path = config['google_api']['json_keyfile_path']
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
credentials = Credentials.from_service_account_file(json_keyfile_path, scopes=scope)
client = gspread.authorize(credentials)
spreadsheet_name = config['google_api']['spreadsheet_name']
spreadsheet = client.open(spreadsheet_name)
sheet_name = config['google_api']['sheet_name']


token_tuple = get_social_data.get_tokens()
user_token = token_tuple[0]
page_token = token_tuple[1][0]['access_token']
access_token = config['meta_api']['temp_access_token']
fb_page_id = config['meta_api']['facebook_page_id']

# You can get the spreadsheet ID from the URL, it's a long string of letters and numbers after '/d/' and before '/edit'
# the below is for `dash automation test` file!
content_sheet_id = config['google_api']['sheet_id']

# content_values = content_sheet.get_all_values()

def get_body(data):
    # no need to extract column headers, have already been manually filled out in sheets
    values = [[entry[column] for column in entry.keys()] for entry in data]
    # prepare update request 
    body = {'values' : values}
    return body


def upload_all_data(start_date, end_date, to_upload='all'):
    if to_upload == 'all' or to_upload == 'facebook_only':
        facebook = Facebook(access_token,page_token,fb_page_id)
        data_fb = facebook.get_final_data(start_date, end_date)
        body_fb = get_body(data_fb)

        # the specific tab/sheet you want to upload the data to.
        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_rows(body_fb['values'], value_input_option='RAW')
        print('Facebook data uploaded to Google Sheets.')

    if to_upload == 'all' or to_upload == 'instagram_only':
        instagram = Instagram(access_token)
        data_ig = instagram.get_combined_data(start_date, end_date)
        body_ig = get_body(data_ig)

        sheet = spreadsheet.worksheet(sheet_name)
        sheet.append_rows(body_ig['values'], value_input_option='RAW')
        print('Instagram data uploaded to Google Sheets.')

    
# upload_all_data('08/22/2023', '08/30/2023', 'all')
