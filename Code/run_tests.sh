#!/bin/bash

SNNI=cheetah
# SNNI=SCI_HE
Data=sqnet
# Data=resnet50
End=5

for i in {1..2}; do 
    echo "Starting $i"
    bash Code/run_test.sh "${SNNI}_${Data}_$i" & PID=$!
    wait $PID
done