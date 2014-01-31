#!/usr/bin/python

import os, shutil, sys, getopt

directory = ['.']
verbose = False
dryRun = False

def FlattenDirsIn(q):
    cwd = os.getcwd()
    os.chdir(q)
    for assgn in os.listdir('.'):
        if not os.path.isdir(assgn): continue
        if verbose: print 'Flattening {}/{}'.format(q, assgn)
	os.chdir(assgn)
	for root, dirs, files in os.walk('.'):
	    if root == '.': continue
	    for f in files:
	        source = '{}/{}'.format(root, f)
		destination = './{}'.format(f)
		count = 0
		while os.path.exists(destination):
		    count = count + 1
		    destination = './{}_{}.{}'.format(f.split('.')[0], count,
		        f.split('.')[1]) if len(f.split('.')) > 1 else './{}_{}'.format(f, count)
	        if verbose: print 'Moving {} to {}'.format(source, destination)
		if not dryRun: shutil.move(source, destination)
	os.chdir('..')
	if verbose: print ''
    os.chdir(cwd)

if __name__ == '__main__':
    try:
        arglist, remaining = getopt.gnu_getopt(sys.argv[1:], 'vd')
	opt_args = {}
	for arg, val in arglist:
	    opt_args[arg] = val
	if remaining: directory = map(lambda x: x.rstrip('/'), remaining)
    except Exception as ex:
        Usage()
	print repr(ex)
        sys.exit()

    if '-v' in opt_args:
        verbose = True

    if '-d' in opt_args:
        dryRun = True

    for q in directory:
        FlattenDirsIn(q)
        
