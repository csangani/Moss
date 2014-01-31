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

import os, glob, subprocess, ui, settings as st, moss, re, client, itertools, string

##
## Select mode for running MOSS
##
## params:
## 	settings: Dict(String, String)
def RunMode(settings):
    # Select course
    courseNumber = ui.selectOption('Select a course:', moss.ListCourses(), transform = string.upper)

    # Select assignment
    assignmentName = ui.selectOption('Select an assignment:', moss.ListAssignments(courseNumber), transform = string.capitalize)
    
    # Load assignment settings
    assignmentSettings = st.readSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName))
    
    # Check for assignment settings validity
    if 'language' not in assignmentSettings:
        assignmentSettings['language'] = ui.selectOption("Select language: ", moss.languages.keys())
        st.writeSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName), assignmentSettings)

    modes = ['Run MOSS on submissions from a single quarter',
             'Run MOSS on submissions from multiple quarters',
             'Run MOSS on current quarter submissions for specific SUnet IDs']

    mode = modes.index(ui.selectOption('What would you like to do?', modes))

    if mode == 0:
    
        quarter = ui.selectOption('Select a quarter:', moss.ListQuarters(courseNumber, assignmentName), transform = moss.InterpretQuarter)
        result = IntraQuarterAnalysis(courseNumber, assignmentName, quarter)
        
    elif mode == 1:
    
        currentQuarter = ui.selectOption('Select current quarter:', moss.ListQuarters(courseNumber, assignmentName), transform = moss.InterpretQuarter)
        quarters = ui.askQuestion('Please enter a comma-separated list of quarters to compare against (wildcards will be expanded) [default: *]:').split(',')
        quarters = [q.strip() for q in quarters]
        if '' in quarters: quarters.remove('')
        if len(quarters) == 0: quarters = ['*']
        result = CrossQuarterAnalysis(courseNumber, assignmentName, currentQuarter, quarters)
        
    elif mode == 2:
    
        quarter = ui.selectOption('Select current quarter:', moss.ListQuarters(courseNumber, assignmentName), transform = moss.InterpretQuarter)
        IDs = ui.askQuestion('Please enter a comma-separated list of SUnet IDs:').split(',')
        IDs = [i.strip() for i in IDs]
        result = SpecificAnalysis(courseNumber, assignmentName, quarter, IDs)
        
    print "Result: {}\n".format(result)

##
## Run MOSS on submissions from one quarter
##
## params:
## 	courseNumber: String
##	assignmentName: String
##	quarter: String
def IntraQuarterAnalysis(courseNumber, assignmentName, quarter):
    """
    assignmentSettings = st.readSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName))
    
    # Build file list
    extensions = moss.languages[assignmentSettings['language']]
    
    files = []
    for e in extensions:
        f = glob.glob('{}/{}/{}/{}/*/{}'.format(moss.archivePath, courseNumber, assignmentName, quarter, e))
        if f is not None: files += f
        
    if len(files) == 0: raise Exception("No files found")
    
    files = dict([(f.split('/')[-2] + '/' + f.split('/')[-1], f) for f in files])
    
    # Check for starter code
    baseFiles = None
    if os.path.isfile('{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, quarter)):
        baseFiles = ['{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, quarter)]
    else:
        baseFiles = []
        
    # Run MOSS
    return RunMoss(files, assignmentSettings['language'], baseFiles, 'Course: {}<br/>Assignment: {}<br/>Quarter: {}'.format(courseNumber.upper(), assignmentName.capitalize(), moss.InterpretQuarter(quarter)))
    """
    return CrossQuarterAnalysis(courseNumber, assignmentName, quarter, [])
          
##
## Run MOSS against submissions from multiple quarters
##
## params:
##  courseNumber: String
##	assignmentName: String
##	currentQuarter: String
##  quarters: List(String)
def CrossQuarterAnalysis(courseNumber, assignmentName, currentQuarter, quarters):

    assignmentSettings = st.readSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName))
        
    # Build file list
    extensions = list(moss.languages[assignmentSettings['language']])
    
    IDs = moss.ListIDs(courseNumber, assignmentName, currentQuarter) + [f.split('/')[-2] for f in glob.glob('{}/{}/{}/multiple/*/{}'.format(moss.archivePath, courseNumber, assignmentName, currentQuarter))]
    
    files = []
    for q in set(quarters + [currentQuarter]):
        for e in extensions:
            f = glob.glob('{}/{}/{}/{}/*/{}'.format(moss.archivePath, courseNumber, assignmentName, q, e))
            if f is not None: files += f
            
    for e in extensions:
        files2 = glob.glob('{}/{}/{}/multiple/*/*/{}'.format(moss.archivePath, courseNumber, assignmentName, e))
        
    if len(files) + len(files2) == 0: raise Exception("No files found")
    
    files = dict([('{}{}/{}'.format(('{}/'.format(moss.InterpretQuarter(f.split('/')[-3])) if f.split('/')[-3] != currentQuarter else ''), f.split('/')[-2], f.split('/')[-1]), f) for f in files])
    
    files.update(dict([('{}/{}/{}-{}'.format(moss.InterpretQuarter(f.split('/')[-4]), f.split('/')[-3], moss.InterpretQuarter(f.split('/')[-2]), f.split('/')[-1]) if f.split('/')[-3] not in IDs else '{}/{}'.format(f.split('/')[-3], f.split('/')[-1]), f) for f in files2 if f.split('/')[-3] not in IDs or (f.split('/')[-3] in IDs and f.split('/')[-2] == currentQuarter)]))
        
    # Check for starter code
    baseFiles = None
    if os.path.isfile('{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, currentQuarter)):
        baseFiles = ['{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, currentQuarter)]
    else:
        baseFiles = []
        
    # Run MOSS
    return RunMoss(files, assignmentSettings['language'], baseFiles, 'Course: {}<br/>Assignment: {}<br/>Current Quarter: {}<br/>Compared Against: {}'.format(courseNumber.upper(), assignmentName.capitalize(), moss.InterpretQuarter(currentQuarter), quarters))
        
##
## Run MOSS against specific submissions from current quarter
##
## params:
## 	courseNumber: String
##	assignmentName: String
##	quarter: String
def SpecificAnalysis(courseNumber, assignmentName, quarter):
    assignmentSettings = st.readSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName))
    
    # Make sure (courseNumber, assignmentName, quarter) is valid
    if not os.path.isdir('{}/{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName, quarter)):
        print "No submissions found for course {} assignment {} in quarter {}".format(courseNumber, assignmentName, quarter)
	return

    # Check for assignment settings
    if 'language' not in assignmentSettings:
        assignmentSettings['language'] = ui.selectOption("Select language: ", moss.languages.keys())
        st.writeSettings('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName), assignmentSettings)
        
    # Check validity of patterns
    extensions = list(moss.languages[assignmentSettings['language']])
    
    dirs = [d for d in os.listdir('{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName)) if os.path.isdir('{}/{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName, d))]
    dirs.remove(quarter)
    if 'multiple' in dirs: dirs.remove('multiple')
    
    patterns = ['*/{}'.format(e) for e in extensions] + ['../{}/*/{}'.format(d, e) for d in dirs for e in extensions]
    
    rejects = []
    cwd = os.getcwd()
    os.chdir('{}/{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName, quarter))
    for p in patterns:
        try:
            glob.iglob(p).next()
        except StopIteration:
            rejects += [p]
    for r in rejects:
        patterns.remove(r)
        
    # Check for starter code
    baseFiles = None
    if os.path.isfile('{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, quarter)):
        baseFiles = ['{}/{}/{}/{}/base'.format(moss.starterCodePath, courseNumber, assignmentName, quarter)]
    else:
        baseFiles = []
        
    # Run MOSS
    runMoss(moss.mossScript, '{}/{}/{}/{}'.format(moss.archivePath, courseNumber, assignmentName, quarter), patterns, language = assignmentSettings['language'], baseFiles = baseFiles, verbose = True)
    
def RunMoss(files, lang, baseFiles, comment):
    
    print "Generating results...\n"
    answer = 'Y'
    while answer == 'Y' or answer == '':
        result =  client.Submit(files, lang = lang, directoryMode = True, baseFiles = baseFiles, comment = comment, verbose = True)
        if result == '':
            answer = None
            while answer != 'Y' and answer != 'n' and answer != '':
                answer = ui.askQuestion('Something went wrong while running MOSS. Would you like to try again? [Y/n]: ')
        else:
            break
    return result
