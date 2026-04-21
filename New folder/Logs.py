class Logs:
    def __init__(self):
        self.filename="crag_all_log.txt"
        
    def append_data_to_file(self, data):
        with open(self.filename, 'a') as f:  
            f.write(data + '\n')  

    def read_latest_data_from_file(self):
        try:

            with open(self.filename, 'r') as f:  
                lines = f.readlines()  
                if lines:  
                    return lines[-1]  
                else:
                    return None  
        except:
            return ""
        
    def increment_value_in_file(self,filename):
        try:
            with open(filename, 'r+') as f:
                value = int(f.read() or 0)
                value += 1
                f.seek(0)
                f.write(str(value))
        except FileNotFoundError:
            with open(filename, 'w') as f:
                f.write('1')

    def get_value_from_file(self,filename):
        try:
            with open(filename, 'r') as f:
                value = int(f.read())
                return value
        except FileNotFoundError:
            return 0