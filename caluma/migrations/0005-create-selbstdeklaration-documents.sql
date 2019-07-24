create extension "uuid-ossp";

------------------
-- SB1
------------------

-- Create new documents for existing ones that have SB1 answers
insert into form_document (id, family, form_id, meta, created_at, modified_at, created_by_user, created_by_group)
select
	uuid_generate_v4() as document_id,
	'00000000-0000-0000-0000-000000000000'::uuid as family_id,
	'sb1' as form_id,
	meta, created_at, modified_at, created_by_user, created_by_group from form_document where form_document.id in (
		select distinct
			form_document.id
		from form_document
		left join form_answer on form_document.id = form_answer.document_id
		where form_answer.question_id in (
			'bedingungen-und-auflagen-erfuellt',
			'abweichung',
			'ist-eine-schnurgerustabnahme-erforderlich',
			'schnurgeruest-zur-abnahme-bereit',
			'beginn-bauarbeiten',
			'ab-wann-ist-eine-kontrolle-moeglich',
			'bemerkungen-sb1'
		)
		and form_document.form_id != 'sb1'
	);

-- Update references of SB1 answers to new document
update form_answer
set document_id = mapping_table.new_document_id
from (
	select
		form_answer.id as answer_id,
		form_answer.question_id,
		form_document.id as old_document_id,
		form_document_2.id as new_document_id,
		form_document.meta->'camac-instance-id' as instance_id,
		form_answer.value
	from form_document
	left join form_answer on form_document.id = form_answer.document_id
	left join form_document as form_document_2
		on form_document_2.form_id='sb1'
		and form_document_2.meta->'camac-instance-id' = form_document.meta->'camac-instance-id'
	where form_answer.question_id in (
		'bedingungen-und-auflagen-erfuellt',
		'abweichung',
		'ist-eine-schnurgerustabnahme-erforderlich',
		'schnurgeruest-zur-abnahme-bereit',
		'beginn-bauarbeiten',
		'ab-wann-ist-eine-kontrolle-moeglich',
		'bemerkungen-sb1'
	)
	and form_document.form_id != 'sb1'
) as mapping_table
where form_answer.id = mapping_table.answer_id;

------------------
-- SB2
------------------

-- Create new documents for existing ones that have SB2 answers
insert into form_document (id, family, form_id, meta, created_at, modified_at, created_by_user, created_by_group)
select
	uuid_generate_v4() as document_id,
	'00000000-0000-0000-0000-000000000000'::uuid as family_id,
	'sb2' as form_id,
	meta, created_at, modified_at, created_by_user, created_by_group from form_document where form_document.id in (
		select distinct
			form_document.id
		from form_document
		left join form_answer on form_document.id = form_answer.document_id
		where form_answer.question_id in (
			'bauvorhaben-nach-baubewilligung-ausgefuehrt',
			'abweichung-ausfuehrung',
			'bedingungen-auflagen-eingehalten',
			'abweichung-bedingungen-auflagen',
			'sicherheitsvorschriften-eingehalten',
			'abweichung-sicherheitsvorschriften',
			'sind-die-nebengebaeude-fertiggestellt',
			'zeitpunt-der-fertigstellung',
			'sind-die-umgebungsarbeiten-fertiggestellt',
			'zeitpunkt-der-fertigstellung-umgebungsarbeiten',
			'meldung-tankanlage',
			'bemerkungen-abschluss-sb2'
		)
		and form_document.form_id != 'sb2'
	);

-- Update references of SB2 answers to new document
update form_answer
set document_id = mapping_table.new_document_id
from (
	select
		form_answer.id as answer_id,
		form_answer.question_id,
		form_document_2.id as new_document_id,
		form_document.meta->'camac-instance-id' as instance_id

	from form_document
	left join form_answer on form_document.id = form_answer.document_id
	left join form_document as form_document_2
		on form_document_2.form_id='sb2'
		and form_document_2.meta->'camac-instance-id' = form_document.meta->'camac-instance-id'
	where form_answer.question_id in (
		'bauvorhaben-nach-baubewilligung-ausgefuehrt',
		'abweichung-ausfuehrung',
		'bedingungen-auflagen-eingehalten',
		'abweichung-bedingungen-auflagen',
		'sicherheitsvorschriften-eingehalten',
		'abweichung-sicherheitsvorschriften',
		'sind-die-nebengebaeude-fertiggestellt',
		'zeitpunt-der-fertigstellung',
		'sind-die-umgebungsarbeiten-fertiggestellt',
		'zeitpunkt-der-fertigstellung-umgebungsarbeiten',
		'meldung-tankanlage',
		'bemerkungen-abschluss-sb2'
	)
	and form_document.form_id != 'sb2'
) as mapping_table
where form_answer.id = mapping_table.answer_id;

-- fix family IDs
update form_document set family = id where family = '00000000-0000-0000-0000-000000000000'::uuid;
