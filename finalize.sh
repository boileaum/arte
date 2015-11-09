#!/bin/bash

echo ">> Finalizing installation"
set -x
if [ -d "dist" ]
then
  projectdir=$PWD
  echo $projectdir
  cd dist/Arte.app/Contents
  rm -rf lib
  mkdir lib
  cd lib
  ln -s ../Resources/tcl8.5
  ln -s ../Resources/tk8.5
  cd $projectdir/dist/
  mv Arte.app Arte\+7.app

else
  echo "Directory ./dist does not exist"
fi

