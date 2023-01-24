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

if [ $# -eq 2 ]; then
    TYPE=$1
    END=$2
else
    TYPE=server
    END=10
fi

sudo rm -rf Code/Logs
sudo mkdir Code/Logs


printf "$G#####################################################\n
############ STARTING CHANGING SERVER BW ############\n
#####################################################\n$ENDCOLOR"

# sudo bash Cheetah/scripts/throttle.sh lan 10000
# for SNNI in "cheetah" "SCI_HE"; do
#     printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
#     NN='sqnet'
#     printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

#     for BW in "30" "14" "3"; do
#         if [ $TYPE == server ]; then
#             printf "Server, changing bandwith to $BW\n";
#             sudo bash Cheetah/scripts/throttle.sh lan $BW;
#         else
#             printf "Not server, server bw to $BW";
#         fi

#         for i in $(seq 1 $END); do 
#             printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
#             bash Code/run_test_single.sh $SNNI $NN $i $TYPE server_${BW} & PID=$!
#             wait $PID
#         done
#     done
#     printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
#     printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
# done
# sudo bash Cheetah/scripts/throttle.sh del

sudo bash Cheetah/scripts/throttle.sh lan 10000
SNNI=SCI_HE
NN=sqnet
BW=3
if [ $TYPE == server ]; then
    printf "Server, changing bandwith to $BW\n";
    sudo bash Cheetah/scripts/throttle.sh lan $BW;
else
    printf "Not server, server bw to $BW";
fi

for i in $(seq 3 10); do 
    printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
    bash Code/run_test_single.sh $SNNI $NN $i $TYPE server_${BW} & PID=$!
    wait $PID
done
sudo bash Cheetah/scripts/throttle.sh del

printf "$G#######################################################\n
# ############ STARTING CHANGING CLIENT BW ############\n
# #####################################################\n$ENDCOLOR"

sudo bash Cheetah/scripts/throttle.sh lan 10000
for SNNI in "cheetah" "SCI_HE"; do
    printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
    NN='sqnet'
    printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

    for BW in "30" "14" "3"; do
        if [ $TYPE == client ]; then
            printf "Client, changing bandwith to $BW\n";
            sudo bash Cheetah/scripts/throttle.sh lan $BW;
        else
            printf "Not client, client bw to $BW";
        fi

        for i in $(seq 1 5); do 
            printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
            bash Code/run_test_single.sh $SNNI $NN $i $TYPE client_${BW} & PID=$!
            wait $PID
        done
    done
    printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
    printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
done
sudo bash Cheetah/scripts/throttle.sh del

printf "$G######################################################\n
#############  STARTING CHANGING BOTH BW  ############\n
######################################################\n$ENDCOLOR"

sudo bash Cheetah/scripts/throttle.sh lan 10000
for SNNI in "cheetah" "SCI_HE"; do
    printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
    NN='sqnet'
    printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

    for BW in "30" "14" "3"; do
        printf "Changing bandwith to $BW\n";
        sudo bash Cheetah/scripts/throttle.sh lan $BW;

        for i in $(seq 1 5); do 
            printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
            bash Code/run_test_single.sh $SNNI $NN $i $TYPE both_${BW} & PID=$!
            wait $PID
        done
    done
    printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
    printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
done
sudo bash Cheetah/scripts/throttle.sh del


printf "$G######################################################\n
#############           PART 2            ############\n
######################################################\n$ENDCOLOR"

printf "$G#######################################################\n
# ############ STARTING CHANGING CLIENT BW ############\n
# #####################################################\n$ENDCOLOR"

sudo bash Cheetah/scripts/throttle.sh lan 10000
for SNNI in "cheetah" "SCI_HE"; do
    printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
    NN='sqnet'
    printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

    for BW in "30" "14" "3"; do
        if [ $TYPE == client ]; then
            printf "Client, changing bandwith to $BW\n";
            sudo bash Cheetah/scripts/throttle.sh lan $BW;
        else
            printf "Not client, client bw to $BW";
        fi

        for i in $(seq 6 10); do 
            printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
            bash Code/run_test_single.sh $SNNI $NN $i $TYPE client_${BW} & PID=$!
            wait $PID
        done
    done
    printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
    printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
done
sudo bash Cheetah/scripts/throttle.sh del

printf "$G######################################################\n
#############  STARTING CHANGING BOTH BW  ############\n
######################################################\n$ENDCOLOR"

sudo bash Cheetah/scripts/throttle.sh lan 10000
for SNNI in "cheetah" "SCI_HE"; do
    printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
    NN='sqnet'
    printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

    for BW in "30" "14" "3"; do
        printf "Changing bandwith to $BW\n";
        sudo bash Cheetah/scripts/throttle.sh lan $BW;

        for i in $(seq 6 10); do 
            printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
            bash Code/run_test_single.sh $SNNI $NN $i $TYPE both_${BW} & PID=$!
            wait $PID
        done
    done
    printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
    printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
done
sudo bash Cheetah/scripts/throttle.sh del































# sudo bash Cheetah/scripts/throttle.sh lan 10000
# for SNNI in "cheetah" "SCI_HE"; do
#     printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
#     for NN in "sqnet" "resnet50"; do
#         printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

#         for BW in "50" "100" "150" "200" "300" "400" "500"; do
#             if [ $TYPE == server ]; then
#                 printf "Server, changing bandwith to $BW\n";
#                 sudo bash Cheetah/scripts/throttle.sh lan $BW;
#             fi

#             for i in $(seq 1 $END); do 
#                 printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
#                 bash Code/run_test_single.sh $SNNI $NN $i $TYPE server_${BW} & PID=$!
#                 wait $PID
#             done
#         done
#         printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
#     done
#     printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
# done
# sudo bash Cheetah/scripts/throttle.sh del

# NN=resnet50
# SNNI=SCI_HE
# END=10
# for BW in "50" "100" "200" "400" "500"; do
#     if [ $TYPE == server ]; then
#         printf "Server, changing bandwith to $BW\n";
#         sudo bash Cheetah/scripts/throttle.sh lan $BW;
#     fi

#     for i in $(seq 1 $END); do 
#         printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
#         bash Code/run_test_single.sh $SNNI $NN $i $TYPE server_${BW} & PID=$!
#         wait $PID
#     done
# done

# printf "$G#####################################################\n
# ############ STARTING CHANGING CLIENT BW ############\n
# #####################################################\n$ENDCOLOR"

# sudo bash Cheetah/scripts/throttle.sh lan 10000
# for SNNI in "cheetah" "SCI_HE"; do
#     printf "${Y}############ Testing for $SNNI ############\n${ENDCOLOR}"
#     for NN in "sqnet"; do
#         printf "${Y}############ Testing for $NN\n${ENDCOLOR}"

#         for BW in "50" "100" "150" "200" "400" "500"; do
#             if [ $TYPE == client ]; then
#                 printf "Server, changing bandwith to $BW\n";
#                 sudo bash Cheetah/scripts/throttle.sh lan $BW;
#             fi

#             for i in $(seq 1 $END); do 
#                 printf "${Y}\rRun $i ($SNNI, $NN)\n${ENDCOLOR}"
#                 bash Code/run_test_single.sh $SNNI $NN $i $TYPE client_${BW} & PID=$!
#                 wait $PID
#             done
#         done
#         printf "${G}\r############ Finished tests for $NN\n${ENDCOLOR}"
#     done
#     printf "${G}\r############ Finished tests for $SNNI\n${ENDCOLOR}"
# done
# sudo bash Cheetah/scripts/throttle.sh del
