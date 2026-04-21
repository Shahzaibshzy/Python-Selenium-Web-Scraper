import json

def number_to_words(number):
    one_to_nineteen = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
                       "ten", "eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
    tens = ["", "", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
    
    if number < 20:
        return one_to_nineteen[number]
    elif number < 100:
        return tens[number // 10] + ("" if number % 10 == 0 else one_to_nineteen[number % 10])
    elif number < 1000:
        return one_to_nineteen[number // 100] + "hundred" + ("" if number % 100 == 0 else "and" + number_to_words(number % 100))
    elif number < 100000:
        return number_to_words(number // 1000) + "thousand" + ("" if number % 1000 == 0 else number_to_words(number % 1000))
    elif number < 10000000:
        return number_to_words(number // 100000) + "lakh" + ("" if number % 100000 == 0 else number_to_words(number % 100000))
    else:
        return "Number out of range"

number_dict = {}


for i in range(0, 100001):  
    word_representation = number_to_words(i)
    number_dict[word_representation] = str(i)


json_data = json.dumps(number_dict, indent=4)


with open('number_dict.json', 'w') as f:
    f.write(json_data)
