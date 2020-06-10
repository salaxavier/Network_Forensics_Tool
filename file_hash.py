# Script: file_hash.py
# Desc:   Generate file hash signature
# Author: Petra L & Rich McF
# modified: 2/12/18 (PEP8 compliance)
#
import sys
import os
import hashlib


def get_hash(filename):
    """prints a hex hash signature of the file passed in as arg"""
    try:
        # Read File
        f=open(filename, 'rb')
        file=f.read()
        # Generate Hash Signature
        file_hashing = hashlib.md5(file)
        
        return file_hashing.hexdigest()

    except Exception as err:
        print(f'[-] {err}')

    finally:
        if 'f' in locals():
            f.close()


def main():
    # Test case
    sys.argv.append(r'c:\temp\a_file.txt')
    # Check args
    if len(sys.argv) != 2:
        print('[-] usage: file_hash filename')
        sys.exit(1)

    filename = sys.argv[1]
    print(get_hash(filename))


if __name__ == '__main__':
    main()
