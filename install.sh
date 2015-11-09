#/bin/bash

./clean.sh
if [ "$1" = "--alias" ]
then
  ./build_alias.sh
else
  ./build_standalone.sh
fi
./finalize.sh
