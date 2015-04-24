#!/usr/bin/env python
# (C) 2015 Ed Bueler

import argparse
import sys
import numpy as np
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description=
'''Generate robustness-of-Newton-convergence figures from ASCII files.''')
parser.add_argument('-o', metavar='FILENAME',
                    help='image filename (e.g. .png or .pdf)')
parser.add_argument('inname', metavar='FILE', type=str,
                    help='name of ASCII input file')
args = parser.parse_args()

def readfile(filename):
    try:
        vfile = open(filename, 'r')
    except IOError:
        print 'ERROR: cannot open file %s' % filename
        sys.exit(1)
    x = vfile.readlines()
    vfile.close()
    if np.mod(len(x),6) != 0:
        print 'ERROR: file does not contain 6X lines'
        sys.exit(2)
    dx = []
    cseps = []
    maxD = []
    ttime = []
    datatype = []
    vitype = []
    for k in range(len(x)/6):
        dx.append(      float(x[6*k].rstrip()  ))
        cseps.append(   float(x[6*k+1].rstrip()))
        maxD.append(    float(x[6*k+2].rstrip()))
        ttime.append(   float(x[6*k+3].rstrip()))
        datatype.append(x[6*k+4].rstrip())  # sea or mcb
        vitype.append(  x[6*k+5].rstrip())  # rsls or ssls
    return dx, cseps, maxD, ttime, datatype, vitype

dx, cseps, maxD, ttime, datatype, vitype = readfile(args.inname)

plt.figure(figsize=(7,5))
plt.hold(True)
for k in range(len(dx)):
    marksize = 10.0
    if vitype[k] == 'rsls':
        if datatype[k] == 'sea':
            mark = 'ok' # circle
            marksize = 11.0
        else:
            mark = 'xk'
    else:
        if datatype[k] == 'sea':
            mark = 'sk' # square
        else:
            mark = '+k'
            marksize = 12.0
    line, = plt.loglog(dx[k],cseps[k],mark,markersize=marksize,
                       markerfacecolor='w',alpha=0.7,markeredgewidth=2.0)
    if dx[k] > 7000.0:
        if datatype[k] == 'sea':
            DT = 'BM1'
        else:
            DT = 'MCB'
        if vitype[k] == 'rsls':
            VI = 'rs'
        else:
            VI = 'ss'
        line.set_label(DT + ' ' + VI)
dxmin, dxmax = 350.0, 12000.0
# lines at \eps_0 ... \eps_11:
klist = np.arange(12)
epslist = 10.0**(-klist/3.0)
for k in klist:
    plt.loglog([480.0,dxmax],[epslist[k],epslist[k]],'k--',lw=0.7)
    plt.text(390.0,0.9*epslist[k],r'$\epsilon_{%d}$' % k, fontsize=16.0)
plt.hold(False)
plt.axis([dxmin, dxmax, 0.0001/1.2, 2.0*1.0])
plt.xlabel(r'$\Delta x$', fontsize=16.0, labelpad=1)
plt.xticks([500, 1000, 2500, 5000, 10000], ('500m', '1km', '2.5km', '5km', '10km'), fontsize=12.0)
klist = np.arange(5)
plt.yticks(10.0**(-klist), ('1.0','0.1','0.01','0.001','0.0001'), fontsize=12.0)
ax = plt.axes()
ax.xaxis.grid(True)
ax.yaxis.grid(False)
plt.legend(fontsize=14.0, loc='upper right')
if args.o == None:
    plt.show()
else:
    plt.savefig(args.o,bbox_inches='tight')

