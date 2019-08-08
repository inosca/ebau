-- Update answer references and values.
update form_answer
set question_id = 'juristische-person-gesuchstellerin'
where question_id = 'juristische-person-personalien';

update form_answer
set "value" = '"juristische-person-gesuchstellerin-ja"'
where "value" = '"juristische-person-personalien-ja"';

update form_answer
set "value" = '"juristische-person-gesuchstellerin-nein"'
where "value" = '"juristische-person-personalien-nein"';

-- Update answer history references and values.
update form_historicalanswer
set question_id = 'juristische-person-gesuchstellerin'
where question_id = 'juristische-person-personalien';

update form_historicalanswer
set "value" = '"juristische-person-gesuchstellerin-ja"'
where "value" = '"juristische-person-personalien-ja"';

update form_historicalanswer
set "value" = '"juristische-person-gesuchstellerin-nein"'
where "value" = '"juristische-person-personalien-nein"';
