#!/bin/sh


ssh $1
while test $? -gt 0
do
   sleep 1
    echo "Waiting for ssh..."
   ssh $1
done

