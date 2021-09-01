#!/usr/bin/python3
# Version 1.0

import os

def generate (folder):
    data = {}
    headers = []

    # Read the data
    with open(f'{folder}/pdfdata.txt','r') as f:
        _i_no,_name,_msb,_lsb,_pc = 0,0,0,0,0
        first_line = True
        curheader = ''
        for line in f.readlines():
            entries = line.strip().split(' ')
            if len(entries) == 0 or entries[0] == '' or entries[0] == '\n': # detect and skip empty lines
                continue
            # Read the file description
            if first_line:
                p = False
                for i in range(len(entries)):
                    i_use = i
                    if p or entries[i]=='name':
                        i_use = -len(entries) + i
                        p = True
                    if entries[i] == 'i_no':
                        _i_no = i_use
                    if entries[i] == 'msb':
                        _msb  = i_use
                    if entries[i] == 'lsb':
                        _lsb  = i_use
                    if entries[i] == 'pc':
                        _pc   = i_use
                    if entries[i] == 'name':
                        if i != len(entries)-1:
                            _name = slice(i,i_use+1,1)
                        else:
                            _name = slice(i,None,1)
                first_line = False
                print('layout',line,_i_no,_name,_msb,_lsb,_pc)
                continue
            # Read a copy-pasted entry
            entries[_i_no] = entries[_i_no].replace('*','') # edge case for psr data
            if entries[0].isdigit():
                # this is an instrument
                i_no = int(entries[_i_no])
                name = ' '.join(entries[_name])
                msb  = int(entries[_msb])
                lsb  = int(entries[_lsb])
                pc   = int(entries[_pc])-1

                info = f'{pc} ({curheader}) {name}'
                
                if not msb in data:
                    data[msb] = {}
                if not lsb in data[msb]:
                    data[msb][lsb] = [None] * 128
                data[msb][lsb][pc] = info
            else:
                # this is a bank header
                curheader = line.strip()
                headers.append(curheader)
                print(curheader)

    # Create the .reabank file
    def gen_reabank(head=''):
        fn = f'{folder}/{folder}.reabank'
        if head != '':
            fn = f'{folder}/{folder}({head.replace(".","")}).reabank'
        with open(fn,'w') as f:
            f.write("// Generated using using rea-parse.py\n")
            msb_keys = list(data.keys())
            msb_keys.sort()
            for msb in msb_keys:
                lsb_keys = list(data[msb].keys())
                lsb_keys.sort()
                for lsb in lsb_keys:
                    bw = False
                    for u in data[msb][lsb]:
                        if u != None and (head=='' or f'({head})' in u):
                            if not bw: # Adds bank only if we are using instruments from it
                                f.write(f'Bank {msb} {lsb} {msb} {lsb}\n')
                                bw = True
                            f.write(f'{u}\n')
                            
    gen_reabank()
    for head in headers:
        gen_reabank(head)

# Call the functions for the keyboards we want to parse
for i in os.listdir():
    if os.path.isdir(i):
        if 'pdfdata.txt' in os.listdir(i):
            print("Generating banks for ",i)
            generate(i)