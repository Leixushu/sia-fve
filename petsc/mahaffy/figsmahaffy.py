#!/usr/bin/env python
#
# (C) 2015 Ed Bueler
#
# Generate .png figures from PETSc binary files written by mahaffy.c.
#
# Example of usage:
#   $ make mahaffy
#   $ ./mahaffy -mah_dump
#   $ python figsmahaffy.py
#   $ eog *.png

import argparse
import sys

import numpy as np
import matplotlib.pyplot as plt

try:
    import PetscBinaryIO as pbio
except:
    print "'import PetscBinaryIO' failed"
    print "need link to petsc/bin/petsc-pythonscripts/PetscBinaryIO.py?"
    sys.exit(2)

try:
    import petsc_conf
except:
    print "'import petsc_conf.py' failed"
    print "need link to petsc/bin/petsc-pythonscripts/petsc_conf.py?"
    sys.exit(2)

parser = argparse.ArgumentParser(description='Generate .png figures from PETSc binary files written by mahaffy.c.')
args = parser.parse_args()

# read a vec from a petsc binary file
io = pbio.PetscBinaryIO()
def readvec(fname,shape=(0,0)):
    try:
        fh = open(fname)
    except:
        print "unable to open '%s' ... ending ..." % fname
        sys.exit(3)
    objecttype = io.readObjectType(fh)
    if objecttype == 'Vec':
        v = io.readVec(fh)
        fh.close()
        if sum(shape) > 0:
            v = np.reshape(v,shape)
        print "  read vec from '%s' with shape %s" % (fname, str(np.shape(v)))
        return v
    else:
        print "unexpected objectype '%s' ... ending ..." % objecttype
        sys.exit(4)
        return

# write fields **in particular order**; see method DumpToFiles() in mahaffy.c for order
print "reading vars x,y,b,m,H,Herror from *.dat ..."
x = readvec('x.dat')
y = readvec('y.dat')
b = readvec('b.dat',shape=(len(y),len(x)))
m = readvec('m.dat',shape=(len(y),len(x)))
H = readvec('H.dat',shape=(len(y),len(x)))
Herror = readvec('Herror.dat',shape=(len(y),len(x)))

figdebug = False
def figsave(name):
    if figdebug:
        print '  showing %s ... close window to proceed ...' % name
        plt.show()  # debug
    else:
        plt.savefig(name,bbox_inches='tight')
        print '  figure file %s generated ...' % name

x = x/1000.0
y = y/1000.0

if len(x) == len(y):
    fsize = (12,9)
else:
    fsize = (int(19.0 * float(len(x)) / float(len(y))),14)

plt.figure(figsize=fsize)
plt.pcolormesh(x,y,H)
plt.axis('tight')
plt.colorbar()
plt.title('thickness solution H (m) with min=%.2f, max=%.2f' % (H.min(),H.max()))
figsave('H.png')

plt.figure(figsize=fsize)
plt.pcolormesh(x,y,b)
plt.axis('tight')
if (b.max() > b.min()):
    plt.colorbar()
plt.title('bed elevation b (m) with min=%.2f, max=%.2f' % (b.min(),b.max()))
figsave('b.png')

plt.figure(figsize=fsize)
s = np.maximum(0.0, H + b)
plt.pcolormesh(x,y,s)
plt.axis('tight')
plt.colorbar()
plt.title('surface elevation s (m) with min=%.2f, max=%.2f' % (s.min(),s.max()))
figsave('s.png')

plt.figure(figsize=fsize)
m = m * 31556926.0
plt.pcolormesh(x,y,m)
plt.axis('tight')
plt.colorbar()
plt.title('surface mass balance m (m/a) with min=%.2f, max=%.2f' % (m.min(),m.max()))
figsave('m.png')

plt.figure(figsize=fsize)
plt.pcolormesh(x,y,Herror)
plt.axis('tight')
plt.colorbar()
plt.title('thickness error H-Hexact (m) with min=%.2f, max=%.2f' % (Herror.min(),Herror.max()))
figsave('Herror.png')
