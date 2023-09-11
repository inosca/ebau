#/bin/sh

vars=$1
path=$2

for file in $(find $path -iname "*.js");
do
  tmpfile="/tmp/$(basename $file)"
  envsubst $vars < $file > $tmpfile;
  mv $tmpfile $file
done
