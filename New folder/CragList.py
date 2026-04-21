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

class CragList:
    @property
    def now(self):
        return datetime.now()
    
    def __init__(self,url=None,choice=None,sleep=0,threshold=0,browser="Headless"):
        self.choice=choice
        self.final_data=[]
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
        if(not Data_push.check_id(data['ad_id'],data['mobile_number'],self.kind)):
            Data_push.push_data(data,self.kind)
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Success : Successfully added the data"))
        else:
            self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Infor : Duplicate Detected"))

        
        self.logs.increment_value_in_file("SUCCESS.txt")
        
    
    def car_scrap(self):
        time.sleep(self.sleep)
        car=None
        total_height = self.driver.execute_script("return document.body.scrollHeight")

        step_size = total_height // 50

        for i in range(1, 50):
            self.driver.execute_script(f"window.scrollTo(0, {i * step_size});")
            time.sleep(0.5)  


        for i in range(49, 0, -1):
            self.driver.execute_script(f"window.scrollTo(0, {i * step_size});")
            time.sleep(0.5) 
        try:
            car=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.results.cl-results-page')))
        except:
            self.driver.refresh()
            time.sleep(self.sleep)
            self.car_scrap()
        
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scarpping started"))  
        time.sleep(self.sleep//2)
        car_ul=car.find_element(By.TAG_NAME,'ol')
        car_list=car_ul.find_elements(By.TAG_NAME,'a')
        for car in car_list:
            try:
                # href_car=car.find_element(By.CSS_SELECTOR,".inner-link")
                self.driver.execute_script("arguments[0].scrollIntoView();", car)
                # href_tag=href_car.get_attribute("href")
                # self.driver.execute_script("window.open('" + href_tag +"');")
                ActionChains(self.driver) \
                                        .key_down(Keys.CONTROL) \
                                        .click(car) \
                                        .key_up(Keys.CONTROL) \
                                        .perform()
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(self.sleep//2)
                self.get_item_details()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.logs.increment_value_in_file("SUCCESS.txt")
            except Exception as e:
                print(e)
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Missed retrying"))  
                self.logs.increment_value_in_file("ERROR.txt")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next page"))  
        self.driver.get("https://indianapolis.craigslist.org/search/pittsboro-in/cta?bundleDuplicates=1&lat=39.8982&lon=-86.4345&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~{}~0".format(self.page))
        self.page+=1
        self.car_scrap()
        
        
    def bike_scrap(self):
        time.sleep(self.sleep)
        car=None
        total_height = self.driver.execute_script("return document.body.scrollHeight")

        step_size = total_height // 50

        for i in range(1, 50):
            self.driver.execute_script(f"window.scrollTo(0, {i * step_size});")
            time.sleep(1)  


        for i in range(49, 0, -1):
            self.driver.execute_script(f"window.scrollTo(0, {i * step_size});")
            time.sleep(1) 
        try:
            car=self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'.results.cl-results-page')))
        except:
            self.driver.refresh()
            time.sleep(self.sleep)
            self.car_scrap()
        
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Scarpping started"))  
        time.sleep(self.sleep//2)
        car_ul=car.find_element(By.TAG_NAME,'ol')
        car_list=car_ul.find_elements(By.TAG_NAME,'a')
        for car in car_list:
            try:
                
                # href_car=car.find_element(By.CSS_SELECTOR,".inner-link")
                self.driver.execute_script("arguments[0].scrollIntoView();", car)
                # href_tag=href_car.get_attribute("href")
                # self.driver.execute_script("window.open('" + href_tag +"');")
                ActionChains(self.driver) \
                                        .key_down(Keys.CONTROL) \
                                        .click(car) \
                                        .key_up(Keys.CONTROL) \
                                        .perform()
                self.driver.switch_to.window(self.driver.window_handles[1])
                time.sleep(self.sleep//2)
                self.get_item_details()
                self.driver.close()
                self.driver.switch_to.window(self.driver.window_handles[0])
                self.logs.increment_value_in_file("SUCCESS.txt")
            except Exception as e:
                print(e)
                self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Missed retrying"))  
                self.logs.increment_value_in_file("ERROR.txt")
        self.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Info : Moving to next page"))  
        self.driver.get("https://stlouis.craigslist.org/search/owensville-mo/mca?bundleDuplicates=1&lat=38.3487&lon=-91.5191&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~{}~0".format(self.page))
        self.page+=1
        self.bike_scrap()
        
        
        
        #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=0&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch
    #https://www.autotrader.ca/motorcycles-atvs/all/?rcp=15&rcs=45&srt=9&yRng=1976%2C&prx=-1&loc=M5V%203L9&hprc=False&wcp=False&sts=New-Used&adtype=Private&showcpo=1&inMarket=advancedSearch    
    
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
