#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download Arte video replay
"""

from bs4 import BeautifulSoup
import easygui
import json
import re
import urllib2
import wget
from os import environ

if __name__ == '__main__':

#    Arte_url = raw_input('Enter an Arte+7 URL: ')              
    Arte_url = easygui.enterbox('Enter an Arte+7 URL: ')              
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

    iversion = 1
    version_choices = []
    
    for key, val in data['videoJsonPlayer']['VSR'].items():
        if key[:5] == u'HTTP_':  # Filter HTTP URLs
            if val['quality'][0:2] == u'HD':  # HD format only
                version_string = "{} ({})".format(val['versionLibelle'],
                                                val['quality'].replace(" ",""))
                urls[version_string] = val['url']  # store URL
                version_choices.append(version_string)  # store version names
    
    msg = "Available versions of \"{} - {}\" for download" \
            .format(broadcast, title)
    version_choice = easygui.choicebox(msg=msg,
                                       title="Available versions",
                                       choices=version_choices)
    
    url = urls[version_choice]

    file_extension = url.split('.')[-1]
    file_name = "Arte-{}-{}-{}.{}".format(broadcast, title,
                                    version_string.replace(" ","-"),
                                    file_extension)
    # Remove ":" and replace spaces (and duplicate spaces) by underscores
    file_name_string = re.sub(' +','_',file_name.replace(":",""))

    # Destination directory is default user download directory
    directory = environ['HOME']+"/Downloads"
    download_path = directory + "/" + file_name_string
    
    msg = 'Download {} to {}?'.format(url, download_path)
    title = "Please Confirm"
    if easygui.ccbox(msg, title):     # show a Continue/Cancel dialog
        wget_file_name = wget.download(url, out=download_path)
        print "\nFile {} downloaded to {}".format(file_name, directory)
            
