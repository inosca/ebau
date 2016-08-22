alter table billing_entry add "CREATED" DATE;
alter table billing_entry add "TYPE" NUMBER(1,0) DEFAULT 0 NOT NULL;
