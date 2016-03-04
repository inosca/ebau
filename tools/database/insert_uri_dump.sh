#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

sqlplus system/oracle << EOF

CREATE OR REPLACE DIRECTORY dmpdir AS '/var/local/database/uri_dumps/';

GRANT read,write ON DIRECTORY dmpdir TO camac;

EOF

impdp camac/camac DIRECTORY=dmpdir DUMPFILE=2016-02-23.dmp SCHEMAS=camac 

exit 0
