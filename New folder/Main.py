import multiprocessing
import time
from datetime import datetime
from Logs import Logs
from CragList import CragList
class Main(CragList):
    @property
    def now(self):
        return datetime.now()
    def __init__(self):
        self.process=None
        self.first_craglist=True
        self.first_auto=True
        self.auto_process=None
        self.carglist=CragList()
        self.logs=Logs()
        self.prev_success=0
    

    def sleepy(self):
        time.sleep(900)
    
    def stop_thread(self):
        if(self.auto_process):
            self.auto_process.terminate()
        if(self.process):
            self.process.terminate()

    
    def backend_app(self,threshold,sleep,browser,car_bike):
        if(car_bike=="Cars/Trucks"):
            self.start_scrap(url="https://indianapolis.craigslist.org/search/pittsboro-in/cta?bundleDuplicates=1&lat=39.8982&lon=-86.4345&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~0~0",choice=car_bike,sleep=sleep,threshold=threshold,browser=browser)
        elif(car_bike=="Bike"):
            
            self.start_scrap(url="https://stlouis.craigslist.org/search/owensville-mo/mca?bundleDuplicates=1&lat=38.3487&lon=-91.5191&postedToday=1&purveyor=owner&search_distance=1000#search=1~gallery~0~0",sleep=sleep,threshold=threshold,browser=browser)

        print(type,threshold,sleep)

    
        
    def start_scrap(self,url,choice=None,sleep=0,threshold=0,browser="Headless"):
        if(True):

            while(True):
                if(self.carglist.exit):
                        break
                if(self.logs.get_value_from_file("ERROR.txt")>=threshold//10 or self.first_craglist or self.logs.get_value_from_file("SUCCESS.txt")==0 or int(self.logs.get_value_from_file("SUCCESS.txt"))==self.prev_success or self.logs.get_value_from_file("ERROR.txt")>10*self.logs.get_value_from_file("SUCCESS.txt")):       
                    if(self.process):
                        self.process.terminate()
                        self.carglist.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Killing the Old thread"))
                    self.carglist.logs.append_data_to_file(str(self.now.strftime("%H:%M:%S")+" "+"Starting the new thread"))
                    
                    kiji_instance=CragList(url=url,choice=choice,sleep=sleep,threshold=threshold,browser=browser)
                    self.process = multiprocessing.Process(target=kiji_instance.start_scrap)
                    self.process.start()
                    self.first_craglist=False
                    if(self.carglist.exit):
                        break
                else:
                    pass
                self.prev_success=int(self.logs.get_value_from_file("SUCCESS.txt"))
                self.sleepy()
    

# if __name__=="__main__":
#     main=Main()
#     main.start_scrap("https://kijiji.ca/","Kiji","cars")


