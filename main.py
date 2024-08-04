import smartscan_registration_module as srm

sheet_name = "Registration_details"
json_keyfile_name = "./credentials.json"

srm.register_user_from_google_sheet(sheet_name,json_keyfile_name)