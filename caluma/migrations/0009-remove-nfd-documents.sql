delete from form_formquestion where question_id='nfd-dokumente';
delete from form_question where slug='nfd-dokumente';

insert into migration_history (name) values ('0009-remove-nfd-documents');
