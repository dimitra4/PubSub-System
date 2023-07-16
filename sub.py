#!/usr/bin/python3
import socket
import sys
import time
import threading


# read the arguments passed
for index, i in enumerate(sys.argv):
    if i == "-i":
        SUB_ID = sys.argv[index + 1]  # SUB id
    elif i == "-r":
        PORT_S = sys.argv[index + 1]  # PORT SUB
    elif i == "-h":
        HOST = sys.argv[index + 1]  # localhost
    elif i == "-p":
        PORT_B = sys.argv[index + 1]  # PORT BROKER
    elif i == "-f":
        commandFile = sys.argv[index + 1]  # The command file


# global variables
commands = []
received_ok = False

with open(f"./{commandFile}", "r") as command_file:
    for line in command_file:
        commands.append(line)
        # print(commands)

def receivedthread(sock):
    global received_ok
    # receive the data
    while True:
        received = str(sock.recv(1024), "utf-8")
        if "OK" in received:
            received_ok = True
            print("Received " + received)
        else:
            print(received)

def main():
    global received_ok
    # connect to server and send and receive the data twice
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((HOST, int(PORT_B)))

    # start new thread for receiving the data with args the socket created above
    thread = threading.Thread(target=receivedthread, args=(sock,))
    thread.start()

    for command in commands:
        time.sleep(int(command.split()[0]))
        # print(datetime.datetime.now())
        sock.sendall(bytes(SUB_ID + command[len(command.split()[0]):len(command)] + "\n", "utf-8"))
        while not received_ok:
            time.sleep(0.1)
        received_ok = False


    while True:
        try:
            keyboard = input("\n")
            if keyboard.upper() == "EXIT":
                break
            time.sleep(int(keyboard.split()[0]))
            sock.sendall(bytes(SUB_ID + keyboard[len(keyboard.split()[0]):len(keyboard)] + "\n", "utf-8"))
            while not received_ok:
                time.sleep(0.1)
            received_ok = False

        except:
            print("Error/Disconnect")


if __name__ == "__main__":
    main()
