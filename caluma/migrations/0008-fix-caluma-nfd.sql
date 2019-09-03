update form_answer set question_id='nfd-tabelle-status', value='"nfd-tabelle-status-erledigt"' where id in (
  select id
  from form_answer
  where value='"nfd-tabelle-erledigt-ja"'
);

update form_answer set question_id='nfd-tabelle-status', value='"nfd-tabelle-status-entwurf"' where id in (
  select id
  from form_answer
  where value='"nfd-tabelle-erledigt-nein"'
);

delete from form_answer where question_id='nfd-einreichen-button';

delete from form_formquestion where question_id in (
  'nfd-tabelle-erledigt',
  'nfd-einreichen-button',
  'nfd-nachforderungen-form',
  'nfd-einreichen-form',
  'nfd-dokumente-form'
);

delete from form_formquestion where form_id in (
  'nfd-dokumente',
  'nfd-einreichen',
  'nfd-nachforderungen'
);

delete from form_questionoption where question_id in (
  'nfd-einreichen-button',
  'nfd-tabelle-erledigt'
);

delete from form_option where slug in (
  'nfd-einreichen-button-eingereicht',
  'nfd-tabelle-erledigt-ja',
  'nfd-tabelle-erledigt-nein'
);

delete from form_question where slug in (
 'nfd-einreichen-form',
 'nfd-dokumente-form',
 'nfd-nachforderungen-form',

 'nfd-einreichen-button',
 'nfd-tabelle-erledigt',
 'nfd-autorin',
 'nfd-behoerde',
 'nfd-beschreibung',
 'nfd-datum-anfrage'
);

delete from form_form where slug in (
 'nfd-einreichen',
 'nfd-dokumente',
 'nfd-nachforderungen'
);

insert into migration_history (name) values ('0008-fix-caluma-nfd');
