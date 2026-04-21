from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import ActionChains
from datetime import datetime
import Data_push
from Logs import Logs
from urllib.parse import urlparse
from selenium.webdriver.firefox.options import Options as FirefoxOptions
import Mobile_number
import pandas as pd
import os
import re
import time
import json

class CragList:
    @property
    def now(self):
        return datetime.now()
    
    def __init__(self,url=None,choice=None,sleep=0,threshold=0,browser="Headless"):
        self.choice=choice
        self.final_data=[]
        self.data = []
        self.sleep = 1
        self.stop = True
        self.page = 0
        self.li_batch=[]
        self.url=url
        self.kiji_sucess=0
        self.driver=None
        self.sleep=sleep
        self.thresh=threshold
        self.thresh_kiji=0
        self.logs=Logs()
        self.browser=browser
        self.exit=False
        self.kind=""
        self.page=1
        
        
        timestamp = self.now.strftime("%Y-%m-%d_%H-%M-%S")
        self.excel_file_car = f"craigslist_car_{timestamp}.xlsx"
        self.excel_file_bike = f"craigslist_bike_{timestamp}.xlsx"

        # Track previously scraped URLs
        self.scraped_links_file = "scraped_links.json"
        if os.path.exists(self.scraped_links_file):
            with open(self.scraped_links_file, "r") as f:
                self.scraped_links = set(json.load(f))
        else:
            self.scraped_links = set()

    def save_links(self):
        with open(self.scraped_links_file, "w") as f:
            json.dump(list(self.scraped_links), f, indent=4)

    def save_excel(self, file):
        if self.data:
            df = pd.DataFrame(self.data)
            df.to_excel(file, index=False)

    def process_ad(self, ad_url, title, price, description, owner, phone):
        if ad_url in self.scraped_links:
            print(f"[SKIP] Duplicate ad: {ad_url}")
            return

        self.data.append({
            "Title": title,
            "Price": price,
            "URL": ad_url,
            "Owner": owner,
            "Phone": phone,
            "Description": description
        })
        self.scraped_links.add(ad_url)
        # Save current run data
        self.save_excel(self.current_excel)
        self.save_links()
        
    def repeat_search(self,element,type,action,data=None):
        
        i=0
        while(i<5):
            time.sleep(1)
            try:
                if(type=="XPATH"):
                    if(action["event"]=="click"):
                        print("clickkk")
                        self.wait.until(EC.presence_of_element_located((By.XPATH,element))).click()
                elif(type=="ID"):
                    if(action['event']=="send"):

                        self.wait.until(EC.presence_of_element_located((By.ID,element))).send_keys(data)
                    elif(action['event']=="element"):
                        self.wait.until(EC.presence_of_element_located((By.ID,element)))
                return
    
            except Exception as e:
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Error : Error locating element"))
                self.logs.increment_value_in_file("ERROR.txt")
                print(e)
                time.sleep(1)
                i+=1
                
    def get_item_details(self):
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Element targetted successfully"))  
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Fetching data"))  
        data={}
        flag=False
        self.stop_flag = False
        wait=WebDriverWait(self.driver,self.sleep//10)
        
        # time.sleep(self.sleep//3)
        try:
            try:
                scroll_height = self.driver.execute_script("return document.body.scrollHeight;")
                self.driver.execute_script(f"window.scrollTo(0, {scroll_height - 300});")
                href = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".show-contact")))
                # self.driver.execute_script("arguments[0].scrollIntoView();", href)
                i=0
                while(i<5):
                    
                    try:
                        time.sleep(2)     
                        href.click()
                    except:
                        break
                    i+=1
                # wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.challenge-container')))
            except: 
               pass
                
            self.driver.execute_script("window.scrollTo(0, 0);")
            self.driver.execute_script("window.scrollBy({ top: 250, behavior: 'smooth' });" )
            body=self.wait.until(EC.presence_of_element_located((By.ID,'postingbody'))).text
            mobile_number_list=Mobile_number.find_number(body)
            print("Mobile Number",mobile_number_list)
            if(len(mobile_number_list)==0):
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Phone number not found"))
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next data"))    
                return
            mobile_number=",".join(mobile_number_list)
                
            name=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.attr.important'))).text
            price=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.price'))).text
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            ad_id = self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.postinginfos p'))).text
            ad_id=ad_id.replace('post id: ', '').strip()
            data['ad_id']=ad_id
            data['vehicle_name']=name
            data['price']=price
            data['mobile_number']=mobile_number
            data['URL']=self.driver.current_url
            data['Captcha']=""
            
            flag=True
            self.logs.increment_value_in_file("SUCCESS.txt")

            
        except Exception as e:
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Phone number not found"))
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next data"))    
            pass
            #https://www.autotrader.ca/a/honda/hr-v/saint-jean-sur-richelieu/quebec/19_12765798_/?showcpo=ShowCpo&ncse=no&ursrc=pl&urp=7&urm=8&pc=M5V%203L9&sprx=-1
        if(flag==True):
            self.thresh_kiji+=1
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Phone number found"))
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Pushing data to excel"))
            self.logs.increment_value_in_file("SUCCESS.txt")
            print("SUCCESS")
            
            self.push_data_to_excel(data)
        print("DATA:",data)

        
    
    def push_data_to_excel(self,data):
        self.logs.append_data_to_file(f"[DEBUG] Saving data with kind = {self.kind}")
        self.logs.append_data_to_file(f"[DEBUG] Data to save: {data}")
        if(not Data_push.check_id(data['ad_id'],data['mobile_number'],self.kind)):
            Data_push.push_data(data,self.kind)
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully added the data"))
        else:
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Infor : Duplicate Detected"))

        
        self.logs.increment_value_in_file("SUCCESS.txt")
        
    
    def car_scrap(self):
        self.current_excel = self.excel_file_car
        while True:
            if hasattr(self, 'stop') and not self.stop:
                print("Car scraper stopped by user.")
                self.save_excel(self.current_excel)
                break

            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except:
                print("Body not loaded, refreshing...")
                self.driver.refresh()
                time.sleep(self.sleep)
                continue

            # Scroll down
            try:
                total_height = self.driver.execute_script("return document.body.scrollHeight")
                step_size = total_height // 50
                for i in range(1, 50):
                    if hasattr(self, 'stop') and not self.stop:
                        break
                    self.driver.execute_script(f"window.scrollTo(0, {i * step_size});")
                    time.sleep(0.2)
            except:
                pass

            hrefs = self.get_ads_links()
            print("Collected links:", hrefs[:5])
            if not hrefs:
                print("No ads found.")
                break

            for ad_url in hrefs:
                if hasattr(self, 'stop') and not self.stop:
                    print("Car scraper stopped by user.")
                    self.save_excel(self.current_excel)
                    return

                if ad_url.startswith("/"):
                    base_url = self.driver.current_url.split(".org")[0] + ".org"
                    ad_url = base_url + ad_url

                if ad_url in [d['URL'] for d in self.data]:
                    continue  # skip duplicates in current run

                try:
                    self.driver.get(ad_url)
                    time.sleep(self.sleep)

                    title = self.driver.find_element(By.ID, "titletextonly").text.strip() \
                        if self.driver.find_elements(By.ID, "titletextonly") else "N/A"
                    price = self.driver.find_element(By.CSS_SELECTOR, ".price").text.strip() \
                        if self.driver.find_elements(By.CSS_SELECTOR, ".price") else "N/A"
                    description = self.driver.find_element(By.ID, "postingbody").text.strip() \
                        if self.driver.find_elements(By.ID, "postingbody") else "N/A"

                    phone = "N/A"
                    owner = "N/A"

                    # Show contact info with JS click to avoid interception
                    if self.driver.find_elements(By.CSS_SELECTOR, "a.show-contact"):
                        show_contact = self.driver.find_element(By.CSS_SELECTOR, "a.show-contact")
                        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", show_contact)
                        time.sleep(1)
                        try:
                            self.driver.execute_script("arguments[0].click();", show_contact)
                            time.sleep(2)
                        except:
                            print(f"[WARN] Could not click show-contact for {ad_url}")

                        if self.driver.find_elements(By.CSS_SELECTOR, "div.contact-info"):
                            contact_box = self.driver.find_element(By.CSS_SELECTOR, "div.contact-info")
                            contact_text = contact_box.text
                            phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", contact_text)
                            if phone_match:
                                phone = phone_match.group()
                            owner = self.driver.find_element(By.CSS_SELECTOR, "div.contact-info h3").text.strip() \
                                if self.driver.find_elements(By.CSS_SELECTOR, "div.contact-info h3") else "N/A"

                    # Fallback: extract number from description
                    if phone == "N/A":
                        numbers_in_desc = Mobile_number.find_number(description)
                        if numbers_in_desc:
                            phone = numbers_in_desc[0]

                    # Skip if no number found
                    if phone == "N/A":
                        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")) + f" Info : Skipped ad (no phone) {ad_url}")
                        continue

                    self.process_ad(ad_url, title, price, description, owner, phone)
                    self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")) + f"[OK] Car ad saved: {ad_url}")

                except Exception as e:
                    print(f"Error processing car ad {ad_url}: {e}")
                    self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")) + " Info : Missed retrying")
                    self.logs.increment_value_in_file("ERROR.txt")




    def bike_scrap(self):
        self.current_excel = self.excel_file_bike
        while True:
            if hasattr(self, 'stop') and not self.stop:
                print("Bike scraper stopped by user.")
                self.save_excel(self.current_excel)
                break

            try:
                self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
            except:
                print("Body not loaded, refreshing...")
                self.driver.refresh()
                time.sleep(self.sleep)
                continue

            containers = self.driver.find_elements(By.CSS_SELECTOR, "div.gallery-card")
            if not containers:
                print("No bike ads found.")
                self.driver.refresh()
                time.sleep(self.sleep)
                continue

            hrefs = []
            for c in containers:
                try:
                    a = c.find_element(By.CSS_SELECTOR, "a.main")
                    hrefs.append(a.get_attribute("href"))
                except: pass
                try:
                    a2 = c.find_element(By.CSS_SELECTOR, "a.cl-app-anchor.cl-search-anchor.text-only.posting-title")
                    hrefs.append(a2.get_attribute("href"))
                except: pass

            hrefs = list(set(hrefs))
            print("Collected bike links:", hrefs[:5])

            for ad_url in hrefs:
                if hasattr(self, 'stop') and not self.stop:
                    print("Bike scraper stopped by user.")
                    self.save_excel(self.current_excel)
                    return

                try:
                    self.driver.get(ad_url)
                    time.sleep(self.sleep)

                    title = self.driver.find_element(By.ID, "titletextonly").text.strip() \
                        if self.driver.find_elements(By.ID, "titletextonly") else "N/A"
                    price = self.driver.find_element(By.CSS_SELECTOR, "span.price").text.strip() \
                        if self.driver.find_elements(By.CSS_SELECTOR, "span.price") else "N/A"
                    description = self.driver.find_element(By.ID, "postingbody").text.strip() \
                        if self.driver.find_elements(By.ID, "postingbody") else "N/A"

                    phone = "N/A"
                    owner = "N/A"

                    if self.driver.find_elements(By.CSS_SELECTOR, "a.show-contact"):
                        show_contact = self.driver.find_element(By.CSS_SELECTOR, "a.show-contact")
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", show_contact)
                        show_contact.click()
                        time.sleep(2)

                        if self.driver.find_elements(By.CSS_SELECTOR, "div.contact-info"):
                            contact_box = self.driver.find_element(By.CSS_SELECTOR, "div.contact-info")
                            contact_text = contact_box.text
                            phone_match = re.search(r"\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}", contact_text)
                            if phone_match:
                                phone = phone_match.group()
                            owner = self.driver.find_element(By.CSS_SELECTOR, "div.contact-info h3").text.strip() \
                                if self.driver.find_elements(By.CSS_SELECTOR, "div.contact-info h3") else "N/A"

                    if phone == "N/A":
                        numbers_in_desc = Mobile_number.find_number(description)
                        if numbers_in_desc:
                            phone = numbers_in_desc[0]

                    if phone == "N/A":
                        continue

                    self.process_ad(ad_url, title, price, description, owner, phone)
                    self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")) + f"[OK] Bike ad saved: {ad_url}")
                    

                except Exception as e:
                    print(f"Error processing bike ad {ad_url}: {e}")
                    self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")) + " Info : Missed retrying")
                    self.logs.increment_value_in_file("ERROR.txt")

            # Move to next page
            self.page += 1
            next_page_url = f"https://stlouis.craigslist.org/search/owensville-mo/mca?bundleDuplicates=1&lat=38.3487&lon=-91.5191&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~{self.page}~0"
            self.driver.get(next_page_url)
            time.sleep(self.sleep)
        
        #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=0&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch
    #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=45&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch    
    
    def get_ads_links(self):
        try:
            # Always re-find elements fresh
            ad_elements = self.driver.find_elements(By.CSS_SELECTOR, "a.cl-app-anchor.cl-search-anchor.posting-title")

            hrefs = []
            for el in ad_elements:
                try:
                    hrefs.append(el.get_attribute("href"))
                except:
                    continue  # skip if element goes stale mid-loop

            print(f"DEBUG: Selector found {len(hrefs)} ads")
            return hrefs

        except Exception as e:
            print(f"DEBUG: Selector failed -> {e}")
            return []




        

    
    def start_scrap(self):
            
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Starting the Scrapping process"))
        
        options = Options()
        

        options.page_load_strategy ="eager"
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--ignore-ssl-errors')
        options.add_argument("--disable-popup-blocking")
        options.add_argument("start-maximized")
        if(self.browser=="Headless"):

            # width,height=pyautogui.size()
            options.add_argument("--headless")
            # options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537')
            
            # options.add_experimental_option("excludeSwitches", ["enable-automation"])
            # options.add_experimental_option('useAutomationExtension', False)
            options.add_argument('--disable-popup-blocking')
            print("HEADLESS")
            options.add_experimental_option("excludeSwitches", ["disable-popup-blocking"])

        self.driver = webdriver.Chrome(options=options)
        self.wait=WebDriverWait(self.driver, self.sleep//2)
        self.driver.get(self.url)
        self.driver.implicitly_wait(20)
        
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Loaded the site")) 
        if(self.choice=="Cars/Trucks"):
            self.kind="craigslist_cars"
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Start Scrapping car data"))  
            self.logs.increment_value_in_file("SUCCESS.txt")
            self.car_scrap()
        else:
            self.kind="craigslist_bikes"
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Start Scrapping bike data"))  
            self.logs.increment_value_in_file("SUCCESS.txt")
            self.bike_scrap()

# if __name__=="__main__":
#     auto=Autotrader(url="https://indianapolis.craigslist.org/search/pittsboro-in/cta?bundleDuplicates=1&lat=39.8982&lon=-86.4345&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~0~0",choice="Cars/Trucks",browser="Head",sleep=10)
#     auto.start_scrap()
