#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""UDP Client Program that sends a RTP mp3 song."""

import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):
    """Main handler to send a RTP audio stream."""

    def handle(self):
        """Handler to manage incoming users SIP request."""
        line = self.rfile.read()
        line_str = line.decode('utf-8')
        line_print = line_str.split(" ")
        if line_str.split(" ")[0] == "INVITE":
            self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
            self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif line_str.split(" ")[0] == "ACK":
            if len(line_print) != 3:
                self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
            else:
                send = "mp32rtp -i 127.0.0.1 -p 23032 < " + sys.argv[3]
                os.system(send)
        elif line_str.split(" ")[0] == "BYE":
            self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
        elif line_str.split(" ")[0] != "":
            self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
        print(line_str)


if __name__ == "__main__":
    try:
        IP = sys.argv[1]
        PORT = int(sys.argv[2])
        AUDIO_FILE = sys.argv[3]
        if not os.path.exists(AUDIO_FILE):  # Does this audio file exists?
            raise OSError
        if len(sys.argv) != 4:
            raise IndexError
        serv = socketserver.UDPServer((IP, PORT), SIPHandler)
        print("Listening...")
        serv.serve_forever()
    except (IndexError, ValueError, OSError):
        sys.exit("Usage: python server.py IP port audio_file")
    except KeyboardInterrupt:
        print("END OF SERVER")
