#!/usr/bin/python3
import os
import sys
import random
import string
import datetime
import glob
import argparse
import re

# USAGE:
# randrn.py wildcard -s .suffix
# Example:
# randrn.py glenn* -s .mp4
# Don't forget the "." in the suffix!

parser = argparse.ArgumentParser(description="randrn - rename files with random names",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('file', default=None, nargs='?', type=argparse.FileType('w'), help="Filename. If omitted, all files in current directory will be selected. Add wildcard.")
parser.add_argument('wildcard', nargs='?', default='*', help='A wildcard pattern to match filenames')
parser.add_argument("-a", "--auto", default=False, action="store_true", help="Auto rename only filenames with non alphanumerical characters")
parser.add_argument("strip", default=False, action="store_true", help="Strip mode: Just strip away non alphanumerical characters")
parser.add_argument("-s", "--suffix", default=False, type=str, help="Suffix to set for new filename")
parser.add_argument("-d", "--dir", default=False, action="store_true", help="Also rename directories")
parser.add_argument("-R", "--recursive", default=False, action="store_true", help="Recursive mode")
#parser.add_argument("-n", "--nonrec", default=False, action="store_true", help="Testing...")
parser.add_argument("-n", "--now", default=False, action="store_true", help="Use datetime NOW iso mtime")
args = parser.parse_args()
config = vars(args)

# Use glob to find all files that match the wildcard pattern in the current directory
pattern = args.wildcard
files = glob.glob(pattern)
print("Pattern:", pattern)

def nonalphanum(s):
    #return bool(re.search(r'[^a-zå-öA-ZÅ-Ö0-9]', s))
    #pattern = re.compile(r'[^\w]|[^a-zA-ZåäöÅÄÖ]', flags=re.UNICODE)
    pattern = re.compile(r'[^a-zA-Z0-9åäöÅÄÖ\-._]', flags=re.UNICODE)
    return bool(pattern.search(s))

root_dir = os.getcwd()
# Iterate over the directory tree using os.walk()
for root, dirs, files in os.walk(root_dir, topdown=not args.recursive):
    
    # If we don't want to go into subdirs, clear dirs.
    # if not args.recursive:
    #     dirs.clear()    

    # Use glob to generate a list of files that match the wildcard pattern
    wildcard_files = glob.glob(os.path.join(root, args.wildcard))
    
    # Iterate over the list of files
    for file in wildcard_files:
        if args.auto and not nonalphanum(os.path.split(file)[1]):
            print("Not renaming:", file)
            continue
        if os.path.isfile(file):
            # Split the file name and the suffix
            file_name, file_suffix = os.path.splitext(file)

            # Generate a random name
            new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))

            # Get the current date and time
            if args.now:
                date_time = datetime.datetime.now()
            else:
                file_date_time = os.path.getmtime(file)
                date_time = datetime.datetime.fromtimestamp(file_date_time)

            # Format the date and time in the desired way
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')

            # Join the date and time, the random name, and the file suffix
            # Did we give a suffix at the command line?
            if args.suffix:
                # Checking for ".":
                if not str.startswith(".", args.suffix):
                    file_suffix = "."+ args.suffix
                else:
                    file_suffix = args.suffix
            new_file = date_time_str + '_' + new_name + file_suffix
            
            # Get the directory name of the file
            directory = os.path.dirname(file)
            
            # Rename the file
            if args.strip and not len(str(os.path.split(file)[1])) < 1:
                new_file = re.sub('[^0-9a-zA-Z]+', '', os.path.split(file)[1])
            print("Renaming:", file, "to:", new_file)
            os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
    if args.dir:
        for dir in dirs:
            if args.auto and not nonalphanum(dir):
                print("Not ranaming:", dir)
                continue
            new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
            
            if args.now:
                date_time = datetime.datetime.now()
            else:
                file_date_time = os.path.getmtime(dir)
                date_time = datetime.datetime.fromtimestamp(file_date_time)
            
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            new_file = date_time_str + '_' + new_name
            directory = dir
            # Rename the file
            print("Renaming:", directory, "to:", new_file)
            os.rename(directory, new_file)
            if not args.recursive:
                break
    if not args.recursive:
        break;