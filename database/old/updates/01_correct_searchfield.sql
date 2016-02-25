-- Correcting the Search field parzellennumber in BK 
-- Fixes #10719


UPDATE "R_SEARCH_FILTER" 
SET  "LABEL" = 'Parzellennummer'
WHERE "R_SEARCH_FILTER_ID" = 46;
