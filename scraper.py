# Script:   scraper.py
# Desc:     Web page information gathering script which retrieves web content,
#           parses it for specific information and performs forensic analysis
#           on the contents.
# Author:   Xavier Sala
# Modified: December 2018
#

import os
import webpage_get, webpage_getlinks, webpage_getdata, hashes_crack, forensic_analysis




def main():
    #Attribute the URL about to analyse to this variable:
    url = 'http://www.soc.napier.ac.uk/~40009856/CW/'
    
    #Fetched data from the URL is attributed to this variable:
    page = webpage_get.wget(url)

    #Directory where to download retrieved data is attributed to this variable:
    downdir = r'C:\Retrieved_files'

    #File containing the known bad files:
    badfiles = 'badfiles.txt'

    #Get the current working directory to pass it as argument 
    curr_dir = os.getcwd()

    #Dictionary used to create the rainbow to compare the retrieved hashes with
    dictionary = 'dictionary.txt'
    
    webpage_getlinks.print_links(page,url)      #Call the print_links() function from the webpage_getlinks module
    webpage_getdata.print_images(page,url)      #Call the print_images() function from the webpage_getdata module
    webpage_getdata.print_docs(page,url)        #Call the print_docs() function from the webpage_getdata module
    webpage_getdata.print_email(page)           #Call the print_email() function from the webpage_getdata module
    webpage_getdata.print_phones(page,url)      #Call the print_phones() function from the webpage_getdata module
    webpage_getdata.print_hashes(page,url)      #Call the print_hashes() function from the webpage_getdata module
                                                #   for Hash in hashes_sorted: dict_crack.dict_attack(Hash)
    webpage_getdata.recover_hashes(dictionary)  #Call recover_hashes(), which calls the dict_attack() function from the hashes_crack module
                                                #   using the contents of the hashes_sorted variable as parameter
    webpage_getdata.download_files(downdir)     #Call the download_files() function from the webpage_getdata module
    forensic_analysis.files_sig(downdir)        #Call files_sig() from the forensic_analysis module, which calls the check_sig() function
                                                #   from the file_type module
    forensic_analysis.badfiles_check(badfiles,downdir,curr_dir) #Call badfiles_check() from the forensic_analysis module, which calls the get_hash() function
                                                                #   from the file_hash module
    forensic_analysis.same_files(downdir)       #Call the same_files() function from the forensic_analysis module

#Boilerplate
if __name__ == '__main__':
	main()
