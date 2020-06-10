# Script: file_type_sig.py 
# Desc:   Check file type signature against filename extension.
# Author: Petra L & Rich McF
# Modifed: Nov 2018 (PEP8 compliance) 
#

'''The code of this script is entirely based on the code found in the lab9 (CSN08114) by Petra L & Rich McF'''


import sys 
import os 
import binascii 

 
file_sigs = {b'\xFF\xD8\xFF': ('JPEG', '.jpg'), b'\x47\x49\x46': ('GIF', '.gif'),
             b'\x89\x50\x4E': ('PNG', '.png'), b'\x42\x4D': ('BMP', '.bmp'),
             b'\x50\x4B\x03': ('DOCX', '.docx'), b'\x25\x50\x44': ('PDF', '.pdf')} 

 
 

def check_sig(filename): 
    """checks the file type signature of the file passed in as arg, 
    returning the type of file and correct extension in a tuple """ 
    #print('\n[*] check_sig()')
 
    try:
        # Read File 
        fh = open(filename, 'rb')
        file_sig = fh.read(3)
        fh.close()
        print(f'\n[+] File: {filename} Sig: {binascii.hexlify(file_sig)}') 

    except FileNotFoundError:
        print(f'[!] Error: {filename} not found.')
        pass
    except PermissionError as err:
        print(f'[!] Error: {err}')
        pass
    else:    
        # Check for file type sig 
        if file_sig not in file_sigs:
            print('\t[-] File type not identified - file sig not in database')
            return (-1,",")

     
        # File Type Sig found, so get sig and ext from file_sigs dic 

        elif file_sig in file_sigs:
            file_type = file_sigs[file_sig][0]
            print(f'\t[-] File type identified as {file_type}')
            print(f'\t[-] Extension: {os.path.splitext(filename)[1]}')
            file_ext = file_sigs[file_sig][1]
            if os.path.splitext(filename)[1].lower() == file_ext:
                print('\t[+] OK - valid extension for this file type')
                return (0,file_type,file_ext)
            #if statement to accept .jpeg extension as a valid extension for JPEG files
            elif os.path.splitext(filename)[1].lower() == '.jpeg' or os.path.splitext(filename)[1].lower() == '.JPEG' and file_type == b'\xFF\xD8\xFF':
                print('\t[+] OK - valid extension for this file type')
                return (0,file_type,file_ext)
            else:
                print(f'\t[!] Expected : {file_ext}. Investigation recommended.') 
                return (-2,file_type,file_ext) 
 

 

def main(): 
    # temp testing url argument 
    sys.argv.append(r'c:\Retrieved_files\msc_asdf_logo.jpeg') 
 
    # Check args 
    if len(sys.argv) != 2: 
        print('usage: file_sig filename') 
        sys.exit(1) 

 
    file_hashsig = check_sig(sys.argv[1]) 

 

if __name__ == '__main__': 
    main() 
