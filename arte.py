#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jul 15 10:24:22 2015

@author: boileau
"""

from bs4 import BeautifulSoup
import json
import urllib2
import sys
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
    
    print "Available versions:"
    iversion = 1
    
    for key, val in data['videoJsonPlayer']['VSR'].items():
        if key[:5] == u'HTTP_':  # Filter HTTP URLs
            if val['quality'][0:2] == u'HD':  # HD format only
                urls[iversion] = val['url']  # store URL
                print "  {}) {} ({})".format(iversion,
                                            val['versionLibelle'],
                                            val['quality'])
                iversion += 1
    
    try:
        version = int(raw_input('Choose your version: '))
    except:
        raise ValueError('Version number must be an integer')
    
    if version not in urls.keys():
        raise ValueError('Version must be: {}"'.format(urls.keys()))
    else:
        url = urls[version]
    
        download = query_yes_no('Do you want to download {} ?'.format(url))                   
        if download:
            # Destination directory is default user download directory
            directory = environ['HOME']+"/Downloads"
            wget_file_name = wget.download(url, out=directory)
            file_name = url.split('/')[-1]
            print "\nFile {} downloaded to {}".format(file_name, directory)
            
