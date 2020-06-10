# Script:   webpage_getdata.py
# Desc:     Web page information gathering script which retrieves image file URLs,
#           document file URLs and download them, email addresses, phone numbers and MD5 hashes
#           from the web content.
# Author:   Xavier Sala 
# Modified: December 2018
#


import re, os, urllib.request
import webpage_get, hashes_crack



#Image file's absolute links stored to this global variable in order to be passed to the download_files() function
images_sorted=[]        


def print_images(page,url):
    ''' find all hyperlinks of image files on the webpage input and print them'''
    print('\n\n\n\n[*] print_images()')

    try:
        # regex to match on hyperlinks of image files
        # pattern matches strings starting with '"' or "'" and ending with '.jpg"', '.JPG"', '.JPEG"', '.jpeg"', '.bmp"', '.BMP"', '.png"' or '.PNG"' (either single or double quotes)
        images = re.findall('(\"|\')(\S.\S*\.jpg|\S.\S*\.JPG|\S.\S*\.jpeg|\S.\S*\.JPEG|\S.\S*\.bmp|\S.\S*\.BMP|\S.\S*\.gif|\S.\S*\.GIF|\S.\S*\.png|\S.\S*\.PNG)(\"|\')', page.decode())

    except AttributeError:
        print('AttributeError')
    # Sort and print the absolute links. For printing distinguished absolute and relative links, uncomment the commented code.
    #images_sorted=[]
    #images_absolute=[]
    #images_relative=[]
    print(f'[+] {len(images)} Image Files Found:\n')

    for link in images:
        #Absolute links are appended to the sorted list
        if link[1].startswith('http') or link[1].startswith('tftp') or link[1].startswith('ftp') or link[1].startswith('www'):              
            images_sorted.append(link[1])
            #images_absolute.append(link[1])        #Store absolute links in a separate list

        #Relative links are appended to the URL and added to the sorted list
        else:
            images_sorted.append(url+link[1])       
            #images_relative.append(link[1])        #Store relative links in a separate list

    images_sorted.sort()
    #images_absolute.sort()
    #images_relative.sort()
    for link in images_sorted: print(link)
    #for link in images_absolute: print(link)
    #for link in images_relative: print(link)




#Document file's absolute links stored to this global variable in order to be passed to the download_files() function
docs_sorted=[]          


def print_docs(page,url):
    ''' find all hyperlinks of document files on the webpage input and print them'''
    print('\n\n\n\n[*] print_docs()')
    # regex to match on hyperlinks of document files

    # pattern matches strings starting with '"' or "'" and ending with '.doc"', '.DOC"', '.docx"', '.DOCX"', '.pdf"' or '.PDF"' (either single or double quotes)
    docs = re.findall('(\"|\')(\S.\S*\.pdf|\S.\S*\.PDF|\S.\S*\.docx|\S.\S*\.DOCX|\S.\S*\.doc|\S.\S*\.DOC)(\"|\')', page.decode())

    # Sort and print the absolute links. For printing distinguished absolute and relative links, uncomment the commented code.
    #docs_sorted=[]
    #docs_absolute=[]
    #docs_relative=[]
    print(f'[+] {len(docs)} Document Files Found:\n')

    for link in docs:
        #Absolute links are appended to the sorted list
        if link[1].startswith('http') or link[1].startswith('tftp') or link[1].startswith('ftp') or link[1].startswith('www'):              
            docs_sorted.append(link[1])
            #docs_absolute.append(link[1])           #Store absolute links in a separate list

        #Relative links are appended to the URL and added to the sorted list
        else:
            docs_sorted.append(url+link[1])         
            #docs_relative.append(link[1])           #Store relative links in a separate list

    docs_sorted.sort()
    #docs_absolute.sort()
    #docs_relative.sort()
    for link in docs_sorted: print(link)
    #for link in docs_absolute: print(link)
    #for link in docs_relative: print(link)






def print_email(page):
    ''' find all email addresses on the webpage input and print them'''
    print('\n\n\n\n[*] print_email()')
    # regex to match on email addresses

    #pattern matches strings with an unknown number of characters [a-zA-Z0-9.-_] followed by @ and an unknown number of characters [a-zA-Z0-9.-_]
    email = re.findall('[\w\.\-\_]*@[\w\.\-\_]*', page.decode())
    #pattern matches strings starting with "mailto:" followed by an unknown number of characters [a-zA-Z0-9.-_], an @ and an unknown number of characters [a-zA-Z0-9.-_]
    email_mailto = re.findall('(mailto\:)([\w\.\-\_]*@[\w\.\-\_]*)', page.decode())

    # sort and print the email addresses
    email_mailto_sorted=[]
    email_freetext_sorted=[]
    
    for addr in email_mailto:
        #regex match is compared with the existing emails in email_mailto_sorted to avoid duplications
        if addr[1] == addr in email_mailto_sorted:          
            pass
        else:
            email_mailto_sorted.append(addr[1])             

    '''regex match is compared with the existing emails in email_mailto_sorted to discard those
       which do not belong to the "free text" group. Then, it is compared to the existing addresses
       within email_freetext_sorted in order to avoid duplicates'''
    for addr in email:
        if addr == addr in email_mailto_sorted or addr == addr in email_freetext_sorted:             
            pass                                                                               
        else:                                                                                   
            email_freetext_sorted.append(addr)

    print(f'[+] {len(email_mailto_sorted)+len(email_freetext_sorted)} eMail Addresses Found:')
    email_mailto_sorted.sort()
    email_freetext_sorted.sort()
    print(f'\n [-] {len(email_mailto_sorted)} "mailto:" addresses found:')
    for addr in email_mailto_sorted: print(addr)
    print(f'\n [-] {len(email_freetext_sorted)} "free text" addresses found:')
    for addr in email_freetext_sorted: print(addr)






def print_phones(page,url):
    ''' find all phone numbers on the webpage input and print them'''
    print('\n\n\n\n[*] print_phones()')
    # regex to match on phone numbers

    # pattern matches strings starting with + and 2-4 digits, followed (or not) by (0) and a combination of numbers, spaces and dashes (between 9 and 15 chars)
    #                   OR starting with 00 and 2-4 digits, followed (or not) by (0) and a combination of numbers, spaces and dashes (between 9 and 15 chars)
    phones = re.findall('\+\d{2,4}[\- ]?[\(0\)]*[0-9\- ]{9,15}|00[ \-]?\d{2,4}[\- ]?[\(0\)]*[0-9\- ]{9,15}', page.decode())
    
    # Sort and print the phone numbers
    phones_sorted=[]
    print(f'[+] {len(phones)} Phone Numbers Found:\n')

    phones.sort()
    for num in phones: print(num)





#Global variable which stores the hashes found in order to pass them to other modules
hashes_sorted=[] 

def print_hashes(page,url):
    ''' find all the MD5 hashes on the webpage input and print them'''
    print('\n\n\n\n[*] print_hashes()')
    # regex to match on MD5 hashes

    # pattern matches strings of 32 consecutive characters a-z or 0-9
    hashes = re.findall('[a-f0-9]{32}', page.decode())
    
    # Sort and print the hashes
    print(f'[+] {len(hashes)} MD5 Hashes Found:\n')

    #Copy the hashes found to the global variable hashes_sorted
    for Hash in hashes: hashes_sorted.append(Hash)      
    hashes_sorted.sort()
    for Hash in hashes_sorted: print(Hash)





    
def recover_hashes(dictionary):
    ''' calls the dict_attack() function from the hashes_crack module
        using the contents of the hashes_sorted global variable as argument
        in order to try to crack each hash'''
    
    print('\n\n\n\n[*] recover_hashes()')

    #If hashes have been found, call dict_attack() to try to crack them
    if len(hashes_sorted) > 0:
        print('    [*] Calling dict_attack()...\n')

        for Hash in hashes_sorted:
            hashes_crack.dict_attack(Hash, dictionary)

    #Otherwise, skip it
    else:
        print ('\t [-] 0 found hashes to recover...')




def download_files(downdir):
    '''Download all the image and document files found in print_images() and print_docs() functions into the {downdir} directory'''

    print('\n\n\n\n[*] download_files()')

    if len(images_sorted) or len(docs_sorted) > 0:

        #Check whether the directory exists and create it
        try:
            #Create directory
            os.mkdir(downdir)                                   
            print (f'[+] Directory {downdir} created\n')            #Code to create a directory was retrieved from https://thispointer.com/how-to-create-a-directory-in-python/
            print (f'[+] Downloading files into {downdir}...\n')    #by Varun (7/4/2018)

        #If directory already exists, FileExistsError is raised
        except FileExistsError:                                 
            try:
                print(f"[+] Directory {downdir} already exists")
                print(f'    [-] Clearing {downdir} contents...')
                #Delete current contents of directory
                os.chdir(downdir)
                files = os.listdir(downdir)
                for file in files:                                  
                    os.remove(file)                             
                print(f'    [-] {downdir} Contents cleared.\n')
                print(f'[+] Downloading files into {downdir}...\n')

            #PermissionError might be raised when trying to delete the contents
            except PermissionError:                             
                print(f'    [-] Access to {downdir} is denied. Contents were NOT cleared. Please, run as administrator.')
                print(f'[+] Trying to download files into {downdir}...\n')
                #Download the files even if previous contents haven't been successfully deleted
                pass                                             

        try:
            #Make {downdir} the current working directory      
            os.chdir(downdir)

            #Download images, avoid name collision and report whether they have been successfully downloaded
            #Successful downloaded images counter
            img_down=0                                      

            #In case there are images found, download them
            if len(images_sorted) > 0:

                #Retrieve the file's URL from the images_sorted global variable
                for link in images_sorted:                      
                    try:
                        list_files_pre = os.listdir(downdir)
                        #Attribute the filename from behind the last / from the URL
                        file = link.split('/')[-1]              
                        #Check whether the file's name about to download coincide with any file in the directory
                        for i in list_files_pre:
                            if i == file:
                                #Rename the file about to download to avoid name collision
                                file='COLLISION_'+file          
                        urllib.request.urlretrieve(link, file)
                        list_files = os.listdir(downdir)
                        #Check whether the file has been successfully downloaded
                        for i in list_files:                    
                            if i == file:
                                print (f'[+] {file.ljust(30)}  ---->  Successfully retrieved')
                                img_down+=1

                    #If the file from the RLS has not been found, an error is raised
                    except Exception as err:                                     
                        print (f"[-] {file.ljust(30)}  ---->  Unsuccessful download. Error: {err}")
                        pass

                #Download documents, avoid name collision and report whether they have been successfully downloaded
                #Successful downloaded documents counter
                doc_down=0                                      

            #In case there are documents found, download them
            if len(docs_sorted) > 0:

                #Retrieve the file's URL from the docs_sorted global variable
                for link in docs_sorted:                        
                    try:
                        list_files_pre = os.listdir(downdir)
                        #Attribute the filename from behind the last / from the URL
                        file = link.split('/')[-1]
                        #Check whether the file's name about to download coincide with any file in the directory
                        for i in list_files_pre:
                            if i == file:
                                #Rename the file about to download to avoid name collision
                                file='COLLISION_'+file            
                        urllib.request.urlretrieve(link, file)
                        list_files = os.listdir(downdir)
                        #Check the file has been successfully downloaded
                        for i in list_files:                    
                            if i == file:
                                print (f'[+] {file.ljust(30)}  ---->  Successfully retrieved')
                                doc_down+=1

                    #If the file from the RLS has not been found, an error is raised
                    except Exception as err:                                     
                        print (f"[-] {file.ljust(30)}  ---->  Unsuccessful download. Error: {err}")
                        pass

            #Print summary of successful downloads
            if len(images_sorted) > 0:
                print (f'\n    [-] {img_down}/{len(images_sorted)} Images successfully downloaded to {downdir}')
            if len(docs_sorted) > 0:
                print (f'    [-] {doc_down}/{len(docs_sorted)} Documents successfully downloaded to {downdir}')
    
        except Exception as err:
            print (f'\t[!] Error: {err}')

    else:
        print('\t[-] No files to download...')





def main():
    #Attribute the URL about to analyse to this variable:
    url = 'http://www.soc.napier.ac.uk/~40009856/CW/'
    #url = 'http://www.blankwebsite.com/'
    #Fetched data from the URL is attributed to this variable:
    page = webpage_get.wget(url)

    #Directory where to download retrieved data is attributed to this variable:
    downdir = r'C:\Retrieved_files'

    #Dictionary used to create the rainbow to compare the retrieved hashes with
    dictionary = 'dictionary.txt'
    
    print_images(page,url)      #Call the print_images() function 
    print_docs(page,url)        #Call the print_docs() function 
    print_email(page)           #Call the print_email() function 
    print_phones(page,url)      #Call the print_phones() function
    print_hashes(page,url)      #Call the print_hashes() function
    recover_hashes(dictionary)  #Call recover_hashes(), which calls the dict_attack() function from the hashes_crack module
                                #    using the contents of the hashes_sorted variable as parameter
    download_files(downdir)     #Call download_files() function

#Boilerplate
if __name__ == '__main__':
	main()
