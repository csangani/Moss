###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  Library to manage log
##
##  Changelog:
##
##  1/14/2014:	Created
##		Chirag Sangani (csangani@stanford.edu)
##
###############################################################################

###############################################################################
##
##	DO NOT EDIT BELOW THIS LINE
##
###############################################################################

import sys, linecache

##
## Print and store log
##
## params:
## 	ex: Exception
## 		Exception object
## returns: Dict()
def printLog(ex):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)

    message = 'Error in {}, line {}: {}\n\t{}'.format(filename, lineno, line.strip(), exc_obj)
    log = open('moss.log', 'w')
    log.write(message)
    log.close()
    print message
    print '\nSaved to moss.log'
