-- B01003_001E: total_population
-- B19013_001E: median_household_income
-- B25064_001E: median_gross_rent
-- B25077_001E: median_home_value

with source as (
    select * from {{ source('census', 'raw_census_places') }}
),


cleaned as (
    select
        state || place as geoid,
        state as state_fips,
        place as place_fips,
        NAME as place_name,
        {{ clean_census_value('B01003_001E') }} as total_population,
        {{ clean_census_value('B19013_001E') }} as median_household_income,
        {{ clean_census_value('B25064_001E') }} as median_gross_rent,
        {{ clean_census_value('B25077_001E') }} as median_home_value
    from source
)

select * from cleaned