#!/usr/bin/env python3

import collections
import os
import hashlib

def main():
    """
    Identifies duplicate files within a directory.  
    """
    # TODO: accept command line argument specifying a path to look in. 
    start_directory = os.getcwd()
    files = get_files(start_directory)
    # TODO: find files with matching hashes
    # https://stackoverflow.com/questions/20462868/how-to-find-duplicate-values-in-dictionaries


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

if __name__=="__main__":
    main()
