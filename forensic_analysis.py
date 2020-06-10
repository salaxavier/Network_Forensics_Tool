# Script:   forensic_analysis.py
# Desc:     Basic forensic analysis script which compares hashes of a directory's files
#           to the ones in the badfiles dictionary and checks whether their extension
#           matches their actual file type.
# Author:   Xavier Sala 
# Modified: December 2018
#

import re, os, sys
import file_hash, file_type



def files_sig(downdir):
    '''Check if the actual file type (as given by the file signature) matches the filename extension by calling
        the check_sig() function from the file_type module'''
    print('\n\n\n\n[*] files_sig()')
    try:
        os.chdir(downdir)
        down_files = os.listdir(downdir)
        print('\t[*] Calling check_sig()...')
        for file in down_files:
            file_type.check_sig(file)
    except FileNotFoundError:
        print(f'[!] Error: Directory {downdir} not found.')
        pass


def badfiles_check(badfiles, downdir, curr_dir):
    '''Creates a bad files dictionary to compare against the hashes of the files in {downdir}'''
    print('\n\n\n\n[*] badfiles_check()')

    try:
        #Create a badfiles dictionary from the content in badfiles file
        os.chdir(curr_dir)
        bad_files={}
    except FileNotFoundError:
        print(f'\t[!] Error: Directory {curr_dir} not found.')
        pass
    
    try:
        with open(badfiles, 'r') as content:
            for line in content:
                #Pattern matches MD5 hashes between quotes, a colon and any word containing alphabetic chars, digits, dots or underscores between quotes
                match = re.search("'([a-f0-9]{32})':'([\w_\.\d]*)'", line)
                #Add match.group(1) as Key and group(2) as Value to the dictionary
                bad_files[match.group(1)] = match.group(2)                                 
    except FileNotFoundError:
        print (f'\t[!] Error: {badfiles} file not found in {curr_dir}')
        pass

    else:
        try:
            #Compare the hashes of the {downdir} files against the badfiles hashes
            #Change directory to {downdir} in order to pass its contents to the file_hash module
            os.chdir(downdir)                       
            down_files = os.listdir(downdir)
            print('\t[*] Retrieving files hashes from get_hash()...')
            for file in down_files:                 #This loop is based on the code found in Lab 9 (CSN08114) by Petra L & Rich McF
                #Get the hash of each file within the directory by calling get_hash() from the file_hash module
                hash_f = file_hash.get_hash(file)   
                if hash_f in bad_files:
                    print (f'\n[-] Bad file match: {file} matches {bad_files[hash_f]}\n \t Hash: {hash_f}')
        except FileNotFoundError as err:
            print(f'\t[!] Error: {err}')
            pass
            
        

def same_files(downdir):
    '''Compare hashes of files originally with the same name to check whether they are actually the same file'''
    print('\n\n\n\n[*] same_files()\n')

    try:
        #Change directory to {downdir} in order to pass its contents to the file_hash module
        os.chdir(downdir)
        
        down_files = os.listdir(downdir)
        hash_col={}
        name_cols=[]

        #Get the hashes of the files renamed because of name collision
        for file in down_files:
            if file.startswith('COLLISION_'):
                hash_a = file_hash.get_hash(file)
                #Sore hashes and file name in hash_col dictionary
                hash_col[hash_a] = file
                #Store the original name of the file to the name_cols list
                name_cols.append(file.split('COLLISION_')[-1])

        #Get the hashes of the files which kept the original name but matched other file names
        for name in name_cols:
            hash_b = file_hash.get_hash(name)
            #Compare the hashes of the original named files with those from renamed files
            if hash_b in hash_col:
                print (f'[!] File match: {name} matches {hash_col[hash_b]}\n \t Hash: {hash_b}')
                
            else:
                print (f'[-] File {name} does not match COLLISION_{name}')
            
    except Exception as err:
        print(f'\t[!] Error: {err}')






def main():
    badfiles = 'badfiles.txt'
    downdir = r'C:\Retrieved_files'
    curr_dir = os.getcwd()
    files_sig(downdir)
    badfiles_check(badfiles, downdir, curr_dir)
    same_files(downdir)



if __name__ == '__main__':
    main()
