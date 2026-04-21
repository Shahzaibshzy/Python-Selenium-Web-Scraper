import pandas as pd
from datetime import datetime
import traceback
import threading
import Google_sheet   # make sure the filename is Google_sheet.py (not GoogleSheet.py)

def safe_save_excel_or_csv(df, excel_path):
    try:
        df.to_excel(excel_path, index=False, engine='openpyxl')
        return True
    except Exception as e:
        print("Failed to write Excel:", e)
        print(traceback.format_exc())
        # fallback: save CSV instead
        csv_path = excel_path.replace('.xlsx', '.csv')
        try:
            df.to_csv(csv_path, index=False)
            print("Saved fallback CSV to", csv_path)
            return True
        except Exception as e2:
            print("Failed to write fallback CSV:", e2)
            return False


def push_data(data, name):
    data_to_append = pd.DataFrame(data, index=[0])

    # === Google Sheet push ===
    if name == "craigslist_cars":
        create_crag_car_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Craglist_cars"))
        thread.start()

    elif name == "craigslist_bikes":
        create_crag_bike_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Craglist_bikes"))
        thread.start()

    # === Excel backup ===
    excel_file_path = f"{name}.xlsx"
    try:
        existing_data = pd.read_excel(excel_file_path)
        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)
    except FileNotFoundError:
        combined_data = data_to_append

    safe_save_excel_or_csv(combined_data, excel_file_path)


def create_crag_car_id(data):
    ids = {'ad_id': data['ad_id']}
    data_to_append = pd.DataFrame(ids, index=[0])
    excel_file_path = "craigslist_cars_ids.xlsx"

    try:
        existing_data = pd.read_excel(excel_file_path)
        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)
    except FileNotFoundError:
        combined_data = data_to_append

    safe_save_excel_or_csv(combined_data, excel_file_path)


def create_crag_bike_id(data):
    ids = {'ad_id': data['ad_id']}
    data_to_append = pd.DataFrame(ids, index=[0])
    excel_file_path = "craigslist_bikes_ids.xlsx"

    try:
        existing_data = pd.read_excel(excel_file_path)
        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)
    except FileNotFoundError:
        combined_data = data_to_append

    safe_save_excel_or_csv(combined_data, excel_file_path)


def check_id(ad_id, mobile_number, type_):
    ids_file = f"{'craigslist_cars' if type_ == 'craigslist_cars' else 'craigslist_bikes'}_ids.xlsx"
    data_file = f"{'craigslist_cars' if type_ == 'craigslist_cars' else 'craigslist_bikes'}.xlsx"

    try:
        if not pd.io.common.file_exists(ids_file):
            pd.DataFrame(columns=['ad_id']).to_excel(ids_file, index=False, engine='openpyxl')
        if not pd.io.common.file_exists(data_file):
            pd.DataFrame(columns=['mobile_number']).to_excel(data_file, index=False, engine='openpyxl')

        xl = pd.read_excel(ids_file)
        x2 = pd.read_excel(data_file)
    except Exception as e:
        print("Error reading id or data file:", e)
        return False

    if str(ad_id) in xl['ad_id'].astype(str).values:
        return True
    mobile = x2.dropna(subset=['mobile_number'])
    if mobile_number and mobile_number in mobile['mobile_number'].astype(str).values:
        return True
    return False
