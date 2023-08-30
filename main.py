from google_sheets import upload_all_data
import utils

def main():
    while True:
        start_date = input("Enter start date (MM/DD/YYYY): ")
        is_valid, error_message = utils.is_valid_start_date(start_date)
        
        if is_valid:
            break  
        else:
            print("Error: ", error_message)

    while True:
        end_date = input("Enter end date (MM/DD/YYYY): ")

        is_valid, error_message = utils.is_valid_end_date(end_date)
        if is_valid:
            break  
        else:
            print("Error: ", error_message)
        

    to_upload_options = ['all', 'facebook_only', 'instagram_only']
    to_upload = input("Enter 'all' to upload all data, 'facebook_only' for Facebook data, or 'instagram_only' for Instagram data: ")

    while to_upload not in to_upload_options:
        print("Invalid input. Please choose from: 'all', 'facebook_only', 'instagram_only'")
        to_upload = input("Enter your choice: ")

    upload_all_data(start_date, end_date, to_upload)


if __name__ == "__main__":
    main()