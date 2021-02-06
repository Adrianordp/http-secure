#!/usr/bin/python3

# HELP:
# usage: createPasswdFile [-h] [--path PATH]
# Creates a password file according to Basic WWW-Authenticationi Scheme RFC 7617
#
# optional arguments:
#   -h, --help            show this help message and exit
#   --path PATH, -p PATH  specify password file path (default: /home/$USER/.passwd-files/http-secure.passwd)


# Example:
#   input (--path is optional):
#
#     python3 createPasswdFile.py --path [path-to-file]
#
#   output:
#     Type username: [username]
#     Type password: [********]
#     Password file created at [path-to-file]

import os
import base64
import hashlib
import argparse
import sys
import getpass

# Get user home folder path
home = os.path.expanduser("~")
# Create folder to store generated password files
mainFolder = os.path.join(home,".passwd-files")
if not os.path.exists(mainFolder):
    os.mkdir(mainFolder)

# Parser basic configurations
parser = argparse.ArgumentParser(
        prog="createPasswdFile",
        description="Creates a password file according to Basic WWW-Authenticationi Scheme RFC 7617",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

# Path argument
parser.add_argument(
  "--path",
  "-p",
  metavar="PATH",
  default=os.path.join(mainFolder,"http-secure.passwd"),
  help="specify password file path")

# Get arguments
args = parser.parse_args()

# Wait for user to input desired username
username = input("Type username: ")
# Abort if empty
if username == '':
    print("User can't be empty!")
    sys.exit()

# Wait for user to input desired password
password = getpass.getpass("Type password: ")
# Abort if empty
if password == '':
    print("Password can't be empty!")
    sys.exit()

# Enconde on base 64
text = base64.b64encode(f"{username}:{password}".encode()).decode()

# Improve path parser to avoid naming folders as files
path = args.path
if os.path.isdir(path):
    path = os.path.join(path, "http-secure.passwd")
elif '.passwd' not in args.path:
    path = path+'.passwd'

# Create the password file with generated hash
f = open(path,'w')
f.write(text)
f.close()

# Feedbacks to user where the file was created
print("Password file created at "+path)
