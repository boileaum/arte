#!/bin/bash

BASEPATH="$HOME/anaconda2/lib"
BASECMD="python setup.py py2app --resources $BASEPATH/tcl8.5,$BASEPATH/tk8.5"

if [ $# == 0 ]
then
  echo ">> Build standalone version"
  set -x
  $BASECMD --excludes "matplotlib,scipy,numpy,PyQt4,zmq"
elif [ $1 == "--alias" ]
then
  echo ">> Build alias version (for development only)"
  set -x
  $BASECMD --alias
else
  echo "Usage: build.sh [--alias]"
  exit
fi
