###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  Utility script to run MOSS on submission archives
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

import os, glob, subprocess, ui, settings as st, moss

def selectFileExtensions(lang):
    newList = []
    if lang in languages:
        rawList = raw_input('Files that match the following patterns will be included: {}. Provide a comma-separated list of additional patterns, if any (e.g. *.h,*.cpp): '.format(repr(languages[lang])))
	newList = languages[lang] + [s.strip() for s in rawList.split(',') if s.strip() != '']
    else:
        rawList = raw_input('Provide a comma separated list of file patterns to include (e.g. *.h,*.cpp, default: *): ')
	newList = [s.strip() for s in rawList.split(',') if s.strip() != '']
    if len(newList) == 0:
        newList += ['*']
    return newList

def selectSubmissionsRootDir():
    rootDir = os.path.realpath('.')
    newRootDir = raw_input('Provide the path to the root directory where all the current submissions are stored. This directory should have all submissions stored separately in their respective directories each with the name format <SUnetID>_<submissionNumber> (default: .): ')
    if newRootDir == '':
        return rootDir
    while not os.path.isdir(newRootDir):
        newRootDir = raw_input('That directory does not exist! Provide a path to a valid directory: ')
    return os.path.realpath(newRootDir)

def archive(archivePath, courseNumber, assignmentName, quarterNumber, language, extensions, submissionsRootDir):
    
    print 'Archive Path:', archivePath
    print 'Course Number:', courseNumber
    print 'Assignment Name:', assignmentName
    print 'Quarter Number:', quarterNumber
    print 'Language:', language
    print 'File extensions:', extensions
    print 'Submissions Directory:', submissionsRootDir

    print

    assert(language is not None)
    assert(len(extensions) != 0)
    assert(submissionsRootDir is not None)

    destinationDir = '{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, quarterNumber)

    # Copy files
    print 'Copying files...'

    command = 'rsync -a --include="*/" ' + ' '.join(['--include="{}"'.format(e) for e in extensions]) + ' --exclude="*" {}/ {}'.format(submissionsRootDir, destinationDir)
    subprocess.call(command, shell = True)

    # Retain only the last submissions for each SUID
    print 'Deleting old submissions...'

    util.retainLast(destinationDir)

    # Flatten all submission directories
    print 'Flattening submission directories...'

    for d in os.listdir(destinationDir):
        if os.path.isdir('{}/{}'.format(destinationDir, d)):
            util.flattenDir('{}/{}'.format(destinationDir, d))

    # Convert all files to ASCII
    print 'Converting files to ASCII...'

    for e in extensions:
        command = 'find -wholename "{}/{}" '.format(destinationDir, e) + '-exec recode -f ..ASCII {} \\;'
	subprocess.call(command, shell = True)

    # Convert all line endings to LF
    print 'Converting line endings...'

    for e in extensions:
        command = 'find -wholename "{}/{}" '.format(destinationDir, e) + '-exec perl -pi -e \'s/\\r\\n|\\n|\\r/\\n/g\' {} \\;'
        subprocess.call(command, shell = True)
	
    # Merge retakes
    print 'Merge retakes...'
    
    util.mergeRetakes('{}/{}/{}'.format(archivePath, courseNumber, assignmentName), verbose = True)

def createListItem(num, item):
    return '   [{}]\t{}'.format(num, item)

def selectOption(prompt, options, custom = False):
    print prompt
    for o in options:
        print createListItem(options.index(o), o)
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

def printLog(msg):
    log = open('moss.log', 'w')
    log.write(msg)
    log.close()
    print '\nError:\n{}'.format(msg)
    print '\nSaved to moss.log'

if __name__ == '__main__':
    try:
    	print banner

        archivePath = None
	courseNumber = None
	quarterNumber = None
	assignmentName = None

        archivePath = os.path.realpath('{}/../archives'.format(scriptPath))

    	# Check whether base path to archives exists
	archivePath = checkArchivePath(archivePath)
	
    	# Obtain course number
        courseNumber = selectOption('Select a course:', os.listdir(archivePath), True)

        if not os.path.isdir('{}/{}'.format(archivePath, courseNumber)):
	    os.makedirs('{}/{}'.format(archivePath, courseNumber))

	print

        # Obtain assignment name
        assignmentName = selectOption('Select an assigment:', os.listdir('{}/{}'.format(archivePath, courseNumber)), True)

	if not os.path.isdir('{}/{}/{}'.format(archivePath, courseNumber, assignmentName)):
	    os.makedirs('{}/{}/{}'.format(archivePath, courseNumber, assignmentName))

	print

	# Obtain quarter number
	quarterNumber = selectOption('Select quarter:',	os.listdir('{}/{}/{}'.format(archivePath, courseNumber,	assignmentName)), True)

	if not os.path.isdir('{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, quarterNumber)):
	    os.makedirs('{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, quarterNumber))

	print

        # Obtain language name
        language = selectOption('Select language:', languages.keys(), True)

	print

	# Obtain additional extensions
	extensions = selectFileExtensions(language)

	print

	# Obtain submissions root directory
        submissionsRootDir = selectSubmissionsRootDir()

	print

        # Archive
	archive(archivePath, courseNumber, assignmentName, quarterNumber, language, extensions, submissionsRootDir)

    except KeyboardInterrupt, SystemExit:
        print '\nCancelled!'
        pass
    except Exception as ex:
        printLog(repr(ex)) 
