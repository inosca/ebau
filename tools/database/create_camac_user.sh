#!/bin/bash

source /u01/app/oracle/product/11.2.0/xe/bin/oracle_env.sh

sqlplus system/oracle << EOF

CREATE USER camac IDENTIFIED BY camac;
grant connect to camac;
grant create table to camac;
grant create view to camac;
grant create procedure to camac;
grant create sequence to camac;
grant create trigger to camac;
grant resource to camac;
grant create materialized view to camac;
grant CREATE any directory to camac;

EOF
