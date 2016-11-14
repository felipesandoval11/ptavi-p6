#!/usr/bin/python3
# -*- coding: utf-8 -*-
# Made by Felipe Sandoval Sibada
"""UDP Client Program that sends a RTP mp3 song."""

import socketserver
import sys
import os


class SIPHandler(socketserver.DatagramRequestHandler):
    """Main handler to send a RTP audio stream."""
    
    line_number = 0  # for distinct use in ack
    
    def handle(self):
        """Handler to manage incoming users SIP request."""
        while 1:
            # Leyendo línea a línea lo que nos envía el cliente
            line = self.rfile.read()
            line_str = line.decode('utf-8')
            print(line_str)
            if line_str.split(" ")[0] == "INVITE": 
                self.wfile.write(b"SIP/2.0 100 Trying\r\n\r\n")
                self.wfile.write(b"SIP/2.0 180 Ringing\r\n\r\n")
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif line_str.split(" ")[0] == "ACK":
                if self.line_number == 0:
                    self.wfile.write(b"SIP/2.0 400 Bad Request\r\n\r\n")
                else:
                    send = "mp32rtp -i 127.0.0.1 -p 23032 < " + sys.argv[3]
                    os.system(send)
            elif line_str.split(" ")[0] == "BYE":
                self.wfile.write(b"SIP/2.0 200 OK\r\n\r\n")
            elif line_str.split(" ")[0] != "":
                self.wfile.write(b"SIP/2.0 405 Method Not Allowed\r\n\r\n")
            
            print(line_str)
            print(self.line_number)
            self.line_number += 1
            # Si no hay más líneas salimos del bucle infinito
            if not line:
                break

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
