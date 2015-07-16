#!/bin/bash

cmdfile="Arte+7.command"

cp arte.py $cmdfile

# Hide extension
SetFile -a E $cmdfile

# Take an image and make the image its own icon:
sips -i icon.png

# Extract the icon to its own resource file:
DeRez -only icns icon.png > tmpicns.rsrc

# append this resource to the file you want to icon-ize.
Rez -append tmpicns.rsrc -o $cmdfile

# Use the resource to set the icon.
SetFile -a C $cmdfile

# clean up.
rm -f tmpicns.rsrc

mv $cmdfile /Applications


