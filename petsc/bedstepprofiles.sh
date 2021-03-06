#!/bin/bash

# generate profile comparison figure for bedrock step

set -x

otheropts="-mah_bedstep -cs_D0 0.001 -da_refine 1 -snes_max_it 400 -pc_type lu -cs_end 12"

./mahaffy -mah_dump $1 $otheropts -mah_lambda 0.0
(cd $1 && mv unnamed.dat noupwind.dat)

./mahaffy -mah_dump $1 $otheropts -mah_lambda 1.0
(cd $1 && mv unnamed.dat upwindfull.dat)

./mahaffy -mah_dump $1 $otheropts

(cd $1 && ../figsmahaffy.py --profile --half --exactbed -extra_H noupwind.dat,upwindfull.dat -extra_H_labels M*,\$\\lambda=0\$,\$\\lambda=1\$)

