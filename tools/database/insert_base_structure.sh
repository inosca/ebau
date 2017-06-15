#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

chown oracle -R /var/local/database

sqlplus system/oracle << EOF
CREATE OR REPLACE DIRECTORY strucdir AS '/var/local/database/structure_dumps/';
GRANT read,write ON DIRECTORY strucdir TO camac;
EOF

impdp camac/camac DIRECTORY=strucdir DUMPFILE=latest SCHEMAS=camac \
    NOLOGFILE=Y

exit 0

