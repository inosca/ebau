#!/bin/bash

# Helper tool to call the scripts that do the db operations
# in the database docker container

sshpass -p "admin" ssh root@$1 -p $2 -o StrictHostKeyChecking=no chmod +x $3
sshpass -p "admin" ssh root@$1 -p $2 -o StrictHostKeyChecking=no bash +x $3

