#!/bin/bash

echo ">> Building alias version (for development only)"
set -x
python setup.py py2app --resources "$HOME/anaconda/lib/tcl8.5,$HOME/anaconda/lib/tk8.5" --alias
