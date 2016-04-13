#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

sqlplus system/oracle << EOF

CREATE USER camac IDENTIFIED BY camac;
grant all privileges to camac;

EOF

#grant CONNECT to camac;
#grant CREATE TABLE to camac;
#grant CREATE VIEW to camac;
#grant CREATE PROCEDURE to camac;
#grant CREATE SEQUENCE to camac;
#grant CREATE TRIGGER to camac;
#grant RESOURCE to camac;
#grant CREATE MATERIALIZED view to camac;
#grant CREATE any directory to camac;
#grant CREATE SYNONYM to camac;
#
#EOF
