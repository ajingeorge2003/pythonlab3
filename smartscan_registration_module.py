import gspread
from google.oauth2.service_account import Credentials

users_db = []

create_user_record = lambda name, email: {'name': name, 'email': email}
insert_user_record = lambda user: users_db.append(user)
fetch_all_user_records = lambda: users_db

def get_google_sheet(sheet_name, json_keyfile_name):
    scope = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive.file",
        "https://www.googleapis.com/auth/drive"
    ]
    creds = Credentials.from_service_account_file(json_keyfile_name, scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open(sheet_name).sheet1
    return sheet

def fetch_data_from_google_sheets(sheet_name, json_keyfile_name):
    sheet = get_google_sheet(sheet_name, json_keyfile_name)
    records = sheet.get_all_records()
    return records

def register_user_from_google_sheet(sheet_name, json_keyfile_name):
    records = fetch_data_from_google_sheets(sheet_name, json_keyfile_name)
    for record in records:
        name = record.get('Name')
        email = record.get('Email')
        if name and email:
            user_record = create_user_record(name, email)
            insert_user_record(user_record)

    print("All registered users:")
    for user in fetch_all_user_records():
        print(user)