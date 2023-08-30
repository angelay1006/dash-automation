import time
from datetime import datetime

def str_to_datetime(date_string):
    '''
    Converts a date string in the format 'MM/DD/YYYY' to a datetime object
    Example: 08/18/2023 --> 2023-08-18 00:00:00
    '''
    return datetime.strptime(date_string, '%m/%d/%Y')

def str_to_formatted_date(date_string, output_format='%m/%d/%Y'):
    '''
    Converts a date string to a formatted date string
    Example: '2023-08-12T02:25:05+0000' --> '08/12/2023'
    '''
    parsed_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    formatted_date = parsed_date.strftime(output_format)
    return formatted_date

def simplify_date(date_string):
    '''
    Converts a date string in the format '2023-08-23T08:01:06+0000' to '2023-08-18 00:00:00'
    '''
    parsed_date = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%S%z')
    formatted_date = parsed_date.strftime('%Y-%m-%d 00:00:00')
    return formatted_date

def clean_post_content(content):
    '''
    For purposes of the dashboard, we want to make the content section as 
    clearly readable as possible, hence 1) removing all occurences of newline
    characters, 2) truncating content to better fit in cells 
    '''
    cleaned_content = content.replace('\n', '')
    truncated_content = cleaned_content[:90] + '...' if len(cleaned_content) > 90 else cleaned_content
    return truncated_content

def is_valid_start_date(start_str):
    date_format = "%m/%d/%Y"
    try:
        datetime.strptime(start_str, date_format).date()
        return True, None
    except ValueError:
        return False,  "Invalid end date format. Please enter a valid MM/DD/YYYY."
    
def is_valid_end_date(end_date_str):
    date_format = "%m/%d/%Y"

    try:
        end_date_obj = datetime.strptime(end_date_str, date_format).date()
        current_date = datetime.now().date()

        # Check if the end_date is in the future
        if end_date_obj >= current_date:
            return False, "End date can't be in the future."
        else:
            return True, None  # Valid end date
    except ValueError:
        return False, "Invalid end date format. Please enter a valid MM/DD/YYYY."
