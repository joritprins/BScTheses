#!/bin/bash
DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"

RED="\e[31m"
GREEN="\e[32m"
ENDCOLOR="\e[0m"

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

trap cleanup SIGINT

modprobe intel_rapl_common # or intel_rapl for kernels < 5

# Clear last results
JSON_NAME="log.json"
if test -f Code/$JSON_NAME; then rm Code/$JSON_NAME; fi

# Start scaphandre and save its pid to PID_SCAPHANDRE
./Scaphandre/target/debug/scaphandre json -n 1 -s 0 -f Code/$JSON_NAME & PID_SCAPHANDRE=$!
while ! test -f Code/$JSON_NAME; do 
    test -f Code/$JSON_NAME
done

printf "${GREEN}Started scaphandre: %d:%d:%d${ENDCOLOR}\n" $[$(date +%H)] $[$(date +%M)] $[$(date +%S)]

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
printf "${GREEN}Scaphandre finished: %d:%d:%d${ENDCOLOR}\n" $[$(date +%H)] $[$(date +%M)] $[$(date +%S)]

printf "\nServer pid: ${PID_SERVER}\nClient pid: ${PID_CLIENT}\nScaphandre pid: ${PID_SCAPHANDRE}\nRun-Client pid: ${PID_RUN_CLIENT}\nRun Server pid: ${PID_RUN_SERVER}\n\nEND\n\n"

python3 Code/parse_results.py -c $PID_RUN_CLIENT -s $PID_RUN_SERVER -f Code/$JSON_NAME -n "Code/cheetah-sqnet.png"
# export $PID_RUN_SERVER
exit 1



# echo "$!\n"
# printf $CODE'\n'


# #!/bin/bash
# # type "finish" to exit

# stty -echoctl # hide ^C

# # function called by trap
# other_commands() {
#     tput setaf 1
#     printf "\rSIGINT caught      "
#     tput sgr0
#     sleep 1
#     printf "\rType a command >>> "
# }

# trap 'other_commands' SIGINT

# input="$@"


# exit 1
# while true; do
#     printf $DIR
#     read input
#     [[ $input == finish ]] && break
#     bash -c "$input"
# done

# # run processes and store pids in array
# for i in $n_procs; do
#     ./procs[${i}] &
#     pids[${i}]=$!
# done

# # wait for all pids
# for pid in ${pids[*]}; do
#     wait $pid
# done

