#!/usr/bin/python3
import os
import sys
import random
import string
import datetime
import glob
import argparse

# USAGE:
# randrn.py wildcard -s .suffix
# Example:
# randrn.py glenn* -s .mp4
# Don't forget the "." in the suffix!
# Also: If you don't use a wildcard, you can't use a suffix!
parser = argparse.ArgumentParser(description="randrn - rename files with random names",
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
#parser.add_argument('file', default=None, nargs='?', type=argparse.FileType('w'), help="Filename. If omitted, all files in current directory will be selected. Add wildcard.")
parser.add_argument('wildcard', nargs='?', default='*', help='A wildcard pattern to match filenames')
parser.add_argument("-s", "--suffix", default=False, type=str, help="Suffix to set for new filename")
parser.add_argument("-d", "--dir", default=False, action="store_true", help="Also rename directories")
parser.add_argument("-R", "--recursive", default=False, action="store_true", help="Recursive mode")
parser.add_argument("-n", "--nonrec", default=False, action="store_true", help="Testing...")
args = parser.parse_args()
config = vars(args)

# #if len(sys.argv) < 2:
# if not args.wildcard:
# # Get the current working directory
#     directory = os.getcwd()
# # Get a list of all the files in the directory
#     files = os.listdir(directory)
#     suff = False
# else:
# Use glob to find all files that match the wildcard pattern in the current directory
    #pattern = glob.escape(sys.argv[1])
#    pattern = sys.argv[1]

pattern = args.wildcard
files = glob.glob(pattern)
print("Pattern:", pattern)

#if len(sys.argv) > 2:
# if args.suffix:
#     suff = args.suffix
#     #suff = sys.argv[2]
# else:
#     suff = False
if 1 == 0: #not args.recursive:
    print("Files:", files)
    # Iterate over the files
    for file in files:
        if os.path.isfile(file):
            # Split the file name and the suffix
            file_name, file_suffix = os.path.splitext(file)

            # Generate a random name
            new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))

            # Get the current date and time
            date_time = datetime.datetime.now()

            # Format the date and time in the desired way
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')

            # Join the date and time, the random name, and the file suffix
            # Did we give a suffix at the command line?
            if args.suffix:
                file_suffix = args.suffix
            new_file = date_time_str + '_' + new_name + file_suffix

            # Get the directory name of the file
            directory = os.path.dirname(file)

            # Rename the file
            print("Renaming:", directory,file, "to:", directory, new_file)
            os.rename(os.path.join(directory, file), os.path.join(directory, new_file))

        elif args.dir and os.path.isdir(file):
            #file_name, file_suffix = os.path.splitext(file)
            new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
            date_time = datetime.datetime.now()
            date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
            
            new_file = date_time_str + '_' + new_name
            #directory = os.path.dirname(file)
            directory = file
            # Rename the file
            print("Renaming:", directory, "to:", new_file)
            os.rename(directory, new_file)
else:# args.recursive:
    root_dir = os.getcwd()
    # Iterate over the directory tree using os.walk()
    if args.recursive:
        rtopdown = False
    else:
        rtopdown = True

    for root, dirs, files in os.walk(root_dir, topdown=not args.recursive):
        
        if not args.recursive: #args.nonrec:
            dirs.clear()
        # Use glob to generate a list of files that match the wildcard pattern
        wildcard_files = glob.glob(os.path.join(root, args.wildcard))
        
        # Iterate over the list of files
        for file in wildcard_files:
            if os.path.isfile(file):
                # Split the file name and the suffix
                file_name, file_suffix = os.path.splitext(file)
                # Generate a random name
                new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
                # Get the current date and time
                date_time = datetime.datetime.now()
                # Format the date and time in the desired way
                date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
                # Join the date and time, the random name, and the file suffix
                # Did we give a suffix at the command line?
                if args.suffix:
                    file_suffix = args.suffix
                new_file = date_time_str + '_' + new_name + file_suffix
                # Get the directory name of the file
                directory = os.path.dirname(file)
                # Rename the file
                print("Renaming:", file, "to:", directory, new_file)
                os.rename(os.path.join(directory, file), os.path.join(directory, new_file))
        if args.dir:
            for dir in dirs:
                new_name = ''.join(random.choices(string.ascii_lowercase + string.digits, k=24))
                date_time = datetime.datetime.now()
                date_time_str = date_time.strftime('%Y-%m-%d_%H-%M-%S')
                
                new_file = date_time_str + '_' + new_name
                #directory = os.path.dirname(file)
                directory = dir
                # Rename the file
                print("Renaming:", directory, "to:", new_file)
                os.rename(directory, new_file)
        if not args.recursive:
            #for dir in dirs:
            break;