# Script:   webpage_getlinks.py
# Desc:     Basic web site info gathering and analysis script.
#           From a URL gets page content, and parses out hyperlinks.
# Author: Petra L & Rich McF
# Modified: Nov 2018


import sys
import re
import webpage_get


def print_links(page,url):
    ''' find all hyperlinks on the webpage input and print them'''
    print('\n\n\n\n[*] print_links()')

    try:
        # regex to match on hyperlinks
        links = re.findall('(<a\shref\=\")(\S*)(\")', page.decode()) #pattern matches strings starting with '<a href="' and ending with '"'
    except:
        print(f'[!] Error: Contents from webpage unsuccessfully retrieved')
        pass

    else:
        try:
            # sort and print the absolute links
            links_sorted = []
            links_absolute = []
            links_relative = []
            print(f'[+] {len(links)} HyperLinks Found:\n')
            for link in links:
                if link[1].startswith('http'):              #Absolute links are appended to the sorted list
                    links_sorted.append(link[1])
                    links_absolute.append(link[1])          #Absolute links are appended to an absolute links list
                else:
                    links_sorted.append(url+link[1])        #Relative links are appended to the URL and added to the sorted list
                    links_relative.append(link[1])          #Relative links are appended to a relative links list
            links_sorted.sort()
            #links_absolute.sort()
            #links_relative.sort()
            for link in links_sorted: print(link)

        except:
            pass

def main():
    # temp testing url argument
    url = r'http://www.napier.ac.uk'
    sys.argv.append(url)

    # Check args
    if len(sys.argv) != 2:
        print('[-] Usage: webpage_getlinks URL')
        return

    # Get the web page
    page = webpage_get.wget(sys.argv[1])
    # Get the links
    print_links(page,url)


if __name__ == '__main__':
    main()
