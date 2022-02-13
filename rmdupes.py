#/usr/bin/env python3

import copy
import hashlib
import os
import re

import rich.console

class Entry():
    """
    Stores file path and hash.
    https://docs.python.org/3/library/hashlib.html
    """
    def __init__(self, path):
        self.path = path
        with open(self.path, 'rb') as curr_file:
            self.hash = hashlib.md5(curr_file.read()).hexdigest()

    def is_copy(self):
        """
        Does the filename suggest this file is a copy?
        """
        if re.match(r'\s{1}[0-9]\.[a-zA-Z]{3,4}$', self.path):
            return True
        return False

    def remove(self):
        print(f'Deleting {self.path} !')
        #os.remove(self.path)


class Content():
    """
    Represents contents of a folder and its subfolders
    """
    def __init__(self, dir_path):
        self.files = []
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

def main():
    
    target = os.getcwd()
    console = rich.console.Console(highlight=False)
    with console.status(status='Searching for duplicate files...'):
        con = Content(target)
        print(con.find_groups())

if __name__ == '__main__':
    main()
