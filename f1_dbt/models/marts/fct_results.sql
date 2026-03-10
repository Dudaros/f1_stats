with drivers as (
    select * from {{ref('stg_drivers')}}
),

races as (
    select * from {{ref('stg_races')}}
),

results as (
    select * from {{ref('stg_results')}}
)

select
    a.race_id,
    a.season,
    a.round,
    a.session_type,
    a.race_name,
    a.circuit_name,
    a.country,
    a.date,
    b.driver_id,
    c.full_name,
    c.nationality,
    b.constructor,
    b.grid,
    b.position,
    b.points,
    b.status
from races a
left join results b on a.race_id = b.race_id
left join drivers c on b.driver_id = c.driver_id


 