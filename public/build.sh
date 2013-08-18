#!/bin/bash

echo "START"

for file in ./css/*.less
do
    f=${file:(6)}
    printf "lessc -c"
    printf " "
    printf $f
    printf " "
    printf ${f/%\.less/\.css}
    printf "\n"
    f=${f/%\.less/\.css}
    lessc -c $file > "./css/${f}"
done

cp css/*.css ../../svn-zhinsta/1/zhinsta/static/css/
cp js/*.js ../../svn-zhinsta/1/zhinsta/static/js/

echo "DONE"
