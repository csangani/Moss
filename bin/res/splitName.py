#!/usr/bin/python

import os, shutil

files = os.listdir('.')
for f in files:
    shutil.move(f, '{}_{}'.format(f[:-1], f[-1]))
