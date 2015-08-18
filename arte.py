#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download Arte video replay
"""

from bs4 import BeautifulSoup
import json
import re
import sys
import urllib2
import wget
from os import environ

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    
    Taken from: http://code.activestate.com/recipes/577058
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

if __name__ == '__main__':

    Arte_url = raw_input('Enter an Arte+7 URL: ')              
    
    page = urllib2.urlopen(Arte_url)
    soup = BeautifulSoup(page.read(), "html.parser")
    
    # Get First JSON file of source page
    video = soup.find('div', class_='video-container')
    jsonfile_url = video['arte_vp_url']
    
    urls = {}  # Dict to store available URLs
    f = urllib2.urlopen(jsonfile_url)
    data = json.load(f)  # Read JSON file

    broadcast = data['videoJsonPlayer']['VTI'].encode('utf-8')  # Get broadcast name
    try:
        title = data['videoJsonPlayer']['VSU'].encode('utf-8')  # Get episode name
    except:
        title = ""    
    print "Available versions of \"{} - {}\"".format(broadcast, title)
    iversion = 1
    
    for key, val in data['videoJsonPlayer']['VSR'].items():
        if key[:5] == u'HTTP_':  # Filter HTTP URLs
            if val['quality'][0:2] == u'HD':  # HD format only
                urls[iversion] = val['url']  # store URL
                version_string = "{} ({})".format(val['versionLibelle'],
                                                val['quality'].replace(" ",""))
                print "  {}) {}".format(iversion, version_string)
                iversion += 1
    
    try:
        version = int(raw_input('Choice: '))
    except:
        raise ValueError('Version number must be an integer')
    
    if version not in urls.keys():
        raise ValueError('Version must be in: {}"'.format(urls.keys()))
    else:
        url = urls[version]

        file_extension = url.split('.')[-1]
        file_name = "Arte-{}-{}-{}.{}".format(broadcast, title,
                                        version_string.replace(" ","-"),
                                        file_extension)
        # Remove ":" and replace spaces (and duplicate spaces) by underscores
        file_name_string = re.sub(' +','_',file_name.replace(":",""))

        # Destination directory is default user download directory
        directory = environ['HOME']+"/Downloads"
        download_path = directory + "/" + file_name_string
        download = query_yes_no('Download {} to {}?'.format(url, download_path))                   
        if download:
            wget_file_name = wget.download(url, out=download_path)
            print "\nFile {} downloaded to {}".format(file_name, directory)
            
