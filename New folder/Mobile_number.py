import re
import json
with open('number_dict.json', 'r') as f:
    word_to_digit=json.load(f)
def find_number(string):
    string=string.lower()

    for word, digit in word_to_digit.items():
        string = string.replace(word, digit)
    pattern = re.compile('[\W_]+')    
    string=pattern.sub('', string)
    mobile_number=""
    possible_number=[]
    flag=True
    for i in string:
        if(i.isalpha()):
            if(len(mobile_number)==10 or len(mobile_number)==11):
                possible_number.append(mobile_number)
            mobile_number=""
        else:
            mobile_number+=i
    if(len(mobile_number)==10 or len(mobile_number)==11):
            possible_number.append(mobile_number)
    return possible_number

