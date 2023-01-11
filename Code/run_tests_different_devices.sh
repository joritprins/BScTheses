#!/bin/bash

trap cleanup SIGINT

R="\e[31m"
G="\e[32m"
ENDCOLOR="\e[0m"
Y='\033[33m'

function cleanup(){
    printf "${R}\rCleaning up\n${E}"
    kill -2 $PID
    exit 1
}

if [ $# -eq 1 ]; then
    TYPE=$1
    END=$2
else
    TYPE=server
    END=10
fi

if test -f Code/Logs/* && [ -n "$(ls -A Code/Logs/)" ]; then 
    cp Code/Logs/* Code/LogsOld;
    rm -rf Code/Logs/*
fi

for SNNI in "SCI_HE" "cheetah"; do
    printf "${Y}\rStarting tests for $SNNI\n${ENDCOLOR}"
    for Data in "sqnet" "resnet50"; do
        printf "${Y}\rStarting tests with $Data\n${ENDCOLOR}"
        for i in $(seq 1 $END); do 
            printf "${Y}\rRun $i ($SNNI, $Data)\n${ENDCOLOR}"
            bash Code/run_test_single.sh $SNNI $Data $i $TYPE & PID=$!
            wait $PID
        done
        printf "${G}\rFinished tests for $Data\n${ENDCOLOR}"
    done
    printf "${G}\rFinished tests for $SNNI\n${ENDCOLOR}"
done