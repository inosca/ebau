update form_document set family=id where meta->>'camac-instance-id' is not NULL and family != id;

create table migration_history (executed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(), name varchar(255));
insert into migration_history (name) values ('0007-fix-document-family-again');
