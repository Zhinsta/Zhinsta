#!/bin/bash

echo "START"

for file in ./css/*.less
do
    f=${file:6}
    printf "lessc -c"
    printf " "
    printf $f
    printf " "
    printf ${f/%\.less/\.css}
    printf "\n"
    f=${f/%\.less/\.css}
    lessc -c $file > "./css/${f}"
done

for file in ./js/*.js
do
    a=".min.js"
    if [[ "${file/$a/}" != "$file" ]]
    then
        continue
    fi
    f=${file:5}
    printf "uglifyjs "
    printf $f
    printf " "
    printf ${f/%\.js/\.min.js}
    printf "\n"
    f=${f/%\.js/\.min\.js}
    uglifyjs $file > "./js/${f}"
done

cp css/*.css ../../svn-zhinsta/1/zhinsta/static/css/
cp js/*.js ../../svn-zhinsta/1/zhinsta/static/js/

echo "DONE"
