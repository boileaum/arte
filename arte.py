#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Download Arte video replay
"""

from bs4 import BeautifulSoup
import easygui
import json
import re
import subprocess
import sys
import urllib2
from os import environ
from progress_meter import withprogress, UserCancelled


    
debug = False

Arte_url = easygui.enterbox('Enter an Arte+7 URL:')
if not Arte_url:
    sys.exit(0)
if debug:
    print "Arte+7 URL:", Arte_url
page = urllib2.urlopen(Arte_url)
soup = BeautifulSoup(page.read(), "html.parser")

# Get First JSON file of source page
video = soup.find('div', class_='video-container')
jsonfile_url = video['arte_vp_url']

urls = {}  # Dict to store available URLs
f = urllib2.urlopen(jsonfile_url)
data = json.load(f)  # Read JSON file
# Get broadcast name
broadcast = data['videoJsonPlayer']['VTI'].rstrip()
try:
    # Get episode name
    episode = data['videoJsonPlayer']['VSU'].rstrip()
    title = u"{}-{}".format(broadcast, episode)
except:
    title = broadcast

iversion = 1
version_choices = []

avail_versions = {}
for key, val in data['videoJsonPlayer']['VSR'].items():
    if key[:5] == u'HTTP_':  # Filter HTTP URLs
        avail_versions[val['quality']] = val['versionLibelle']
        
for key, val in data['videoJsonPlayer']['VSR'].items():
    if key[:5] == u'HTTP_':  # Filter HTTP URLs
        version_string = u"{} ({})".format(
                            val['versionLibelle'],
                            val['quality'].replace(" ",""))
        urls[version_string] = val['url']  # store URL
        # store version names
        version_choices.append(version_string.encode('utf-8'))

msg = u"Available versions of \"{}\" for download" \
        .format(title)
if debug:
    print msg
    print version_choices
version_choice = easygui.choicebox(msg=msg,
                                   title=u"Available versions",
                                   choices=version_choices)
if not version_choice:
    sys.exit(0)
    
url = urls[version_choice]

file_extension = url.split('.')[-1]
tmp_name = u"Arte-{}-{}.{}".format(title,
                                version_choice.replace(" ","-"),
                                file_extension)
# Remove ":" and replace spaces (and duplicate spaces) by underscores
file_name = tmp_name.replace(":","").replace(' +','_').replace('/','sur')

# Destination directory is default user download directory
directory = environ['HOME'].decode('utf-8') + u"/Downloads"
download_path = directory + u"/" + file_name

u = urllib2.urlopen(url)
file_size = float(u.headers["Content-Length"])
msg = u'Download:\n{}\n({:.2f} Mb) to:\n{}?'.format(url,
                                file_size/(1024*1024), download_path)
if debug:
    print msg

title = "Please Confirm"    
if easygui.ccbox(msg, title):  # Download or cancel? box
    

    f = open(download_path, 'wb')
    print "Downloading: {} ({} Bytes)".format(file_name.encode('utf-8'),
                                        file_size)

    # Call decorator to launch the progress bar
    @withprogress(upto=100, cancellable=True,
                  title="Downloading...", color="orange")
    def download():
        """Decorated function to download file"""
        block_sz = 64*1024  # chunk size of download
        file_size_dl = 0
        while True:
            buffer = u.read(block_sz)
            file_size_dl += len(buffer)
            status = 100*file_size_dl/file_size
            if not buffer:
                break
            f.write(buffer)
            yield status  # Send status to progress bar decorator
    
    try:
        download()
    except UserCancelled:
        print("Cancelled")
    else:
        print("Completed")        
        msg = "File {} downloaded to {}".format(file_name.encode('utf-8'),
                                         directory)
        easygui.msgbox(msg)  # Final message box
        file_to_show = directory + "/" + file_name
        # Show file in download directory
        subprocess.call(["open", "-R", file_to_show])
    finally:
        f.close()
        
