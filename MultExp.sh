#!/bin/bash

n=$1
Repeat=$2

#N=$((2**(n - 2)))
#N=$((2**((n/2) - 2)))
#N=$((2**((n/2) - 1)))
N=$((2**((n/2))))
#N=$((2**((n/2) + 1)))
#N=$((2**((n/2) + 2)))
S=$((100*$N))
#N=1
#S=1

for ((it=1; it <= $Repeat; it++))
do
	nohup python3 Experiment.py -i $n $N $S >> Outputs.txt &
done
