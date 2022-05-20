#!/bin/bash

function file_checked(){
    local file_path="/db/data/logfile.txt"
    local check_time=1
    while [[ true ]]; do
        file_old_stat="`stat ${file_path}|grep Modify`"
        sleep ${check_time}
        file_new_stat="`stat ${file_path}|grep Modify`"
        if [ -f ${file_path} ]; then  # file exists
            if [[ `echo ${file_old_stat}` == `echo ${file_new_stat}` ]]; then
                echo "### In ${check_time}s, ${file_path} doesn't change ###"
            else
                grep "time" ${file_path} | tail -1 > /db/data/mqtt_sensordata.txt  # get the last data
                echo "### In ${check_time}s, ${file_path} changes ###"
            fi
            echo "${file_path} exists."
        else
            echo "${file_path} does not exists."
        fi
    done
}

touch /db/data/mqtt_sensordata.txt

file_checked

## use '&' to execute script in background, e.g., `sh check_file.sh &`