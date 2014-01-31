###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  Library to manage settings
##
##  Changelog:
##
##  1/13/2014:	Created
##		Chirag Sangani (csangani@stanford.edu)
##
###############################################################################

###############################################################################
##
##	DO NOT EDIT BELOW THIS LINE
##
###############################################################################

##
## Read settings for directory
##
## params:
## 	path: String
## 		Read settings for this directory
## returns: Dict()
def readSettings(path):
    try:
        f = open('{}/.moss'.format(path))
	a = eval(f.read())
	f.close()
	return a
    except:
        return dict()

##
## Read settings for directory
##
## params:
## 	path: String
## 		Write settings for this directory
##	settings: Dict()
##		Settings for the specified directory
## returns: Boolean
def writeSettings(path, settings):
    try:
        f = open('{}/.moss'.format(path), 'w+')
	f.write(str(settings))
	f.close()
	return True
    except:
        return False
