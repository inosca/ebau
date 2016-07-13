delete from publication_setting;

alter table publication_setting drop column value;
alter table publication_setting add "VALUE" NVARCHAR2(2000);


insert into publication_setting
("PUBLICATION_SETTING_ID", "KEY", "VALUE")
VALUES(1, 'duration','20 Tage');

insert into publication_setting
("PUBLICATION_SETTING_ID", "KEY", "VALUE")
VALUES(2, 'fromEmail', 'camac@ur.ch');

insert into publication_setting
("PUBLICATION_SETTING_ID", "KEY", "VALUE")
VALUES(3, 'toEmail', 'amtsblatt@ur.ch');

insert into publication_setting
("PUBLICATION_SETTING_ID", "KEY", "VALUE")
VALUES(4, 'text', '
Gemeindebaubehörde [@authority]

Standeskanzlei Uri
Redaktion Amtsblatt
Rathaus
6460 Altdorf

[@zip] [@location], [@date]


Meldung einer Bauplanauflage zur Publikation im Amtsblatt unter der Rubrik
"Bau und Planungsrecht"

Sehr geehrte Damen und Herren

Wir bitten Sie, folgende Bauplanauflage im Amtsblatt vom Freitag [@publishDate]
zu publizieren:

[@community]

Bauherrschaft:[@c1q221i1] [@c1q23i1], [@c1q61i1], [@c1q62i1]
Bauvorhaben: [@intent]
Bauplatz: [@c21q93i1]
Parzelle: [@c21q91i1]
Bemerkungen: [@note]




Wir danken Ihnen für Ihre Bemühungen und stehen bei Fragen gerne zur Verfügung

Freundliche Grüsse

Gemeindebaubehörde [@authority]


[@zip] [@location], [@date]

');
