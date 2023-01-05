#!/bin/bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

SNNI="cheetah"
# SNNI = SCI_HE
Data="sqnet"
# Data = resnet50

if [ $# -eq 1 ]; then
    OUTPUT_NAME=$1
else
    OUTPUT_NAME="${SNNI}_${Data}_output"
fi

if [ $# -eq 2 ]; then
    OUTPUT_NAME=$1
    NR=$2
else
    NR=0
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
    
    if [[ ! -z "$PID_SERVER" ]]; then
        if ps -p $PID_SERVER > /dev/null 2>&1; then 
            if kill $PID_SERVER; then 
                printf "${GREEN}Killed server script\n${ENDCOLOR}"
            else 
                printf "${RED}Error killing server script, pid:${PID_SERVER}\n${ENDCOLOR}"
            fi
        else
            printf "No PID_SERVER running\n"
        fi
    else
        printf "PID_SERVER not set\n"
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

    if [[ ! -z "$PID_RUN_CLIENT" ]]; then
        if ps -p $PID_RUN_CLIENT > /dev/null 2>&1; then 
            if kill $PID_RUN_CLIENT; then 
                printf "${GREEN}Killed server process\n${ENDCOLOR}"
            else 
                printf "${RED}Error killing server process, pid:${PID_RUN_CLIENT}\n${ENDCOLOR}"
            fi
        else
            printf "No PID_RUN_CLIENT running\n"
        fi
    else
        printf "PID_RUN_CLIENT not set\n"
    fi
    exit 1
}

modprobe intel_rapl_common # or intel_rapl for kernels < 5

# Clear last results
# JSON_NAME="log.json"
JSON_PATH=Code/Logs/$OUTPUT_NAME.json
if test -f $JSON_PATH; then rm $JSON_PATH; fi

# Start scaphandre and save its pid to PID_SCAPHANDRE
./Scaphandre/target/debug/scaphandre json -n 1 -s 0 -f $JSON_PATH & PID_SCAPHANDRE=$!
while ! test -f $JSON_PATH; do 
    test -f $JSON_PATH
done

printf "${GREEN}Started scaphandre: %d:%d:%d${ENDCOLOR}\n" $[$(date +%-H)] $[$(date +%-M)] $[$(date +%-S)]

# Start server- and client side and save pid's
cd Cheetah
if test -f data/client; then rm data/client; fi
if test -f data/server; then rm data/server; fi

if . scripts/run-server.sh cheetah sqnet & PID_SERVER=$!; then   
    # wait $PID_SERVER
    printf "${GREEN}Started server\n${ENDCOLOR}"
    if . scripts/run-client.sh cheetah sqnet & PID_CLIENT=$!; then
        # wait $PID_CLIENT
        printf "${GREEN}Started client\n${ENDCOLOR}"
    else
        printf "${RED}Could not start client\n${ENDCOLOR}" 
        cleanup
    fi
else
    printf "${RED}Could not start server\n${ENDCOLOR}"
    cleanup
fi

# Save PID's from server and client process
while [[ ! -f data/server ]]; do : ; done
PID_RUN_SERVER=$( cat data/server )
while [[ ! -f data/client ]]; do : ; done
PID_RUN_CLIENT=$( cat data/client )

# Wait till process is finished
wait $PID_SERVER
printf "${GREEN}Server finished${ENDCOLOR}\n"
wait $PID_CLIENT
printf "${GREEN}Client finished${ENDCOLOR}\n"
cd ..

# End measuring program
kill $PID_SCAPHANDRE
# echo "name:"$output_name
printf "${GREEN}Scaphandre finished: %d:%d:%d${ENDCOLOR}\n" $[$(date +%-H)] $[$(date +%-M)] $[$(date +%-S)]

printf "\nServer pid: ${PID_SERVER}\nClient pid: ${PID_CLIENT}\nScaphandre pid: ${PID_SCAPHANDRE}\nRun-Client pid: ${PID_RUN_CLIENT}\nRun Server pid: ${PID_RUN_SERVER}\n\nEND\n\n"
echo '"'${NR}'":{"client":'${PID_RUN_CLIENT}',"server":'${PID_RUN_SERVER}',"scaphandre":'${PID_SCAPHANDRE}'}END' >> Code/Logs/pids
# python3 Code/parse_results.py -c $PID_RUN_CLIENT -s $PID_RUN_SERVER -f $JSON_PATH -n "cheetah-sqnet.png" -o $output_name
# export $PID_RUN_SERVER
exit 1



