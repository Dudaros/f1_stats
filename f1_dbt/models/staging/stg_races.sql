with source as (
    select * from {{source('f1_raw', 'races')}}
    )
select
race_id,
season,
round,
session_type,
race_name,
circuit_name,
country,
date

from source