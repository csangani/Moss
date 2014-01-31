###############################################################################
##   __  __  ___  ____ ____  
##  |  \/  |/ _ \/ ___/ ___| 
##  | |\/| | | | \___ \___ \ 
##  | |  | | |_| |___) |__) |
##  |_|  |_|\___/|____/____/ 
##
##  Utility script to run MOSS or archive submissions
##
##  Changelog:
##
##  1/11/2014:	Created
##		Chirag Sangani (csangani@stanford.edu)
##
###############################################################################

###############################################################################
##
##	CONFIGURABLE PARAMETERS
##
###############################################################################

languages = {
                'cc': ['*.cpp'],
                'java': ['*.java']
            }

archivePath = '/usr/class/cs198/tools/moss/archives'

starterCodePath = '/usr/class/cs198/tools/moss/starterCode'

settingsDescriptions = {}

###############################################################################
##
##	DO NOT EDIT BELOW THIS LINE
##
###############################################################################

import os, glob, subprocess, settings as st, ui, run, archive, log, readline, re

scriptDir = os.path.dirname(os.path.realpath(__file__))

def ListCourses():
    return sorted([d for d in os.listdir(archivePath) if os.path.isdir('{}/{}'.format(archivePath, d))])
    
def ListAssignments(courseNumber):
    return sorted([d for d in os.listdir('{}/{}'.format(archivePath, courseNumber)) if os.path.isdir('{}/{}/{}'.format(archivePath, courseNumber, d))])
    
def ListQuarters(courseNumber, assignmentName):
    return sorted([d for d in os.listdir('{}/{}/{}'.format(archivePath, courseNumber, assignmentName)) if os.path.isdir('{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, d))])
    
def ListIDs(courseNumber, assignmentName, quarter):
    return sorted([d.split('_')[0] for d in os.listdir('{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, quarter)) if os.path.isdir('{}/{}/{}/{}/{}'.format(archivePath, courseNumber, assignmentName, quarter, d))])

def InterpretQuarter(quarter):
    numName = {'2': 'Fall', '4': 'Winter', '6': 'Spring', '8': 'Summer'}
    if re.match('1\d\d[2468]\D?$', quarter):
        year = int(quarter[1:3])
        return '{}{}-{}'.format((quarter[-1].upper() + '-' if len(quarter)  == 5 else ''), year, numName[quarter[3]])
    elif quarter.lower() == 'multiple':
        return 'Multiple'
    elif quarter.lower() == 'online':
        return 'Online'
    return quarter

def Completer(text, state):
    try:
        i = glob.iglob('{}*'.format(text))
        while True:
            r = i.next()
            if not state:
                return r
            else:
                state -= 1
    except StopIteration:
        pass

def Run():
    try:
        print """   __  __  ___  ____ ____  
  |  \/  |/ _ \/ ___/ ___| 
  | |\/| | | | \___ \___ \ 
  | |  | | |_| |___) |__) |
  |_|  |_|\___/|____/____/
"""
        # Setup autocomplete
        readline.parse_and_bind("tab: complete")
        readline.set_completer(Completer)

        # Load global settings
        settings = st.readSettings(scriptDir)
        
        if set(settings.keys()) == set(settingsDescriptions.keys()):
            try:
                for s in settings:
                    print "{}: {}".format(settingsDescriptions[s], settings[s])
                answer = None
                while answer != 'Y' and answer != 'n' and answer != '':
                    answer = raw_input("Is the above information correct? [Y/n]: ")
                    
                if answer == 'n':
                    settings = dict()
            finally:
                print
        
        # Check that all global settings are valid
        if len(settings) != len(settingsDescriptions) and len(settingsDescriptions) != 0:
            try:
                print "Please enter the following information:"
                for s in settingsDescriptions:
                    if s not in settings:
                        settings[s] = raw_input('{}: '.format(settingsDescriptions[s]))
                st.writeSettings(scriptDir, settings)
            finally:    
                print

        modes = ["Run MOSS", "Archive submissions"]
        mode = modes.index(ui.selectOption('What would you like to do?', modes))

        if mode == 0:
            run.RunMode(settings)
        elif mode == 1:
            archive.ArchiveMode(settings)
        else:
            raise Exception('Invalid mode')
    
    except KeyboardInterrupt, SystemExit:
        print '\nCancelled!'
    except Exception as ex:
        log.printLog(repr(ex)) 
