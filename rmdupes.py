#!/usr/bin/env python3
"""
Script for detecting and removing duplicate files.
"""

import copy
import hashlib
import os
import re

import rich.console
import rich.prompt

class Entry():
    """
    Stores file path and hash.
    https://docs.python.org/3/library/hashlib.html
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as curr_file:
            self.hash = hashlib.md5(curr_file.read()).hexdigest()

    def move_to_dir(self, new_dir):
        """
        Moves file to new_dir
        """
        filename = os.path.basename(self.path)
        new_path = os.path.join(new_dir, self.path)
        os.replace(self.path, new_path)
        self.path = new_path

    def is_whatsapp_img(self):
        if re.match(os.path.basename(self.path), r'[A-Z]{4}\d{4}\.[A-Z]{3,4}'):
            return True
        return False

    def remove(self):
        """
        Deletes file.
        """
        print(f'Deleting {self.path}...')
        os.remove(self.path)

    def __str__(self):
        return f'{self.path} : hash {self.hash}'


class Content():
    """
    Represents contents of a folder and its subfolders
    """
    def __init__(self, dir_path):
        self.files = []
        self.start_dir = dir_path
        frontier = []
        elements = os.listdir(dir_path)

        for element in elements:
            p = os.path.join(dir_path, element)
            if os.path.isdir(p):
                frontier.append(p)
            else:
                self.files.append(Entry(p))

        while frontier:
            current_dir = frontier.pop()
            elements = os.listdir(current_dir)
            for element in elements:
                p = os.path.join(current_dir, element)
                if os.path.isdir(p):
                    frontier.append(p)
                else:
                    self.files.append(Entry(p))

        self.dupe_groups = self.find_groups()

    def find_groups(self):
        """
        Identify groups of duplicates.
        """
        dupe_groups = []
        # make a copy of the files list.
        fcopy = copy.deepcopy(self.files)
        # construct groups of identical files.
        while len(fcopy) > 0:
            curr = fcopy.pop()
            tmp = []
            tmp.append(curr)
            tmp += [x for x in fcopy if x.hash == curr.hash]
            if len(tmp) > 1:
                dupe_groups.append(tmp)
                discards = [x for x in fcopy if x in tmp]
                for x in discards:
                    fcopy.remove(x)
        return dupe_groups

    def propose_removals(self):
        """
        Prints groups of files.  Proposes files for deletion.
        """
        for i in range(len(self.dupe_groups)):
            print(f'Group {i+1} of {len(self.dupe_groups)}:')
            group = self.dupe_groups[i]
            group.sort(key=lambda x: x.path, reverse=True)
            for e in group:
                print(f'\t{e}')
            print('The following will be removed:')
            print(f'\t{[str(x) for x in group[1:]]}')

    def remove_dupes(self):
        """
        Removes duplicate files.
        """
        removals = []

        for group in self.dupe_groups:
            group.sort(key=lambda x: x.path, reverse=True)
            removals += group[1:]

        for removal in removals:
            removal.remove()

    def organize_whatsapp_pics(self):
        """
        Moves whatsapp pics to a subfolder.
        """
        # TODO: create subfolder.
        # Entry class already contains helper functions for moving files around
        pass

def main():
    """
    Provides CLI.
    """
    target = os.getcwd()
    console = rich.console.Console(highlight=False)
    with console.status(status='Searching for duplicate files...'):
        con = Content(target)
        con.propose_removals()

    proceed_to_del = rich.prompt.Confirm.ask('Delete files?')
    if proceed_to_del:
        con.remove_dupes()

    proceed_to_move = rich.prompt.Confirm.ask('Move whatsapp pics?')
    if proceed_to_move:
        con.organize_whatsapp_pics()

if __name__ == '__main__':
    main()
