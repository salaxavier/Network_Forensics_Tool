# Script:  hashes_crack.py
# Description: Cracks password hash using a dictionary attack.
# Author: Petra L & Rich McF (Adapted by Xavier Sala)
# Modified: December 2018 

'''The code of this script is entirely based on the script dict_crack.py made by Petra L & Rich McF'''


import hashlib
def get_rainbow(dictionary):
    try:
        #Read the dictionary file which contains a list of common passwords
        dic = [s.strip('\n') for s in open(dictionary, 'r')]

        # create list of corresponding md5 hashes using a list comprehension
        hashes = [hashlib.md5(pwd.encode('utf-8')).hexdigest() for pwd in dic] 

        # zip dic and hashes to create a dictionary (rainbow table)
        rainbow = dict(zip(hashes,dic)) 
        return rainbow
    
    except FileNotFoundError:
        print(f'[!] Error: {dictionary} not found in {os.getcwd()}')



def dict_attack(passwd_hash, dictionary):
    """Checks password hash against a dictionary of common passwords"""
    #print('\n\n\n\n[*] dict_attack()')
    
    passwd_found = get_rainbow(dictionary).get(passwd_hash) 
        
    if passwd_found:
        print (f'[+]Cracking hash: {passwd_hash}    Password recovered: {passwd_found}')
    else:
        print (f'[-]Cracking hash: {passwd_hash}    Password not recovered')






def main():
    
    #passwd_hash = '5c916794deca0f7c3eeaee426b88f8bd'
    passwd_hash = 'ae4e20ba64f111a3be58a5d207de27bf'
    dictionary = 'dictionary.txt'
    dict_attack(passwd_hash, dictionary)


    
if __name__ == '__main__':
	main()
