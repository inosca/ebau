#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

sqlplus system/oracle << EOF
CREATE OR REPLACE DIRECTORY strucdir AS '/var/local/database/uri_dumps/';
GRANT read,write ON DIRECTORY strucdir TO camac;
EOF

impdp camac/camac DIRECTORY=strucdir DUMPFILE=deployed-but-not-adjusted-2016-05-11-07-35.dmp SCHEMAS=camac 

exit 0

