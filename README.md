# randrn
Random name renamer
#### Use-case #1:
You have an amount of files with garbled names. Use this to rename files to more easy to maintain names:
By default, including:
- Modyfied date and time
- Counting from 0001 to 9999, sorted by modyfied date/time
- 16 alphanumerical random characters
- Original extension or one by your choice

#### Example:
```
$ randrn *.txt
'Some file name with &%¤# in it.txt' --> 2022-12-12_09-49-45_0001_cya5x6mk6spb19tt.txt
```
#### Use-case #2:
You have an amount of files with non alphanumerical characters in the file name - garbage filenames:
- Use "-a or --auto": Only renames files which actually have garbage in the filenames.
- Use "-S or --strip": Only strips out garbage and replaces it with alphanumerical randomness.

#### Example of --strip:
```
$ randrn --strip Some*
'Some file name with &%¤# in it.txt' --> Some_kiflx11hfile_kiflx11hname_kiflx11hwith_kiflx11hin_kiflx11hit.txt
(this will probably change into something more useful...)
```
## Usage:
```
randrn -h
usage: randrn [-h] [-a] [-S] [-e EXTENSION] [-d] [-R] [-n] [wildcard]

randrn - rename files with random names

positional arguments:
  wildcard              A wildcard pattern to match filenames (default: *)

options:
  -h, --help            show this help message and exit
  -a, --auto            Auto rename only filenames with non alphanumerical characters (default: False)
  -S, --strip           Strip mode: Just strip away non alphanumerical characters (default: False)
  -e EXTENSION, --extension EXTENSION
                        Extension to set for new filename (default: False)
  -d, --dir             Also rename directories (default: False)
  -R, --recursive       Recursive mode (default: False)
  -n, --now             Use datetime NOW iso mtime (default: False)
```
