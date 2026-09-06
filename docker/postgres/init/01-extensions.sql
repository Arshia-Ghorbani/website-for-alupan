-- Runs once, on first initialisation of the data volume.
-- pg_trgm  : fuzzy / partial matching for site search (works with Persian text).
-- unaccent : strips diacritics so "façade" matches "facade".
CREATE EXTENSION IF NOT EXISTS pg_trgm;
CREATE EXTENSION IF NOT EXISTS unaccent;
CREATE EXTENSION IF NOT EXISTS btree_gin;
