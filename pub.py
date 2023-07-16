#!/usr/bin/python3
import socket
import time
import datetime
import sys


# read the arguments passed
for index, i in enumerate(sys.argv):
    if i == "-i":
        PUB_ID = sys.argv[index + 1]  # PUB id
    elif i == "-r":
        PORT_P = sys.argv[index + 1]  # PORT PUB
    elif i == "-h":
        HOST = sys.argv[index + 1]  # localhost
    elif i == "-p":
        PORT_B = sys.argv[index + 1]  # PORT BROKER
    elif i == "-f":
        commandFile = sys.argv[index + 1]  # The command file


# global variables
commands = []

with open(f"./{commandFile}", "r") as command_file:
    for line in command_file:
        commands.append(line)
        print(commands)


def main():
    # connect to server and send and receive the data
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        sock.connect((HOST, int(PORT_B)))
        print("Connection ok")
    except:
        print("Connection failed")

    while True:
        for command in commands:
            time.sleep(int(command.split()[0]))
            # print(datetime.datetime.now())
            sock.sendall(bytes(PUB_ID + command[len(command.split()[0]):len(command)] + "\n", "utf-8"))
            # receive the data
            received = str(sock.recv(1024), "utf-8")
            print("Received: " + received)

        # input from keybord: The same as the command file
        while True:
            keyboard = input("Another command, if not Exit: ")
            if keyboard.upper() == "EXIT":
                break
            time.sleep(int(keyboard.split()[0]))
            sock.sendall(bytes(PUB_ID + keyboard[len(keyboard.split()[0]):len(keyboard)] + "\n", "utf-8"))
            # receive the data
            received = str(sock.recv(1024), "utf-8")
            print("Received: " + received)
        break


if __name__ == "__main__":
    main()
