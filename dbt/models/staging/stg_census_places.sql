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
        CASE WHEN B01003_001E::INTEGER < 0 THEN NULL ELSE CAST(B01003_001E AS INTEGER) END as total_population,
        CASE WHEN B19013_001E::INTEGER < 0 THEN NULL ELSE CAST(B19013_001E AS INTEGER) END as median_household_income,
        CASE WHEN B25064_001E::INTEGER < 0 THEN NULL ELSE CAST(B25064_001E AS INTEGER) END as median_gross_rent,
        CASE WHEN B25077_001E::INTEGER < 0 THEN NULL ELSE CAST(B25077_001E AS INTEGER) END as median_home_value
    from source
)

select * from cleaned