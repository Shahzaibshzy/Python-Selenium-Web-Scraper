import pandas as pd
from datetime import datetime
import Google_sheet
import threading

def push_data(data,name):
    data_to_append=pd.DataFrame(data,index=[0])

    if(name=="craigslist_cars"):
        create_crag_car_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Craglist_cars"))
        thread.start()
        # Google_sheet.push_data(data=data,name="Kijiji_Auto_Data")
    elif(name=="craigslist_bikes"):
        create_crag_bike_id(data)
        thread = threading.Thread(target=Google_sheet.push_data, args=(data, "Craglist_bikes"))
        thread.start()
        # Google_sheet.push_data(data=data,name="Kijiji_Data")


    excel_file_path = '{}.xlsx'.format(name)
    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
        
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def create_crag_car_id(data):
    ids={}
    ids['ad_id']=data['ad_id']
    data_to_append=pd.DataFrame(ids,index=[0])
    excel_file_path = '{}_ids.xlsx'.format("craigslist_cars")

    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def create_crag_bike_id(data):
    ids={}
    ids['ad_id']=data['ad_id']
    data_to_append=pd.DataFrame(ids,index=[0])
    excel_file_path = '{}_ids.xlsx'.format("craigslist_bikes")

    try:
        existing_data = pd.read_excel(excel_file_path)

        combined_data = pd.concat([existing_data, data_to_append], ignore_index=True)

        
    except FileNotFoundError:
        combined_data = data_to_append
        
    try:
        combined_data.to_excel(excel_file_path, index=False)
    except:
        pass

def check_id(id,mobile_number,type):
    xl=None
    try:
        if(type=="craigslist_cars"):
            xl = pd.ExcelFile('craigslist_cars_ids.xlsx')
            x2=pd.ExcelFile('craigslist_cars.xlsx')
        elif(type=="craigslist_bikes"):
            xl = pd.ExcelFile('craigslist_bikes_ids.xlsx')
            x2=pd.ExcelFile('craigslist_bikes.xlsx')
        df = xl.parse('Sheet1')
        df_mobile=x2.parse('Sheet1')
        mobile=df_mobile.dropna(subset=['mobile_number'])

        if id in df['ad_id'].values or int(id) in df['ad_id'].values or int(mobile_number) in mobile['mobile_number'].values or mobile_number in mobile['mobile_number']:
            return True
    except:
        return False
    return False
