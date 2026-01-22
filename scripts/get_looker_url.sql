-- Get sample Looker Studio URLs
SELECT "Name", "UsrURL"
FROM "UsrReportesPampa"
WHERE "UsrURL" IS NOT NULL AND "UsrURL" != ''
LIMIT 5;
