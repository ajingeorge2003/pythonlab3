import gspread
from google.oauth2.service_account import Credentials
import qrcode
from PIL import Image
from pyzbar.pyzbar import decode

users_db = []

create_user_record = lambda name, email: {'name': name, 'email': email}
insert_user_record = lambda user: users_db.append(user)
fetch_all_user_records = lambda: users_db

def get_google_sheet(sheet_name, json_keyfile_name):
    try:
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive.file",
            "https://www.googleapis.com/auth/drive"
            ]
        creds = Credentials.from_service_account_file(json_keyfile_name, scopes=scope)
        client = gspread.authorize(creds)
        sheet = client.open(sheet_name).sheet1
        return sheet
    except Exception as e:
        print(f"Error in getting Google Sheet : {e}")
        return None

def fetch_data_from_google_sheets(sheet_name, json_keyfile_name):
    sheet = get_google_sheet(sheet_name, json_keyfile_name)
    if sheet:
        try:
            records = sheet.get_all_records()
            return records
        except Exception as e:
            print(f"Error in fetching data from Google Sheets: {e}")
            return []
    return []

def register_user_from_google_sheet(sheet_name, json_keyfile_name):
    records = fetch_data_from_google_sheets(sheet_name, json_keyfile_name)
    if records:
        for record in records:
            name = record.get('Name')
            email = record.get('Email')
            if name and email:
                user_record = create_user_record(name, email)
                insert_user_record(user_record)

        print("All registered users:")
        for user in fetch_all_user_records():
            print(user)
    else:
        print("No records found or error in fetching records. ")

def generate_qr_code(data, filename):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L, 
        box_size=10, 
        border=4
        )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black',back_color='white')
    img.save(filename)
    print(f"QR code saved as {filename}")

def decode_qr_code(filename):
    img = Image.open(filename)
    decoded_objects = decode(img)
    for obj in decoded_objects:
        return obj.data.decode('utf-8')
    return None