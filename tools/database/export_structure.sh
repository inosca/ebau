#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

sqlplus system/oracle << EOF

CREATE OR REPLACE DIRECTORY strucdir AS '/var/local/database/structure_dumps/';

GRANT read,write ON DIRECTORY strucdir TO camac;

EOF

date=$(date +%Y-%m-%d-%H-%M)

expdp camac/camac DIRECTORY=strucdir DUMPFILE="structure-"$date TABLES=ATTACHMENT

exit 
