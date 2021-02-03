import subprocess
import os
import time
from datetime import datetime as dt
import threading as thr

def kill_server():
    subprocess.run("lsof -t -i tcp:8000 | xargs kill -9", shell=True) # kill the server

def modification_date(filename):
    t = os.path.getmtime(filename) # get the last time moment of change of the file
    return dt.fromtimestamp(t)

def track_time():
    time_modification_old = None
    count_time = 0
    while True:
        time_modification = modification_date("debug.log")
        print("last time use of script =", time_modification)
        if time_modification_old != None:
            time_modification_delta = time_modification_old - time_modification
            delta = time_modification_delta.total_seconds()
            if int(delta) == 0:
                count_time +=1
                print("you did not use script for", count_time, "minutes, script will be killed at 5 minutes inactivity")
            else:
                count_time = 0
        time_modification_old = time_modification
        time.sleep(60)
        if count_time > 5:
            break
    kill_server()

def timer():
    time.sleep(10) # sleep untill server is running
    track_time()

def start_timer_thread():
    timer_thread = thr.Thread(target=timer)
    timer_thread.start()