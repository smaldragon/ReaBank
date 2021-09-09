#!/usr/bin/python3
# Version 1.0

import os

def generate (folder):
    data = {}
    headers = []

    # Read the data
    with open(f'{folder}/pdfdata.txt','r') as f:
        dati = {}
        brak = []
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
                    e = entries[i]
                    if e[0] == '(':
                        e = e[1:-1]
                        brak.append(e)
                    if e in ['i_no','msb','lsb','pc']:
                        dati[e] = i_use
                    elif e == 'name':
                        if i != len(entries)-1:
                            dati[e] = slice(i,i_use+1,1)
                        else:
                            dati[e] = slice(i,None,1)
                first_line = False
                print('layout',dati)
                continue
            # Read a copy-pasted entry
            if len(entries) > dati['i_no']:
                entries[dati['i_no']] = entries[dati['i_no']].replace('*','') # edge case for psr data
            def grab(dat):
                d = dati[dat]
                if type(d) != slice:
                    if d >= len(entries):
                        return ""
                print(d,entries)
                if dat in brak and entries[d][0] == "(":
                    return entries[d][1:-1]
                else:
                    return entries[d]
            
            if grab('i_no').isdigit():
                # this is an instrument
                i_no = int(grab('i_no'))
                name = ' '.join(grab('name'))
                msb  = int(grab('msb'))
                lsb  = int(grab('lsb'))
                pc   = int(grab('pc'))-1
                
                heada = curheader
                if heada != '':
                    heada = f'({heada}) '
                info = f'{pc} {heada}{name}'
                
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