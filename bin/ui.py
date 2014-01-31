###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  UI library
##
##  Changelog:
##
##  1/11/2014:	Created
##		Chirag Sangani (csangani@stanford.edu)
##
###############################################################################

###############################################################################
##
##	DO NOT EDIT BELOW THIS LINE
##
###############################################################################

##
## Ask a question
##
## params:
##	question: String
##
## returns: String
def askQuestion(question):
    try:
        return raw_input('{}\n'.format(question))
    finally:
        print

##
## Return a formatted version of an item in a list
##
## params:
##	num: Integer
##		Index of item in list
##	item: String
##
## returns: String
def createListItem(num, item):
    return '   [{}]\t{}'.format(num, item)

##
## Show CUI for selecting an item from a list
##
## params:
##	prompt: String
##		Prompt to show above list
##	options: List(String)
##		List options
##	custom = False: Boolean
##		Allow custom options?
##
## returns: String
def selectOption(prompt, options, custom = False, transform = None):
    try:
        print prompt
        for o in options:
            print createListItem(options.index(o), o if transform is None else transform(o))
        if custom:
            print createListItem(len(options), 'Other')
        while True:
            index = raw_input('Choose index: ')
	    try:
    	        if int(index) == len(options) and custom:
	            return raw_input('Specify: ')
                return options[int(index)]
            except:
	        print 'Invalid index!'
    finally:
        print
