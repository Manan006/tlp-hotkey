import zmq
import time 
import os
from pynput import keyboard
from config import *
from pynput.keyboard import Key,KeyCode
from plyer import notification

def send_notification(title:str,message:str):
    notification.notify(
    title = title,
    message = message,
    app_icon = f"{path}/icon.ico",
    timeout = 10)
COMBINATIONS = [
    {"keys":[Key.ctrl,Key.alt, KeyCode(char='1')],"governor":"powersave","is_aggressive":True,"tlp_file":"tlp_powersave.conf"},
    {"keys":[Key.ctrl,Key.alt, KeyCode(char='2')],"governor":"conservative","is_aggressive":False},
    {"keys":[Key.ctrl,Key.alt, KeyCode(char='3')],"governor":"ondemand","is_aggressive":False},
    {"keys":[Key.ctrl,Key.alt, KeyCode(char='4')],"governor":"performance","is_aggressive":True,"tlp_file":"tlp_performance.conf"}
]
def copy_files(source:str,destination:str):
    send_to_server(cp_format.replace("%source",source).replace("%destination",destination))

def on_press(key):
    if any([key in COMBO["keys"] for COMBO in COMBINATIONS]):
        current.add(key)
        for COMBO in COMBINATIONS:
            combo_check_list=[key in current for key in COMBO["keys"]]
            if all(combo_check_list):
                execute(COMBO) 
                break

def on_release(key):
    if any([key in COMBO["keys"] for COMBO in COMBINATIONS]):
        try:
            current.remove(key)
        except KeyError:
            pass

def startup():
    time.sleep(wait_on_startup)
    if not startup_combo==None:
        COMBO=COMBINATIONS[startup_combo]
        execute(COMBO)

def execute(COMBO:dict):
    governor=COMBO["governor"]
    is_aggressive=COMBO["is_aggressive"]
    print(governor,is_aggressive)
    if is_aggressive:
        codes=[send_to_server(f"/usr/bin/echo '{governor}' | /usr/bin/tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")]
        codes.append(copy_files(os.path.join(path,COMBO["tlp_file"]),"/etc/tlp.conf"))
        codes.append(send_to_server(tlp_restart))
        if any(codes):
            send_notification("Unsuccessful",f"Exit code : {str(codes)}\nUnsuccessfully changed to mode {governor}")
        else:
            send_notification(str(governor),f"Successfully changed to mode {str(governor)}")
    else:
        codes=[send_to_server(f"/usr/bin/echo '{governor}' | /usr/bin/tee /sys/devices/system/cpu/cpu*/cpufreq/scaling_governor")]
        codes.append(copy_files(os.path.join(path,tlp_default),"/etc/tlp.conf"))
        codes.append(send_to_server(tlp_restart))
        if any(codes):
            send_notification("Unsuccessful",f"Exit codes : {str(codes)}\nUnsuccessfully changed to mode {governor}")
        else:
            send_notification(str(governor),f"Successfully changed to mode {str(governor)}")

def send_to_server(cmd:str):
    print(cmd)
    socket.send_string(cmd)
    return int(socket.recv_string())

if __name__=="__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect("tcp://localhost:6969")
    startup()
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()