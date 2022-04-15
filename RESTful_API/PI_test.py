import os
import time
import requests
import threading
import json

filename="/db/data/logfile.txt"
fg = 0
global b_time
global a_time

#key
SecureKey = "NoKey"
#url
Restful_URL = "https://data.lass-net.org/Upload/MAPS-secure.php?"
#APP ID
APP_ID = "MAPS6"

def upload_task():
    while True:
        global fg
        time.sleep(10)
        
        # the file modified time
        b_time = os.stat(filename).st_mtime

        if fg == 0:
            print("")
        elif int(b_time)!=int(a_time):
            # read data
            with open(filename, 'r') as f:
                firstline = f.readline().rstrip()

            # data cleaning
            mqtt_msg=""
            str1 = firstline.strip('{}').split(',')
            for i in str1:
                if(i[0:4] == 'time'):
                    mqtt_msg = mqtt_msg + "," + "\"" + i.split(':')[0] + "\"" + ":" + "\"" + i.split(':')[1] \
                    + ":" + i.split(':')[2] + ":" + i.split(':')[3] + "\""
                else:
                    mqtt_msg = mqtt_msg + "," + "\"" + i.split(':')[0] + "\"" + ":" + "\"" + i.split(':')[1] + "\""  
            mqtt_msg = "{" + mqtt_msg + "}" 
            mqtt_msg = mqtt_msg.replace(",", "", 1)
            print(mqtt_msg)  # "{"s_t0":"26.38","app":"MAPS6","date":"2022-04-12","s_d0":"4","s_h0":"52.0","device_id":"B827EB8E9774","s_gg":"1","ver_app":"6.4.3-a","time":"09:09:31"}"
            data = json.loads(mqtt_msg)

            msg = ""

            # if((data['gps_lat'] != "") and (data['gps_lon'] != "")):
            #     msg = msg + "|gps_lon=" + data['gps_lon'] + "|gps_lat=" + data['gps_lat']
            # if(data['s_g8'] != 65535):
            #     msg = msg + "|s_g8=" + data['s_g8']

            msg = msg + "|s_t0=" + data['s_t0'] + "|app=" + data['app'] + "|date=" + data['date'] + "|s_d0=" + data['s_d0'] + "|s_h0=" + data['s_h0'] + "|device_id=" + data['device_id'] + "|s_gg=" + data['s_gg'] + "|ver_app=" + data['ver_app'] + "|time=" + data['time']

            # if((data['s_s0L'] != 0) and (data['s_s0L'] != float("inf"))):
            #     msg = msg + "|s_s0=" + data['s_s0'] + "|s_s0M=" + data['s_s0M'] + "|s_s0m=" + data['s_s0m'] + "|s_s0L=" + data['s_s0L']

            print("message ready")

            restful_str = Restful_URL + "topic=" + APP_ID + "&device_id=" + data['device_id'] + "&key=" + SecureKey + "&msg=" + msg
            try:
                r = requests.get(restful_str)
                print("send result")
                print(r)
                print("message sent!")
            except:
                print("internet err!!")

        # store the file modified time
        a_time = b_time
        fg = 1

#start upload routine
upload_task()

#start upload routine
# upload_t = threading.Thread(target = upload_task, name = "upload_t")
# upload_t.setDaemon(True)

#start routine job
# upload_t.start()
