#!/bin/bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

SNNI="cheetah"
# SNNI = SCI_HE
NN="sqnet"
# NN = resnet50

#TODO: error checking
if [ $# -eq 4 ]; then
    SNNI=$1
    NN=$2
    NR=$3
    TYPE=$4
else
    SNNI="cheetah"
    # SNNI = SCI_HE
    NN="sqnet"
    # NN = resnet50
    NR=0
    TYPE=server
fi

trap cleanup SIGINT

function cleanup(){
    printf "${RED}\rCleaning up\n${ENDCOLOR}"
    if [[ ! -z "$PID_SCAPHANDRE" ]] && ps -p $PID_SCAPHANDRE > /dev/null 2>&1; then 
        if kill $PID_SCAPHANDRE; then 
            printf "${GREEN}Killed Scaphandre process\n${ENDCOLOR}"
        else 
            printf "${RED}Error killing Scaphandre process, pid:${PID_SCAPHANDRE}\n${ENDCOLOR}"
        fi
    fi
    
    if [[ ! -z "$PID_CLIENT" ]]; then
        if ps -p $PID_CLIENT > /dev/null 2>&1; then 
            if kill $PID_CLIENT; then 
                printf "${GREEN}Killed client script\n${ENDCOLOR}"
            else 
                printf "${RED}Error killing client script, pid:${PID_CLIENT}\n${ENDCOLOR}";
            fi
        else
            printf "No PID_CLIENT running\n"
        fi
    else
        printf "PID_CLIENT not set\n"
    fi

    if [[ ! -z "$PID_RUN_SERVER" ]]; then
        if ps -p $PID_RUN_SERVER > /dev/null 2>&1; then 
            if kill $PID_RUN_SERVER; then 
                printf "${GREEN}Killed server process\n${ENDCOLOR}"
            else 
                printf "${RED}Error killing server process, pid:${PID_RUN_SERVER}\n${ENDCOLOR}"
            fi
        else
            printf "No PID_RUN_SERVER running\n"
        fi
    else
        printf "PID_RUN_SERVER not set\n"
    fi

    exit 1
}

modprobe intel_rapl_common # or intel_rapl for kernels < 5

# Clear last results

# Create folder for results (if it does not exist) and empty (if it does exist)
JSON_FOLDER=Code/Logs/${SNNI}_${NN}/
JSON_PATH=${JSON_FOLDER}${TYPE}_${NR}.json # output saved in /cheetah_sqnet/client_0.json
if [[ -d ${JSON_FOLDER} ]]; then
    if test -f $JSON_PATH; then rm $JSON_PATH; fi
    if test -f ${JSON_FOLDER}${TYPE}_pids; then rm ${JSON_FOLDER}${TYPE}_pids; fi
else
    mkdir $JSON_FOLDER
fi


# Start scaphandre and save its pid to PID_SCAPHANDRE
./Scaphandre/target/debug/scaphandre json -n 1 -s 0 -f $JSON_PATH & PID_SCAPHANDRE=$!
# Wait till scaphandre started and outputs results
while ! test -f $JSON_PATH; do 
    test -f $JSON_PATH
done

printf "${GREEN}Started scaphandre: %d:%d:%d${ENDCOLOR}\n" $[$(date +%-H)] $[$(date +%-M)] $[$(date +%-S)]

# Start server- and client side and save pid's
cd Cheetah
if test -f data/${TYPE}; then rm data/${TYPE}; fi

if . scripts/run-${TYPE}.sh $1 $2 & PID_SCRIPT=$!; then   
    # wait $PID_SERVER
    printf "${GREEN}Started ${TYPE}\n${ENDCOLOR}"
else
    printf "${RED}Could not start ${TYPE}\n${ENDCOLOR}"
    cleanup
fi

# Save PID's from server and client process
while [[ ! -f data/${TYPE} ]]; do : ; done
PID_RUN=$( cat data/${TYPE} )

# Wait till process is finished
wait $PID_SCRIPT
printf "${GREEN}${TYPE} finished${ENDCOLOR}\n"

# End measuring program
kill $PID_SCAPHANDRE
printf "${GREEN}Scaphandre finished: %d:%d:%d${ENDCOLOR}\n" $[$(date +%-H)] $[$(date +%-M)] $[$(date +%-S)]

cd ..

printf "\n${TYPE} script pid: ${PID_SCRIPT}\nScaphandre pid: ${PID_SCAPHANDRE}\nRun-${TYPE} pid: ${PID_RUN}\n\nEND\n\n"
echo '"'${NR}'":{"'${TYPE}'":'${PID_RUN}',"scaphandre":'${PID_SCAPHANDRE}'}END' >> ${JSON_FOLDER}${TYPE}_pids
exit 1



