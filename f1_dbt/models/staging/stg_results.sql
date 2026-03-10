with sources as (
    select * from {{source ('f1_raw', 'results')}}
)

select
result_id,
race_id,
driver_id,
constructor,
grid,
position,
points,
status

from sources
