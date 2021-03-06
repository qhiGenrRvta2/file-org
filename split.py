#!/usr/bin/env python3
"""
Organizes files into subfolders.
"""
import math
import os
import re
import shutil

def main():
    """
    Divides big group of files into folders
    """
    size = 200

    # Get list of files having the expected filename format.
    pwd = os.getcwd()

    # r means "treat this as a raw string".
    name_format = re.compile(r'[A-Z]{3}\d{4,5}\.[a-zA-z]+')
    file_list = [entry for entry in os.listdir(pwd) if re.search(name_format, entry)]

    photo_dirs = generate_folder_names(file_list, size)

    # Check if directories exist; if not, create them.
    # Move files home.
    for folder in photo_dirs:

        tmp_path = os.path.join(os.getcwd(), folder)

        if not os.path.isdir(tmp_path):
            os.mkdir(tmp_path)

        start = int(folder.split('-')[0])
        # Add 1 to the end position because 'range' is not inclusive!
        end = int(folder.split('-')[1]) + 1

        for entry in file_list:
            # Move files into directories.
            if int(re.findall(r'\d+', entry)[0]) in range(start, end):
                # https://docs.python.org/3/library/shutil.html
                print(f"putting {entry} into {folder}")
                shutil.move(os.path.join(os.getcwd(), entry), tmp_path)


def generate_folder_names(file_list, size):
    """
    Generate a list of suitable folder names.
    """
    # Number parts of file names.
    file_numbers = [int(re.findall(r'\d+', entry)[0]) for entry in file_list]

    # Get lowest file number.
    # Logic from https://stackoverflow.com/questions/9810391/round-to-the-nearest-500-python
    range_bottom = math.floor(min(file_numbers) / 200) * 200

    # Highest numbered file
    highest_file_number = max(file_numbers)
    # Temporary list for storing which file we are looking at.
    new_directory_ends = []

    # First directory
    position = range_bottom + size

    # Identify any further directories.
    tracker = True
    while tracker or not new_directory_ends:
        if position > highest_file_number:
            tracker = False
        new_directory_ends.append(position)
        position += size

    # Generate list of directors needed.
    photo_dirs = [f"{entry-size}-{entry-1}" for entry in new_directory_ends]

    return photo_dirs


if __name__ == '__main__':
    main()
