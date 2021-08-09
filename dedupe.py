#!/usr/bin/env python3

import os
import hashlib
import rich.console

def main():
    """
    Handles the user interface.
    Main application logic is in the find_duplicates function.
    """
    # TODO: accept command line argument specifying a path to look in. 
    start_directory = os.getcwd()
    
    # Set up a console for showing progress bar / providing nice output
    console = rich.console.Console(force_terminal=False)

    # Do the useful stuff.
    with console.status(status="Searching for duplicate files"):
        result = find_duplicates(start_directory, console)

    # Provide output.
    if result == 0:
        console.print("No duplicates found!")
    

def find_duplicates(start_directory, output_console):
    """
    Main script logic.
    Searches for and hashes files.
    Identifies duplicates using the hashes.
    Puts lists of duplicates into a buffer for printing.
    """

    files = get_files(start_directory)
    hash_table = {files[entry]['hash']: [] for entry in files}

    for current_file in files:
        hash_table[files[current_file]['hash']].append(files[current_file]['location'])

    group_count = 0

    for element in hash_table:
        if len(hash_table[element]) > 1:
            group_count += 1
            print_group(output_console, group_count, hash_table[element])

    return group_count


def generate_hash(my_file):
    """
    Generates the md5 hash of my_file.
    """
    with open(my_file, 'rb') as current_file:
        buffered_file = current_file.read()
        hasher = hashlib.md5()
        hasher.update(buffered_file)
    
    return hasher.hexdigest()


def get_files(start_directory):
    """
    Finds files in a directory (and any sub-directories) by depth-first search.
    """
    results = {entry: {'location': os.path.join(start_directory, entry), 'hash': generate_hash(entry)} for entry in os.listdir(start_directory) if not os.path.isdir(entry)} 
    # Also need to look in subdirectories. 
    frontier = [os.path.join(start_directory, entry) for entry in os.listdir(start_directory) if os.path.isdir(entry)]
    
    while(frontier):
        # Take a subdirectory.
        current_directory = frontier.pop()
        # Add any child directories to the frontier.
        frontier += [os.path.join(current_directory, entry) for entry in os.listdir(current_directory) if os.path.isdir(entry)]
        # Add any new files to our dictionary.
        new_files = [os.path.join(current_directory, entry) for entry in os.listdir(current_directory) if not os.path.isdir(os.path.join(current_directory, entry))]
        for entry in new_files:
            results[entry] = {'location': entry, 'hash': generate_hash(entry)}
        
    return results

def print_group(console, group_count, group_list):
    """
    Prints out a group of files believed to be duplicates.
    """
    console.print(f"Group {group_count}:")
    for i in range(len(group_list)):
        console.print(f"\t {group_list[i]}")

if __name__=="__main__":
    main()
