#!/bin/sh


ssh $1 -p $p2 --o StrictHostKeyChecking=no
while test $? -gt 0
do
   sleep 1
    echo "Waiting for ssh..."
   ssh $1 -p $p2 -o StrictHostKeyChecking=no
done

