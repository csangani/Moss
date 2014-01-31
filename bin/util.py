import os, shutil, glob

tools = dict()

def flattenDir(d, verbose = False, dryRun = False):
    cwd = os.getcwd()
    if not os.path.isdir(d): raise 'Not a directory: {}'.format(d)
    if verbose: print 'Flattening d'.format(d)
    os.chdir(d)
    for root, dirs, files in os.walk('.'):
        if root == '.': continue
        for f in files:
            source = '{}/{}'.format(root, f)
            destination = './{}'.format(f)
            count = 0
            while os.path.exists(destination):
                count = count + 1
                destination = './{}_{}.{}'.format(f.split('.')[0], count, f.split('.')[1]) if len(f.split('.')) > 1 else './{}_{}'.format(f, count)
            if verbose: print 'Moving {} to {}'.format(source, destination)
            if not dryRun: shutil.move(source, destination)
    os.chdir(cwd)

def retainLast(d, separator = "_", verbose = False, dryRun = False):
    if not os.path.isdir(d): raise 'Not a directory: {}'.format(d)
    if verbose: print 'Deleting duplicates from {}'.format(d)
    files = os.listdir(d)
    files = [(separator.join(f.split(separator)[:-1]), f.split(separator)[-1]) if len(f.split(separator)) > 1 else (f,'') for f in files]
    mappedFiles = dict([(key, []) for (key, value) in files])
    for (key, value) in files:
        if len(value) > 0:
            mappedFiles[key] = sorted(mappedFiles[key] + [int(value)])
    filesToDelete = [(key, mappedFiles[key][:-1]) for key in mappedFiles if len(mappedFiles[key]) > 1]
    for (key, files) in filesToDelete:
        for f in files:
            if verbose: print 'Deleting {}/{}{}{}'.format(d, key, separator, f)
            if not dryRun: shutil.rmtree('{}/{}{}{}'.format(d, key, separator, f))

def mergeRetakes(d, separator = '_', verbose = False, dryRun = False):
    if not os.path.isdir(d): raise 'Not a directory: {}'.format(d)
    quarters = [q for q in os.listdir(d) if os.path.isdir('{}/{}'.format(d, q))]
    if 'multiple' in quarters:
    	quarters.remove('multiple')
    submissions = dict()
    for q in quarters:
        submissions[q] = [s.split(separator)[0] for s in os.listdir('{}/{}'.format(d, q)) if os.path.isdir('{}/{}/{}'.format(d, q, s))]
   
    retakes = dict()
    
    if os.path.isdir('{}/multiple'.format(d)):
        multiples = [m for m in os.listdir('{}/multiple'.format(d)) if os.path.isdir('{}/multiple/{}'.format(d, m))]
        for q in quarters:
            for s in submissions[q]:
                if s in multiples:
                    if s in retakes:
                        retakes[s] += [q]
                    else:
                        retakes[s] = [q]
        
    for q1 in quarters:
        for s1 in submissions[q1]:
            for q2 in quarters:
                for s2 in submissions[q2]:
                    if s1 == s2 and q1 != q2:
                        if s1 in retakes:
                            retakes[s1] += [q1, q2]
                        else:
                            retakes[s1] = [q1, q2]
    for r in retakes:
        retakes[r] = set(retakes[r])
        if verbose: print "Merging submissions for {}".format(r)
        for q in retakes[r]:
            sdir = glob.glob('{}/{}/{}*'.format(d, q, r))[0]
            ddir = '{}/multiple/{}/{}'.format(d, r, q)
            if verbose: print "Moving {} to {}".format(sdir, ddir)
            if not dryRun: shutil.move(sdir, ddir)
        if verbose: print

tools = ['retainLast', 'flattenDir', 'mergeRetakes']
