#!/usr/bin/python3
import os
import sys
import random
import string
import datetime
import glob
import argparse
import re

parser = argparse.ArgumentParser(description="randrn - rename files with random names",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('file', default=None, nargs='?', type=argparse.FileType('w'), help="Filename. If omitted, all files in current directory will be selected. Add wildcard.")
parser.add_argument('wildcard', nargs='?', default='*', help='A wildcard pattern to match filenames')
parser.add_argument("-a", "--auto", default=False, action="store_true", help="Auto rename only filenames with non alphanumerical characters")
parser.add_argument("-S", "--strip", default=False, action="store_true", help="Strip mode: Just strip away non alphanumerical characters")
parser.add_argument("-e", "--extension", default=False, type=str, help="Extension to set for new filename")
parser.add_argument("-d", "--dir", default=False, action="store_true", help="Also rename directories")
parser.add_argument("-R", "--recursive", default=False, action="store_true", help="Recursive mode")
#parser.add_argument("-n", "--nonrec", default=False, action="store_true", help="Testing...")
parser.add_argument("-n", "--now", default=False, action="store_true", help="Use datetime NOW iso mtime")
args = parser.parse_args()
config = vars(args)
if args.strip:
    args.auto = True
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
    wildcard_files.sort(key=lambda x: os.path.getmtime(x))
    # Iterate over the list of files:
    i=0
    for file in wildcard_files:
        i+=1
        if args.auto and not nonalphanum(os.path.split(file)[1]):
            print("Not renaming:", file)
            continue
        if os.path.isfile(file):
            # Split the file name and the suffix:
            file_name, file_extension = os.path.splitext(file)

            # Strip mode?:
            if args.strip and nonalphanum(os.path.split(file)[1]):
                print("Strip:", os.path.split(file)[1])
                # First, strip all whitespace and replace with underscore:
                new_name = re.sub(r'\s+', '_', os.path.split(file_name)[1])
                # Then, strip all other garbage and replace with randomness:
                new_name = re.sub('[^0-9a-zA-Z\-._]+', '_'+''.join(random.choices(string.ascii_lowercase + string.digits, k=2)), new_name)
                if len(new_name) < 1:
                    new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            # Or generate a random name:
            else:
                new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))

            # Get the current date and time OR mtime from file?:
            if args.now:
                date_time = datetime.datetime.now()
            else:
                file_date_time = os.path.getmtime(file)
                date_time = datetime.datetime.fromtimestamp(file_date_time)

            # Format the date and time in the desired way
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')

            # Join the date and time, the random name, and the file suffix
            # Did we give a suffix at the command line?
            if args.extension:
                # Checking for ".":
                if not args.extension.startswith('.'):
                    file_extension = '.'+ args.extension
                else:
                    file_extension = args.extension
            if not args.strip:
                new_file = date_time_str + '_' + f"{i:04d}" +'_'+ new_name + file_extension
            else:
                new_file = new_name + file_extension
            
            # Get the directory name of the file
            directory = os.path.dirname(file)
            
            # Actually enaming the file:
            print("Renaming:", file, "to:", new_file)
            try:
                os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
            except OSError as exc:
                print("ERROR")
                if exc.errno == 36:
                    try:
                        os.rename(os.path.basename(file), new_file)
                    except:
                        print("FAILED")
                        raise
    if args.dir:
        for dir in dirs:
            # Auto mode?:
            if args.auto and not nonalphanum(dir):
                print("Not ranaming:", dir)
                continue
            
            # Strip mode?:
            if args.strip and nonalphanum(dir):
                print("Strip:", os.path.split(file)[1])
                new_name = re.sub('[^0-9a-zA-Z\-._]+', ''.join(random.choices(string.ascii_lowercase + string.digits, k=8)), os.path.split(file_name)[1])
                if len(new_name) < 1:
                    new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            # Or generate a random name:
            else:
                new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=16))
            
            if args.now:
                date_time = datetime.datetime.now()
            else:
                file_date_time = os.path.getmtime(dir)
                date_time = datetime.datetime.fromtimestamp(file_date_time)
            
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            if args.strip:
                new_file = new_name
            else:
                new_file = date_time_str + '_' + new_name
            directory = dir

            # Actually renaming the dir:
            print("Renaming:", directory, "to:", new_file)
            os.rename(directory, new_file)
            if not args.recursive:
                break
    if not args.recursive:
        break;