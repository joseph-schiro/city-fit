select *
from {{ ref('stg_census_places') }}
where total_population < 0
   or median_household_income < 0
   or median_gross_rent < 0
   or median_home_value < 0