#/bin/sh

# WARNING: Please be aware that this is a shell script, not a bash script! If
# you change the code of this script, you must make sure to test it in sh, not
# bash.

varnames=$1
source_path=$2
target_path=$3

# Prefix each variable name with a dollar sign. This converts a value of
# "FOO,BAR,BAZ" to "$FOO,$BAR,$BAZ" which is required for envsubst to work
variables=$(echo $varnames | sed 's/\([^,]*\)/$\1/g')

# Print the variables that will be replaced for debugging
echo "Replacing ENV variables:"
set -- $(echo "$variables" | tr ',' ' ')
for item in "$@"; do
  eval "echo \" - \$item: $item\""
done

# Force copy source files to the target folder to make sure the target folder
# contains unprocessed files before replacing the variables.
# The raw files (`$source_path`) are kept so we can change variables, restart
# and have the new values in the processed files.
cp -rf "$source_path/." "$target_path/"

for file in $(find $target_path -iname "*.js");
do
  tmpfile="/tmp/$(basename $file)"
  envsubst $variables < $file > $tmpfile;
  mv $tmpfile $file
done
