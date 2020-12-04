import constants


# This reads a char array of keys and values and converts
# it to a dictionary
def char_array_to_dictionary(char_array, separator):
    dictionary = {}
    if len(char_array) == 0:
        return

    first = True
    reading_value = False
    key = ""
    value = ""

    for char in char_array:
        # Ignoring first \\ if present
        if first and char == separator:
            first = False
            continue

        if char == separator:
            if reading_value:
                dictionary[key] = value
                value = ""
                key = ""
            reading_value = not reading_value
            continue
        elif not reading_value:
            key += char
        else:
            value += char

    # Adding the last key-value pair because there's no
    # separator in the end of the array
    dictionary[key] = value

    return dictionary

'''
# Tries to find a value matching the given string key in
# an array of characters
def find_value_for_key(char_array, key):
    reading_value = False
    final_value_being_read = False
    first = True
    value = ""
    last_key = ""

    for char in char_array:
        # Ignoring first \\ if present
        if first and char == '\\':
            first = False
            continue

        if char == '\\':
            if final_value_being_read:
                break
            if not reading_value:
                if last_key == key:
                    final_value_being_read = True
            else:
                last_key = ""
            reading_value = not reading_value
        elif not reading_value:
            last_key += char
        elif final_value_being_read:
            value += char

    if final_value_being_read:
        return value
    else:
        return False
'''

# Updates value of a key in an array of characters
# key and value are string, max_size is an integer
# Returns either True or False and
# an array of characters (updated or original)
'''
def set_value_for_key(char_array, key, value, max_size):
    original_char_array = char_array.copy()
    if len(char_array) < 1:
        return False, original_char_array

    # Star keys can't be modified
    if key[0] == '*':
        return False, original_char_array

    if key.find('\\') != -1 or value.find('\\') != -1 or key.find('\"') != -1 or value.find('\"') != -1 or \
       len(key) >= constants.MAX_INFO_KEY or len(value) >= constants.MAX_INFO_KEY:
        print("Invalid key and/or value in set_value_for_key")
        return False, original_char_array

    reading_value = False
    key_found = False
    first = True
    last_key = ""

    for char in char_array:
        # Ignoring first \\ if present
        if first and char == '\\':
            first = False
            continue

        if char == '\\':
            if final_value_being_read:
                break
            if not reading_value:
                if last_key == key:
                    key_found = True
            else:
                last_key = ""
            reading_value = not reading_value
        elif not reading_value:
            last_key += char
        elif final_value_being_read:
            value += char
'''


def red_to_white_text(text):
    if not text or len(text) == 0:
        return text

    text_list = list(text)
    converted_text = ""

    for char in text_list:
        ascii_number = ord(char)
        converted = False
        if 18 <= ascii_number <= 27:
            converted = True
            converted_text += chr(ascii_number + 30)
        # Yellow numbers
        elif 146 <= ascii_number <= 155:
            converted = True
            converted_text += chr(ascii_number - 98)
        # Remove the highest bit in the byte which makes the text red
        elif ascii_number & 0b10000000:
            converted = True
            ascii_number &= ~128
            converted_text += chr(ascii_number)
        if ((0 <= ascii_number <= 31) or (127 <= ascii_number <= 159)) and not converted:
            converted = True
            converted_text += ""
        if not converted:
            converted_text += char

    return converted_text
