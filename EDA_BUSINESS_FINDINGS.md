# MIG Cement Forecasting — EDA & Business Findings

This companion document contains the detailed exploratory findings used in the main GitHub README.

## Demand Distribution and Cement Type

- Cement consumption is **right-skewed**, with some observations recording zero consumption while others exceed **69 tonnes**.
- Average consumption is approximately **23.7 tonnes per operational record**.
- Demand differs across sites, reflecting differences in project scale, activity, pour schedules and operating conditions.
- Demand across the three cement types is broadly similar, although **CEM II contributes slightly more than 34% of total consumption**.

![Demand distribution](../assets/eda/01_demand_distribution.png)

![Consumption by site](../assets/eda/03_total_consumption_by_site.png)

![Consumption by cement type](../assets/eda/04_consumption_by_cement_type.png)

## Demand Over Time and Seasonality

- Cement consumption fluctuates over time rather than remaining constant.
- Average monthly demand does not vary dramatically, suggesting broad month-level seasonality is relatively weak.
- Average weekday demand is also similar overall.
- Demand appears somewhat higher on **Tuesday, Wednesday, Thursday, Saturday and Sunday**, while **Monday and Friday** are comparatively lower.
- The month × weekday heatmap reveals more specific operating patterns:
  - Monday → **August**
  - Tuesday → **December**
  - Wednesday → **January**
  - Thursday → **July**
  - Sunday → **November**
- Friday and Saturday do not show a similarly clear recurring high-demand pattern.

![Demand over time](../assets/eda/05_demand_over_time.png)

![Average demand by month](../assets/eda/06_average_demand_by_month.png)

![Average demand by weekday](../assets/eda/07_average_demand_by_weekday.png)

![Month weekday heatmap](../assets/eda/13_month_weekday_heatmap.png)

## Demand Volatility Across Sites

- Demand volatility varies meaningfully across sites.
- **Sites 28, 26, 14, 24 and 06** appear among the more volatile sites.
- More stable sites may be easier to forecast.
- Forecast difficulty should therefore not be assumed to be uniform across MIG's portfolio.

![Site demand volatility](../assets/eda/08_site_demand_volatility.png)

## Planned Pours vs Actual Consumption

- Planned pours and actual consumption have a clear positive relationship.
- The correlation is approximately **0.781**.
- Planned construction activity is therefore a potentially strong forecasting input.
- The relationship is associative rather than causal.

![Planned pours vs actual](../assets/eda/09_planned_pours_vs_actual.png)

## Weather and Cement Demand

- Rainfall shows a strong negative relationship with cement consumption in the historical data.
- Higher rainfall is generally associated with lower consumption.
- Temperature shows only a weak linear relationship with consumption.
- A weak linear relationship does not prove temperature is irrelevant; it may interact with other variables.

![Rainfall vs consumption](../assets/eda/10_rainfall_vs_consumption.png)

![Temperature vs consumption](../assets/eda/11_temperature_vs_consumption.png)

## Inventory View

The EDA also contains a site-level closing-inventory comparison that can be used as a starting point for deeper inventory-risk diagnostics.

![Average closing inventory by site](../assets/eda/12_average_closing_inventory_by_site.png)

## Overall Business Interpretation

MIG's cement demand is influenced by multiple dimensions rather than one universal pattern. Demand differs across sites, displays meaningful volatility, responds strongly to planned construction activity and appears sensitive to rainfall.

Broad monthly and weekday averages are relatively stable, but more granular calendar analysis reveals specific month–weekday combinations where demand becomes noticeably higher.

These findings support a forecasting approach that preserves:

- site-level differences
- cement type
- calendar effects
- planned pours
- historical demand patterns
- weather information where justified and available at forecast time
