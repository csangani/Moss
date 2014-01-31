###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  MOSS client toolkit
##
##  Changelog:
##
##  1/27/2014:	Created
##		Chirag Sangani (csangani@stanford.edu)
##
###############################################################################

server = 'moss.stanford.edu'
port = 7690
userID = 97212303

###############################################################################
##
##	DO NOT EDIT BELOW THIS LINE
##
###############################################################################

import socket, os

##
## Check if a file is binary
##
## params:
##  path: String
##  chunkSize: Integer
##      Size of file head to check for null character
def IsBinary(path, chunkSize = 1024):
    f = open(path, 'rb')
    try:
        while True:
            chunk = f.read(chunkSize)
            if '\0' in chunk:
                return True
            if len(chunk) < chunkSize:
                break
    finally:
        f.close()
    return False

##
## Upload a file
##
## params:
##  socket: Socket
##  name: String
##  ID: Integer
##  path: String
##  lang: String
##  verbose: Boolean
def UploadFile(sock, name, ID, path, lang, verbose = False):
    if not os.path.isfile(path):
        raise Exception("File doesn't exist: {}".format(path))
    size = os.path.getsize(path)
    f = open(path, 'r')
    if verbose: print("Uploading {}...".format(name))
    sock.send("file {} {} {} {}\n".format(ID, lang, size, name))
    for line in f:
        sock.send(line)
    f.close()

##
## Submit job to MOSS
##
## params:
##  files: Map(String, String)
##      A map of file names with the logical path as key and physical path as
##	    value
##  lang: String
##      Language of the job
##  maxMatches: Integer
##      Number of times a code snippet repeats before it is ignored
##  directoryMode: Boolean
##      If True, leaf directories of logical paths are submissions. Else,
##      individual files are submissions
##  experimentalMode: Boolean
##      Run on the experimental version of MOSS
##  comment: String
##      Comment to include in the result
##  showNum: Integer
##      Number of rows in the result
##  baseFiles: List(String)
##      A list of physical file paths that are considered as base files
##  verbose: Boolean
def Submit(files, lang = 'c', maxMatches = 10, directoryMode = False, experimentalMode = False, comment = '', showNum = 250, baseFiles = [], verbose = False):
    
    if verbose: print("Checking files...")
    for f in baseFiles + files.values():
        if IsBinary(f):
            raise Exception("Not a text file: {}".format(f))
    
    if verbose: print("Connecting...")
    sock = socket.create_connection((server, port))
    sock.send("moss {}\n".format(userID))
    sock.send("directory {}\n".format(1 if directoryMode else 0))
    sock.send("X {}\n".format(1 if experimentalMode else 0))
    sock.send("maxmatches {}\n".format(maxMatches))
    sock.send("show {}\n".format(showNum))
    sock.send("language {}\n".format(lang))
    if sock.recv(128).strip() == 'no':
        sock.send("end\n")
        sock.close()
        raise Exception("Unrecognized language: {}".format(lang))
        
    for b in baseFiles:
        UploadFile(sock, b, 0, b, lang, verbose = verbose)
        
    count = 1
    for f in sorted(files.keys()):
        UploadFile(sock, f, count, files[f], lang, verbose = verbose)
        count += 1
        
    if verbose: print("Waiting for response...")
    sock.send("query 0 {}\n".format(comment))
    URL = sock.recv(128).strip()
    sock.send("end\n")
    sock.close()
    if verbose: print("Response: {}".format(URL))
    return URL
