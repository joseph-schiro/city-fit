with places as (
    select *
    from {{ ref('stg_census_places') }}
    where total_population >= {{ var('min_population') }}
      and median_household_income is not null
      and median_gross_rent is not null
      and median_home_value is not null
      -- Exclude Puerto Rico
      and state_fips <> '72'
),

ratios as (
    select
        *,
        median_gross_rent * 12 / nullif(median_household_income, 0) as rent_to_income_ratio,
        median_home_value / nullif(median_household_income, 0) as home_value_to_income_ratio
    from places
),

scored as (
    select
        *,
        round(100 * percent_rank() over (order by rent_to_income_ratio desc)) as rent_score,
        round(100 * percent_rank() over (order by home_value_to_income_ratio desc)) as home_price_score,
        round(100 * percent_rank() over (order by median_household_income asc)) as income_score
    from ratios
)

select * from scored