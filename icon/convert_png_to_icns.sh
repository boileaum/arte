#!/bin/bash

cp icon.png icon.icns
sips -i icon.png 
DeRez -only icns icon.png > tmpicns.rsrc
Rez -append tmpicns.rsrc -o icon.icns
SetFile -a C icon.icns 
rm -f tmpicns.rsrc
