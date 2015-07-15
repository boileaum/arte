#!/bin/bash

cp arte.py arte.command
SetFile -a E  arte.command

# Take an image and make the image its own icon:
#sips -i icon.png

# Extract the icon to its own resource file:
DeRez -only icns icon.png > tmpicns.rsrc

# append this resource to the file you want to icon-ize.
Rez -append tmpicns.rsrc -o arte.command

# Use the resource to set the icon.
SetFile -a C arte.command

# clean up.
rm tmpicns.rsrc
# rm icon.png # probably want to keep this for re-use.
