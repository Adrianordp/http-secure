#!/bin/python3

# Based on https://gist.github.com/fxsjy/5465353
# and on https://gist.github.com/epiasini/60012a7a245f5fd8980fcc1a5c3c8085

# HELP:
# usage: http-secure.py [-h] [--cgi] [--bind ADDRESS] [--directory DIRECTORY] [--password-file PASSWORDFIlE] [port]
#
# Opens a python3 http.server protected by a password file from passwd2file.py
#
# positional arguments:
#   port                   Specify alternate port [default: 8000]
# 
# optional arguments:
#   -h, --help             show this help message and exit
#   --cgi                  Run as CGI Server
# 
#   --bind ADDRESS,
#    -b ADDRESS            Specify alternate bind address [default: all interfaces]
#   --directory DIRECTORY,
#    -d DIRECTORY          Specify alternative directory [default:current directory]
#
#   --password-file PASSWORDFIlE,
#    -f PASSWORDFIlE

# EXAMPLE:
# python3 http-secure.py -d /home/ -b 0.0.0.0 -f /home/$MYUSER/.passwd-files/http-secure.passwd

#***********************************************
#          !!! WARNING SECTION !!!
#
# TO RUN THIS APPLICATION YOU'LL NEED A PASSWORD
# FILE GENERATED VIA python3 passwd2file.py 
# 
#***********************************************

from functools import partial
from http.server import SimpleHTTPRequestHandler, test
import base64
import os


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    """ Main class to present webpages and authentication. """

    def __init__(self, *args, **kwargs):
        passwordFilePath = kwargs.pop("password_file")
        passwordFile     = open(passwordFilePath, 'r')
        self._auth       = passwordFile.read()
        super().__init__(*args, **kwargs)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_AUTHHEAD(self):
        self.send_response(401)
        self.send_header("WWW-Authenticate", 'Basic realm="Test"')
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """ Present frontpage with user authentication. """
        if self.headers.get("Authorization") == None:
            self.do_AUTHHEAD()
            self.wfile.write(b"no auth header received")
        elif self.headers.get("Authorization") == "Basic " + self._auth:
            SimpleHTTPRequestHandler.do_GET(self)
        else:
            self.do_AUTHHEAD()
            self.wfile.write(self.headers.get("Authorization").encode())
            self.wfile.write(b"not authenticated")

if __name__ == "__main__":
    import argparse

    # Parser basic configuration
    parser = argparse.ArgumentParser(
            description="Opens a python3 http.server protected by a password file from passwd2file.py",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    # CGI argument
    parser.add_argument("--cgi", action="store_true", help="Run as CGI Server")
    parser.add_argument(
        "--bind",
        "-b",
        metavar="ADDRESS",
        default="127.0.0.1",
        help="Specify alternate bind address ",
    )
    # Directory argument
    parser.add_argument(
        "--directory",
        "-d",
        default=os.getcwd(),
        help="Specify alternative directory ",
    )
    # Port argument
    parser.add_argument(
        "port",
        action="store",
        default=8000,
        type=int,
        nargs="?",
        help="Specify alternate port",
    )
    
    # Store user home folder path
    home = os.path.expanduser("~")
    # Store default password files path
    mainFolder = os.path.join(home,".passwd-files")
    # Password file path argument
    parser.add_argument(
            "--password-file", "-f",
            metavar="PASSWORDFIlE",
            default=os.path.join(mainFolder,'http-secure.passwd'),
            help="Specify password file path")

    # Get arguments
    args = parser.parse_args()

    # Pass arguments to AuthHTTPRequestHandler class
    handler_class = partial(
        AuthHTTPRequestHandler,
        password_file=args.password_file,
        directory=args.directory,
    )
    test(HandlerClass=handler_class, port=args.port, bind=args.bind)