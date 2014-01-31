#!/usr/bin/python

import sys, getopt, os, shutil

directory = ['.']
separator = "_"
verbose = False
dryRun = False

def DeleteDuplicates(d):
    if verbose: print 'Deleting duplicates from {}'.format(d)
    try:
        files = os.listdir(d)
        files = [(separator.join(f.split(separator)[:-1]), f.split(separator)[-1]) if
                  len(f.split(separator)) > 1 else (f,'') for f in files]
        mappedFiles = dict([(key, []) for (key, value) in files])
        for (key, value) in files:
	    if len(value) > 0:
                mappedFiles[key] = sorted(mappedFiles[key] + [int(value)])
        filesToDelete = [(key, mappedFiles[key][:-1]) for key in mappedFiles if len(mappedFiles[key]) > 1]
        for (key, files) in filesToDelete:
            for f in files:
                if verbose: print 'Deleting {}/{}{}{}'.format(d, key, separator, f)
                if not dryRun:
	            shutil.rmtree('{}/{}{}{}'.format(d, key, separator, f))
    except Exception as ex:
        print repr(ex)
	sys.exit()
    if verbose: print ''

def Usage():
    print """
Usage:	deleteDuplicates.py [options] <directory list>

Options are:
	-s SEPARATOR	Characters that separate the SUID from the assignment
			number. If multiple separators are present, the last one
			is split. Default is underscore ("_").
	-v		Verbose
	-d		Dry run. Does not actually delete directories.

Example:
	deleteDuplicates.py -s '_' .
"""

if __name__ ==  '__main__':
    try:
        optlist, remaining = getopt.gnu_getopt(sys.argv[1:], 's:vd')
	opt_args = {'-s': '_'}
	for arg, val in optlist:
	    opt_args[arg] = val
	if remaining:
	    directory = map(lambda x: x.rstrip('/'), remaining)
    except Exception as ex:
        Usage()
        print repr(ex)
	sys.exit()
	   
    if opt_args['-s']:
        separator = opt_args['-s']

    if '-v' in opt_args:
        verbose = True

    if '-d' in opt_args:
        dryRun = True

    for d in directory:
        DeleteDuplicates(d)
