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

home = os.path.expanduser("~")
mainFolder = os.path.join(home,".passwd-files")
if not os.path.exists(mainFolder):
    os.mkdir(mainFolder)

parser = argparse.ArgumentParser(
        prog="createPasswdFile",
        description="Creates a password file according to Basic WWW-Authenticationi Scheme RFC 7617",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument(
  "--path",
  "-p",
  metavar="PATH",
  default=os.path.join(mainFolder,"http-secure.passwd"),
  help="specify password file path")

args = parser.parse_args()
username = input("Type username: ")

if username == '':
    print("User can't be empty!")
    sys.exit()

password = getpass.getpass("Type password: ")
if password == '':
    print("Password can't be empty!")
    sys.exit()

text = base64.b64encode(f"{username}:{password}".encode()).decode()
path = args.path
if '.passwd' not in args.path:
    path = path+'.passwd'

f = open(path,'w')
f.write(text)
f.close()

print("Password file created at "+path+'.')
