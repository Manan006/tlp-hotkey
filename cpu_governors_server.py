import os
import time
import zmq 
from config import commands

if __name__=="__main__":
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:6969")
    os.system("sysctl vm.swappiness=10")
    while True:
        cmd = socket.recv_string()
        print(cmd)
        for command in commands:
            print(command)
            print(cmd[len(str(command["start"])):-len(str(command["end"]))])
            if cmd.startswith(str(command["start"])) and cmd.endswith(str(command["end"])) and cmd[len(str(command["start"])):-len(str(command["end"]))] in command["args"]:
                socket.send_string(str(os.system(cmd)))
                break
        else:
            socket.send_string("69")
        time.sleep(0.5)
