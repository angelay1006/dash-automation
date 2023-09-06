# Engagement Dash Automation

## Introduction

Welcome to Engagement Dash Automation! Are you harnessing the full potential of your social media presence? This project is designed to simplify the process of collecting and managing engagement metrics from Facebook and Instagram. Traditionally, gathering these metrics required manual effort within Meta Business Suites, but Engagement Dash Automation streamlines this task by utilizing the Meta API. 

## Table of Contents

- [Introduction](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
- [Features](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
- [Getting Started](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
    - [Prerequisites](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
    - [Installation](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
- [Usage](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)
- [Limitations](#limitations)
- [Contact](https://www.notion.so/Dash-Automation-README-b3f7b135249e45478a59c3e17a9237ce?pvs=21)

## Features

- **Automated Data Retrieval**: Engagement Dash Automation largely automates the retrieval of pre-defined engagement metrics (see [here](https://docs.google.com/spreadsheets/d/1YddmdXVaet0obMYtKHIJXwGVMNffC-wuqIuFEjYYAQ4/edit#gid=0)) from Facebook and Instagram, saving valuable time and effort.
    - 🚀 **Boosted**: Reach a wider audience with paid advertising, maximizing your impact.
    - 👍 **Reactions**: Gauge user engagement with likes.
    - 🔄 **Shares**: Measure the ripple effect as your content spreads through messaging, other pages, and groups.
    - 👁️ **Views**: Know how long users engage with your videos, a crucial factor in content effectiveness.
    - 🗣️ **Comments**: Understand audience sentiment and feedback through comments
    - 📥 **Saves**: Discover what content resonates most as users add it to their favorites.
    - 📈 **Reach**: Track the unique users who see your posts
    - 👥 **Follower Reach**: Ensure loyal followers are engaged and involved.
    - 🌐 **Non-follower Reach**: Expand influence by reaching beyond the current follower base.
- **Data Parsing and Organization**: The project parses, sorts, and organizes the data to make it easily understandable and accessible for further analysis.
- **Seamless Integration with Google Sheets**: The reformatted and organized data is seamlessly uploaded to a Google Sheet, providing a convenient way to store and visualize the data.

## Getting Started

### Prerequisites

Ensure that you have ********all******** components listed below before continuing onto the next step!

#### Meta

1. Ensure that you have an Instagram or Facebook business account, or both! You will need your Facebook page ID (`facebook_page_id`). ([Documentation](https://www.facebook.com/business/help/2814101678867149))
2. Create your own Facebook App. You won’t have to actually create an app - you just need this for the credentials that you’re going to pass to the program.
    1. Go to the **[Facebook for Developers](https://developers.facebook.com/)** website. Click on "Get Started" and follow the prompts to create a new app. Once your app is created, you'll have access to the App ID (`client_id`) and App Secret (`client_secret`).
    2. Access the Facebook Graph API Explorer [here](https://developers.facebook.com/tools/explorer/). There is a “User Token” field. Click on “Get User Access Token”. Copy the generated access token, which will appear in the “Access Token” field. This will be your `temp_access_token`. 

#### Google Sheets

1. A Google Sheet following this [template](https://docs.google.com/spreadsheets/d/1YddmdXVaet0obMYtKHIJXwGVMNffC-wuqIuFEjYYAQ4/edit#gid=0) (you can make a copy). The title of your file is `spreadsheet_name`, and the tab that you want to upload your data to is `sheet_name`. By default, this would be “Content” unless you change the name of that tab.
2. Create/configure your [Google Cloud](https://console.cloud.google.com/welcome?project=pomodoro-party-8e414) service account such that you can authorize changes to the above Google Sheet. Download your service account key file. ([Documentation](https://cloud.google.com/iam/docs/keys-create-delete)) 

### Installation

Clone this repository in the directory of your choice. Now, add the service account key file into the same directory. Copy the relative path to the key file - this will be `json_keyfile_path`. 

## Usage

1. Open the project in the IDE of your choice. There is a `config.json` which stores the necessary credentials. It looks like the below. Refer to the Prerequisites section for the right credential to store. 

```jsx
{
    "meta_api": {
      "client_id": "YOUR_CLIENT_ID", 
      "client_secret": "YOUR_CLIENT_SECRET",
      "temp_access_token": "YOUR_TEMPORARY_ACCESS_TOKEN",
      "long_lived_user_access_token": "YOUR_LONG_LIVED_USER_ACCESS_TOKEN",
      "facebook_page_id": "YOUR_FACEBOOK_PAGE_ID"
    },
    "google_api": {
      "json_keyfile_path": "PATH_TO_YOUR_JSON_KEYFILE",
      "spreadsheet_name": "NAME_OF_YOUR_SPREADSHEET_FILE",
      "sheet_name": "NAME_OF_YOUR_INDIVIDUAL_SHEET"
    } 
}
```

1. Open terminal, ensuring that you have navigated to the correct directory (should be the main directory of the project) 
2. Run `main.py` by using the command `python3 main.py`. Follow the prompts on the screen for specifying the start/end date of the post data that you want to collect and upload. Please keep in mind that the end date is *****not inclusive,***** and that the input date format is MM/DD/YYYY. Once the program finishes running, your selected data should be uploaded to Google Sheets.  

## Limitations

Some metrics on certain platforms are not available through the API, and have to be accessed through manual means (such as directly looking at insights through the Instagram app). 

#### Facebook

- Saves are not available through the Facebook API.
- Views are only valid for media such as Reels and Videos.

#### Instagram

- Follower and Non-follower reach metrics are not available through the Instagram API.

## Contact

email: angela1006yeung@gmail.com or angela_yeung@brown.edu
