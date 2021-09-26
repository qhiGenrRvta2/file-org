#!/usr/bin/env python3

import hashlib
import os
import sys

import rich.console

def main():
    """
    Handles the user interface.
    Main application logic is in the find_duplicates function.
    """

    # Handle command line arguments
    if len(sys.argv) == 2:
        try:
            start_directory = check_input(sys.argv[1])
        except ValueError:
            sys.exit(f"Could not find {sys.argv[1]}")
    elif len(sys.argv) > 2:
        sys.exit("Too many arguments. \n Usage: dedupe.py DIRECTORY")
    else:
        start_directory = os.getcwd()

    print(start_directory)
    # Set up a console for showing progress bar / providing nice output
    console = rich.console.Console(highlight=False)

    # Do the useful stuff.
    with console.status(status="Searching for duplicate files"):
        result = find_duplicates(start_directory, console)

    # Provide output.
    if result == 0:
        console.print("No duplicates found!")

def check_input(argument):
    """
    checks if argument is a valid relative or absolute path
    """
    if os.path.isdir(argument):
        return argument
    elif os.path.isdir(os.path.join(os.getcwd(), argument)):
        return os.path.join(os.getcwd(), argument)
    
    # If we got here, value is bad.
    raise ValueError("invalid path specified")


def find_duplicates(start_directory, output_console):
    """
    Main script logic.
    Searches for and hashes files.
    Identifies duplicates using the hashes.
    Puts lists of duplicates into a buffer for printing.
    """

    files = get_files(start_directory)
    # 'None' means we could not open the file due to a permissions error.
    hash_table = {files[entry]['hash']: [] for entry in files if files[entry]['hash'] is not None}

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
    try:
        with open(my_file, 'rb') as current_file:
            buffered_file = current_file.read()
            hasher = hashlib.md5()
            hasher.update(buffered_file)
    
        return hasher.hexdigest()
    except PermissionError:
        return None
    except FileNotFoundError:
        print(f"{my_file=} does not exist")
        return None

def get_files(start_directory):
    """
    Finds files in a directory (and any sub-directories) by depth-first search.
    """
    results = {entry: {'location': os.path.join(start_directory, entry), 'hash': generate_hash(os.path.join(start_directory, entry))} for entry in os.listdir(start_directory) if not os.path.isdir(os.path.join(start_directory, entry))} 
    # Also need to look in subdirectories. 
    frontier = [os.path.join(start_directory, entry) for entry in os.listdir(start_directory) if os.path.isdir(os.path.join(start_directory, entry))]
    
    while(frontier):
        # Take a subdirectory.
        current_directory = frontier.pop()
        
        # Add any child directories to the frontier. 
        # Try/except block is needed to handle permission errors. Cannot even list the contents of ~/.Trash, apparently.
        try:
            frontier += [os.path.join(current_directory, entry) for entry in os.listdir(current_directory) if os.path.isdir(os.path.join(current_directory, entry))]
        except PermissionError:
            continue

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
