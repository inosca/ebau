/*
 * This will link all "Baugesuch" pages into
 * other similar forms ("Vorabklärung vollständig", "Generelles Baugesuch", "Baugesuch mit UVP")
 *
 * Usage:
 *		1. make dbshell on root directory
 *	    2. copy all scripts into the bash
 *		3. run
 *	    4. always check before committing your changes
 */
INSERT INTO "PAGE_FORM" ("SORT","FORM_ID","PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID")
	SELECT "SORT",40001,"PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID"
	FROM "PAGE_FORM"
	WHERE "FORM_ID" = 1;

INSERT INTO "PAGE_FORM" ("SORT","FORM_ID","PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID")
	SELECT "SORT",40002,"PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID"
	FROM "PAGE_FORM"
	WHERE "FORM_ID" = 1;

INSERT INTO "PAGE_FORM" ("SORT","FORM_ID","PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID")
	SELECT "SORT",110001,"PAGE_ID","PAGE_FORM_GROUP_ID","PAGE_FORM_MODE_ID"
	FROM "PAGE_FORM"
	WHERE "FORM_ID" = 1;

