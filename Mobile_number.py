import re
import json

# Load number dictionary
with open('number_dict.json', 'r') as f:
    word_to_digit = json.load(f)

def find_number(string):
    string = string.lower()

    # Replace word numbers with digits
    for word, digit in word_to_digit.items():
        string = re.sub(r'\b' + re.escape(word) + r'\b', digit, string)

    # Remove any characters that are not digits or letters
    string = re.sub(r'[^a-z0-9]', '', string)

    mobile_number = ""
    possible_number = []

    for ch in string:
        if ch.isdigit():
            mobile_number += ch
        else:
            # If we reach a letter, check if we have 10+ digits
            if len(mobile_number) >= 10:
                possible_number.append(mobile_number)
            mobile_number = ""

    # Check last collected number
    if len(mobile_number) >= 10:
        possible_number.append(mobile_number)

    # Return all detected numbers
    return possible_number
