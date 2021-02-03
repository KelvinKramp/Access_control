import subprocess
import os
import time
from datetime import datetime as dt
import threading as thr

# FIRST ADD THE FOLLOWING TO YOUR settings.py TO CREATE A deboug.log FILE THAT TRACKS THE OUTPUT
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'DEBUG',
#             'class': 'logging.FileHandler',
#             'filename': 'debug.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'DEBUG',
#             'propagate': True,
#         },
#     },
# }

# TO USE THE SCRIPT IN YOUR DJANGO APPLICATION WRITE "from inactivity_tracker_Django import start_timer_thread" IN YOUR APPLICATION FILE AND START THE MODULE WITH start_timer_thread() SOMEWHERE IN THE BEGINNING OF YOUR APPLICATION FILE


# FUNCTION FOR KILLING THE LOCAL SERVER
def kill_server():
    subprocess.run("lsof -t -i tcp:8000 | xargs kill -9", shell=True) # kill the server

# FUNCTION FOR TRACKING LAST MODIFCATION DATE OF FILE
def modification_date(filename):
    t = os.path.getmtime(filename) # get the last time moment of change of the file
    return dt.fromtimestamp(t)

# FUNCTION FOR TRACKING TIME AND KILLING DJANGO LOCAL SERVER
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
        if count_time > 5: # KILL SCRIPT AFTER 5 TIMES 60 SECONDS, ADJUST TO CREATE A LONGER INACTIVTY TRESHOLD
            break
    kill_server()

# CREATE A PAUSE BEFORE RUNNING THE SCRIPT TO PREVENT DOING THINGS WHILE THE SERVER IS NOT RUNNING YET
def timer():
    time.sleep(10) # sleep untill server is running
    track_time()

# START THE INACTIVITY TIME TRACKER ON THE BACKGROUND AS A THREAD.  
def start_timer_thread():
    timer_thread = thr.Thread(target=timer)
    timer_thread.start()
