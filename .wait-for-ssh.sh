#!/bin/sh


sshpass -p "admin" ssh $1 -p $2 -o StrictHostKeyChecking=no
while test $? -gt 0
do
   sleep 1
   echo "Waiting for ssh..."
   sshpass -p "admin" ssh $1 -p $2 -o StrictHostKeyChecking=no
done

