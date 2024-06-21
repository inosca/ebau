#/bin/sh

varnames=$1
path=$2

# prefix each variable name with $ and
# concatenate them in a string
for var in $varnames
do
  variables=${variables:+$variables}" \$$var"
done


for file in $(find $path -iname "*.js");
do
  tmpfile="/tmp/$(basename $file)"
  envsubst $variables < $file > $tmpfile;
  mv $tmpfile $file
done
