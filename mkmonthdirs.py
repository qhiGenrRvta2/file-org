#!/usr/bin/env python3

import os
import calendar

def main():
    """
    Creates January, February ... December directories.
    """
    months = [calendar.month_name[i] for i in range(1, 13)]

    pwd = os.getcwd()
        
    for month in months:
        month_dir = os.path.isdir(os.path.join(pwd, month))
        if not month_dir: 
            os.mkdir(month_dir)

if __name__=="__main__":
    main()
