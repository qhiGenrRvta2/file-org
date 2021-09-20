#!/usr/bin/env python3

import math
import os
import re

def main():
    """
    """
    size = 200

    # Get list of files having the expected filename format.
    pwd = os.getcwd()
    
    # r means "treat this as a raw string".
    name_format = re.compile(r'[A-Z]{3}\d{4,5}\.[a-zA-z]+')
    file_list = [entry for entry in os.listdir(pwd) if re.search(name_format, entry)]
   
    # Number parts of file names.
    file_numbers = [int(re.findall('\d+', entry)[0]) for entry in file_list] 

    # Get lowest file number.
    # Logic from https://stackoverflow.com/questions/9810391/round-to-the-nearest-500-python
    range_bottom = math.floor(min(file_numbers) / 200) * 200 
    
    # Highest numbered file
    highest_file_number = max(file_numbers)

    # Temporary list for storing which file we are looking at.
    new_directory_ends = []
   
    # First directory
    position = range_bottom + size

    # Any more directories to create? 'not' test ensures at least the start position gets onto our list.
    while position <= highest_file_number or not new_directory_ends:
        new_directory_ends.append(position)
        position += size 
   
    photo_dirs = [f"{entry-size}-{entry-1}" for entry in new_directory_ends]
    
    # check if directories exist; if not, create them.
    for folder in photo_dirs:
        tmp_path = os.path.join(os.getcwd(), folder)
        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)

if __name__ == '__main__':
    main()
