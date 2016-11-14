#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""UDP Client Program that sends a SIP method request."""

import socket
import sys


try:
    METHOD = sys.argv[1]
    LOGIN = sys.argv[2]
    if len(sys.argv) != 3:
        raise IndexError
except (IndexError, ValueError):
    sys.exit("Usage: python client.py method receiver@IP:SIPport")

# Server IP address & port. We got it by splitting LOGIN values.
SERVER_IP = LOGIN.split("@")[1].split(":")[0]
PORT = int(LOGIN.split("@")[1].split(":")[1])
LOGIN = LOGIN.split("@")[0] + "@127.0.0.1"

# Content to send.
SIP_LINE = METHOD + " sip:" + LOGIN + " SIP/2.0\r\n\r\n"

if __name__ == "__main__":
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as my_socket:
            my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            my_socket.connect((SERVER_IP, PORT))
            print(SIP_LINE)
            my_socket.send(bytes(SIP_LINE, 'utf-8'))
            data = my_socket.recv(1024)
            print('-- RECIEVED SIP INFO --\n' + data.decode('utf-8'))
            if data.decode('utf-8').split(" ")[-1] == "OK\r\n\r\n":
                SIP_ACK = "ACK" + " sip:" + LOGIN + " SIP/2.0\r\n\r\n"
                my_socket.send(bytes(SIP_ACK, 'utf-8'))
                data = my_socket.recv(1024)
                print(data.decode('utf-8'))
            my_socket.close()
            print("END OF SOCKET")
    except ConnectionRefusedError:
        print("Connection Refused. Server not found.")
