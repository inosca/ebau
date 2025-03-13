#/bin/sh

# WARNING: Please be aware that this is a shell script, not a bash script! If
# you change the code of this script, you must make sure to test it in sh, not
# bash.

varnames=$1
path=$2

# Prefix each variable name with a dollar sign. This converts a value of
# "FOO,BAR,BAZ" to "$FOO,$BAR,$BAZ" which is required for envsubst to work
variables=$(echo $varnames | sed 's/\([^,]*\)/$\1/g')

# Print the variables that will be replaced for debugging
echo "Replacing ENV variables:"
set -- $(echo "$variables" | tr ',' ' ')
for item in "$@"; do
  eval "echo \" - \$item: $item\""
done

for file in $(find $path -iname "*.js");
do
  tmpfile="/tmp/$(basename $file)"
  envsubst $variables < $file > $tmpfile;
  mv $tmpfile $file
done
