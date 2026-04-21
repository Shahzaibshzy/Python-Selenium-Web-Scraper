import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd

def authorize_google_sheets():
    scope = ['https://spreadsheets.google.com/feeds',
             'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name('Kijiji_Sheet_secret_token.json', scope)
    client = gspread.authorize(creds)
    return client

def get_sheet(client, name):
    sheet = client.open(name).sheet1
    return sheet

def append_data_to_sheet(sheet, data_to_append):
    # If the sheet is empty, append the column names first
    if not sheet.get_all_records():
        sheet.append_row(data_to_append.columns.tolist())
    
    # Append the data
    for row in data_to_append.values.tolist():
        sheet.append_row(row)

def push_data(data, name):
    data_to_append = pd.DataFrame(data,index=[0])

    client = authorize_google_sheets()
    sheet = get_sheet(client, name)
    append_data_to_sheet(sheet, data_to_append)
    

