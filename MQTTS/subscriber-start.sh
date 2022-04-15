#!/bin/bash
# This shell script is made by Chia-Chin Chung <60947091s@gapps.ntnu.edu.tw>

# generate the new subscriber CSR using pre-set CA.key & cert
openssl req -new -newkey $SIG_ALG -keyout /test/certs/subscriber.key -out /test/certs/subscriber.csr -nodes -subj "/O=test-subscriber/CN=$SUB_IP"

# generate the subscriber cert
openssl x509 -req -in /test/certs/subscriber.csr -out /test/certs/subscriber.crt -CA /test/certs/CA.crt -CAkey /test/certs/CA.key -CAcreateserial -days 365

# modify file permissions
chmod 777 certs/*

# generate a log file
touch /db/data/logfile.txt

# execute mosquitto MQTT subscriber
flg=0
while [ 1 ]; do
    mosquitto_sub -h $BROKER_IP -t test/sensor1 -q 0 -i "Client_sub" -k 120 -C 1 \
    --tls-version tlsv1.3 --cafile /test/certs/CA.crt \
    --cert /test/certs/subscriber.crt --key /test/certs/subscriber.key >> /db/data/logfile.txt

    if [ $flg -eq 0 ]
        then
        echo "first message!!"
    elif [ $flg -eq 1 ]
        then
        echo "other message!!"
        sed -i '1d' /db/data/logfile.txt
    fi

    flg=1
    sleep 1s
done
