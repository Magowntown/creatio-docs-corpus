-- Check what the status IDs mean
SELECT "Id", "Name"
FROM "OrderStatus"
WHERE "Id" IN (
    '40de86ee-274d-4098-9b92-9ebdcf83d4fc',
    '2b9201fc-3891-4ba3-abde-1bb9ce195ecc',
    '29fa66e3-ef69-4feb-a5af-ec1de125a614'
);
