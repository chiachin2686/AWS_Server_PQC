#!/bin/bash

function file_checked(){
    local file_path="/db/data/logfile.txt"
    local check_time=1
    counter=0  # set a counter
    while [[ true ]]; do
        file_old_stat="`stat ${file_path}|grep Modify`"
        sleep ${check_time}
        file_new_stat="`stat ${file_path}|grep Modify`"
        if [ -f ${file_path} ]; then  # file exists
            if [[ `echo ${file_old_stat}` == `echo ${file_new_stat}` ]]; then
                echo "### File doesn't change ###"
            else
                grep "time" ${file_path} | tail -1 > /db/data/mqtt_sensordata.txt  # get the last data
                if [[ "$counter" -gt 1000 ]]; then  # if counter > 1000, reset the log file
                    rm ${file_path}
                    touch ${file_path}
                    counter=0
                else
                    counter=$((counter+1))
                fi
                echo "### File changes ###"
            fi
            echo "File exists."
        else
            echo "File does not exists."
        fi
    done
}

touch /db/data/mqtt_sensordata.txt

file_checked

## use '&' to execute script in background, e.g., `sh check_file.sh &`