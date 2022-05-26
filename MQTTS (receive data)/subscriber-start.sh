#!/bin/bash
# This shell script is made by Chia-Chin Chung <60947091s@gapps.ntnu.edu.tw>

# generate the new subscriber CSR using pre-set CA.key & cert
openssl req -new -newkey $SIG_ALG -keyout /test/certs/subscriber.key -out /test/certs/subscriber.csr -nodes -subj "/O=test-subscriber/CN=$SUB_IP"

# generate the subscriber cert
openssl x509 -req -in /test/certs/subscriber.csr -out /test/certs/subscriber.crt -CA /test/certs/CA.crt -CAkey /test/certs/CA.key -CAcreateserial -days 365

# modify file permissions
chmod 777 certs/*

# generate a flag
touch /db/data/flag.txt

# execute mosquitto MQTT subscriber
while [ 1 ]; do
    for ((i=1;i<=20;i++))
    do
        # generate a log file
        touch /db/data/logfile$i.txt
        # continuous subscription for 3 minutes
        mosquitto_sub -h $BROKER_IP -t test/sensor1 -q 0 -i "Client_sub" -k 600 -W 180 \
        --tls-version tlsv1.3 --cafile /test/certs/CA.crt \
        --cert /test/certs/subscriber.crt --key /test/certs/subscriber.key >> /db/data/logfile$i.txt && echo "success" || echo "fail"
        echo $i > /db/data/flag.txt
        sleep 1
    done
done
