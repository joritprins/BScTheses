#!/bin/bash

trap cleanup SIGINT

function cleanup(){
    RED="\e[31m"
    GREEN="\e[32m"
    ENDCOLOR="\e[0m"
    printf "${RED}\rCleaning up\n${ENDCOLOR}"
    kill -2 $PID
    exit 1
}

SNNI=cheetah
# SNNI=SCI_HE
Data=sqnet
# Data=resnet50
End=5

rm -rf Code/Logs/*

for i in {0..3}; do 
    echo "Starting $i"
    bash Code/run_test.sh "${SNNI}_${Data}_$i" $i & PID=$!
    wait $PID
done