#!/usr/bin/python3
import threading
import socket
import sys
import time
import queue
from os import path


# read the arguments passed
HOST = "localhost"
for index, i in enumerate(sys.argv):
    if i == "-p":
        P_PORT = sys.argv[index + 1]  # PORT for pubs
    elif i == "-s":
        S_PORT = sys.argv[index + 1]  # PORT for subs


# global variables
publishes = []

# thread for publisher
def pubthread():
    global publishes
    # set up for publisher
    pub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    pub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        pub_sock.bind((HOST, int(P_PORT)))
        print("The connection with the Publisher is ok")
    except:
        print("Connection failed")

    pub_sock.listen(20)
    print("Broker listening Pubs on %s %d" % (HOST, int(P_PORT)))

    conn, addr = pub_sock.accept()
    print("Pub Connected : " + addr[0] + ":" + str(addr[1]))

    while True:
        try:
            data = conn.recv(1024).strip().decode('UTF-8') # περιμενει και δεν προχωραει
            data_new = data.replace(f"{data.split()[0]} pub ", "")
            message = data_new.replace(f"{data_new.split()[0]}", "")
            print("Received from Pub: " + data)
            conn.sendall(bytes(f"OK Published msg for topic {data_new.split()[0]} : {message}", "utf-8"))

            with open("./subscriptions.txt", "r") as subscriptions_file:
                sub_lines = subscriptions_file.readlines()
                for line in sub_lines:
                    if (data.split()[2] in line) and line.split()[1] == "sub":
                        # publishes.put(data_new)
                        for i in publishes:
                            i.sendall(bytes(f"Received msg for topic {data_new.split()[0]} : {message}", "utf-8"))

        except:
            print("Pub Disconnected")
            break


# thread for subscriber
def subthread():
    global publishes

    # set up for subscriber
    sub_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sub_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        sub_sock.bind((HOST, int(S_PORT)))
        print("The connection with the Subscriber is ok")
    except:
        print("Connection failed")

    sub_sock.listen(10)
    print("Broker listening Subs on %s %d" % (HOST, int(S_PORT)))

    conn_sub, addr = sub_sock.accept()
    publishes.append(conn_sub)
    print("Sub Connected : " + addr[0] + ":" + str(addr[1]))

    while True:
        try:
            print("Wait for sub data")
            # use decode to change data from bytes to string
            data = conn_sub.recv(1024).strip().decode('UTF-8')
            # client closed the connection
            if not data:
                break
            print("Received from Sub: " + str(data))
            conn_sub.sendall(bytes(f"OK {data.split()[1]} {data.split()[2]}", "utf-8"))

            with open("./subscriptions.txt", "r") as subscriptions_file:
                sub_lines = subscriptions_file.readlines()
                for line in sub_lines:
                    if data.split()[2] in line:
                        sub_lines.remove(line)
                        break

            sub_lines.append(data + "\n")
            with open("./subscriptions.txt", "w") as subscriptions_file:
                for line in sub_lines:
                    subscriptions_file.write(line)

        except:
            print("Sub Disconnected")
            break


def main():  # with threading are running in parallel two different parts pubthread/subthread
    try:
        # create a subscriptions.txt if not exists in the directory the project is executed
        if not path.exists("subscriptions.txt"):
            with open("./subscriptions.txt", "w") as fp:
                pass

        pud_thread = threading.Thread(target=pubthread)
        pud_thread.start()
        sub_thread = threading.Thread(target=subthread)
        sub_thread.start()

        pud_thread.join()
        sub_thread.join()

        print("Broker closed")

    except KeyboardInterrupt as msg:
        sys.exit(0)


if __name__ == "__main__":
    main()
