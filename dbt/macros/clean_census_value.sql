{% macro clean_census_value(column_name) %}
    case when {{ column_name }}::integer < 0 then null else {{ column_name }}::integer end
{% endmacro %}