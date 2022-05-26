import os
import time
import requests
import threading
import json

filename="/db/data/logfile"
svname="/db/data/flag.txt"
flg=0
global b_time
global a_time

#secure key
SecureKey = "NoKey"
#server url
Restful_URL = "https://data.lass-net.org/Upload/MAPS-secure.php?"
#APP ID
APP_ID = "MAPS6"

def clean_data(data1):
    mqtt_msg=""
    str1 = data1.strip('{}').split(',')
    for i in str1:
        if(i[0:4] == 'time'):
            mqtt_msg = mqtt_msg + "," + "\"" + i.split(':')[0] + "\"" + ":" + "\"" + i.split(':')[1] \
            + ":" + i.split(':')[2] + ":" + i.split(':')[3] + "\""
        else:
            mqtt_msg = mqtt_msg + "," + "\"" + i.split(':')[0] + "\"" + ":" + "\"" + i.split(':')[1] + "\""  
    mqtt_msg = "{" + mqtt_msg + "}" 
    mqtt_msg = mqtt_msg.replace(",", "", 1)
    # print(mqtt_msg)
    data = json.loads(mqtt_msg)

    msg = ""

    if(('gps_lat' in data) and ('gps_lon' in data)):
        msg = msg + "|gps_lon=" + data['gps_lon'] + "|gps_lat=" + data['gps_lat']
    if('s_g8' in data):
        msg = msg + "|s_g8=" + data['s_g8']

    msg = msg + "|s_t0=" + data['s_t0'] + "|app=" + data['app'] + "|date=" + data['date'] + "|s_d0=" + data['s_d0'] + "|s_h0=" + data['s_h0'] + "|device_id=" + data['device_id'] + "|s_gg=" + data['s_gg'] + "|ver_app=" + data['ver_app'] + "|time=" + data['time']

    if('s_s0L' in data):
        msg = msg + "|s_s0=" + data['s_s0'] + "|s_s0M=" + data['s_s0M'] + "|s_s0m=" + data['s_s0m'] + "|s_s0L=" + data['s_s0L']

    print(msg)
    print("message ready")
    restful_str = Restful_URL + "topic=" + APP_ID + "&device_id=" + data['device_id'] + "&key=" + SecureKey + "&msg=" + msg
    return restful_str


def upload_task():
    while True:
        global flg
        # the flag file modified time
        if (os.path.isfile(svname)):
            b_time = os.stat(svname).st_mtime
        time.sleep(1)

        if flg == 0:
            print("")
        elif int(b_time)!=int(a_time):    # if flag changes
            try:
                print("Start!!")
                # get flag number
                with open(svname, 'r') as f:
                    cnt = f.readline().rstrip()
                
                arr=[]
                # read data
                with open(filename + cnt + ".txt", 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        # print(line)
                        arr.append(line.rstrip())
                
                # clean & send data
                for i in arr:
                    x = clean_data(i)
                    r = requests.get(x)
                    print("send result")
                    print(r)
                    print("message sent!")
                
                # remove logfile
                os.remove(filename + cnt + ".txt")
            except Exception as e:
                print(e,type(e))
                err = 'db/data/err.txt'
                with open(err, 'a') as f:
                    f.write(e + " " + type(e))
        
        # store the file modified time
        a_time = b_time
        flg = 1

#start upload routine
upload_task()

#start upload routine
# upload_t = threading.Thread(target = upload_task, name = "upload_t")
# upload_t.setDaemon(True)

#start routine job
# upload_t.start()
