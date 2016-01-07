#!/bin/bash -
set -o nounset                              # Treat unset variables as an error
cd data
for f in $(ls *.TXT)
do
    echo $f
    sed -i "" 's#\([0-9]\{2\}\)\/\([0-9]\{2\}\)\/\([0-9]\{4\}\)#\3-\1-\2#g' $f
done


