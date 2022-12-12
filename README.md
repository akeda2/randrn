# randrn
Random name renamer

## Usage:
```
randrn -h
usage: randrn [-h] [-a] [-S] [-s SUFFIX] [-d] [-R] [-n] [wildcard]

randrn - rename files with random names

positional arguments:
  wildcard              A wildcard pattern to match filenames (default: *)

options:
  -h, --help            show this help message and exit
  -a, --auto            Auto rename only filenames with non alphanumerical characters (default: False)
  -S, --strip           Strip mode: Just strip away non alphanumerical characters (default: False)
  -s SUFFIX, --suffix SUFFIX
                        Suffix to set for new filename (default: False)
  -d, --dir             Also rename directories (default: False)
  -R, --recursive       Recursive mode (default: False)
  -n, --now             Use datetime NOW iso mtime (default: False)
```
