import os, shutil

for x in os.listdir('.'):
    if os.path.isdir(x):
        shutil.move(x, ''.join(x.split('_')))
