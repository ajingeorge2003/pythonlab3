import smartscan_registration_module as srm

sheet_name = "Registration_details"
json_keyfile_name = "./credentials.json"
print(f"Smartscan registration : \n 1.User registration from Forms and Print the users\n 2.Generate QR code for users user\n 3.Read QR code of a user\n4. Exit")
choice = int(input("Enter your choice : "))
while True:
    if choice == 1:
        srm.register_user_from_google_sheet(sheet_name,json_keyfile_name)
        break
    elif choice == 2:
        records = srm.fetch_data_from_google_sheets(sheet_name, json_keyfile_name)
        for i, record in enumerate(records):
            name = record.get('Name')
            email = record.get('Email')
            if name and email:
                data = f"{name},{email}"
                filename = f"user_{i+1}_qrcode.png"
                srm.generate_qr_code(data, filename)
        break
    elif choice == 3:
        filename = input("Enter the name of the file correctly : ")
        data = srm.decode_qr_code(filename)
        if data:
            name, email = data.split(',')
            print(f"Decoded data from {filename} : Name - {name}, Email - {email}")
        break
    elif choice == 4:
        exit(0)