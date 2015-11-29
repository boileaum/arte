#/bin/bash

if [ $# != 0 ]
then
  if [ $1 != "--alias" ]
  then
    echo "Usage: install.sh [--alias]"
    exit
  fi
fi
./clean.sh
./build.sh $1
./finalize.sh
