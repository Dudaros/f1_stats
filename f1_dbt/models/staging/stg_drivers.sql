with source as (
    select * from {{ source('f1_raw', 'drivers')}}
)

select
driver_id,
code,
first_name,
last_name,
first_name || ' ' || last_name AS full_name,
nationality,
date_of_birth

from source
