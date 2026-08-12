# Cement-Demand-Forecasting-Across-Multiple-Sites
This project seek to  address MIG currently facing challenges including stockouts, overstocking, and inefficiencies from reactive ordering. 

### Cement Demand Forecasting Across Multiple Sites
Project Context
Midlands Infrastructure Group (MIG) is a Tier-1 UK civil engineering and construction company operating 25–40 active project sites nationwide. Cement plays a critical role in project delivery but is prone to supply-demand mismatches due to fluctuating pour schedules, weather variations, and manual planning practices.
MIG currently faces challenges including stockouts, overstocking, and inefficiencies from reactive ordering. These issues result in project delays, wastage, and increased costs. MIG leadership has requested a data-driven forecasting solution that can anticipate cement demand at each site and support proactive inventory management decisions.

### Project Purpose
To design and deploy a predictive forecasting model that uses historical consumption, pour schedules, weather data, and inventory records to forecast cement demand across multiple sites. The model will drive more efficient stock planning, reduce waste, and ensure project continuity without material shortages.
Expected Deliverables
•	A time-series forecasting model (ARIMA/ML-based) capable of predicting cement demand up to 8 weeks ahead.
•	A Plotly Dash dashboard displaying forecasts, inventory levels, and reorder alerts by site.
•	A data-driven inventory optimization framework to define reorder points based on forecasted demand and silo capacities.
•	Project documentation covering methodology, model performance, and key insights.
Target Outcomes
•	Forecast accuracy with MAPE ≤ 15%.
•	≥ 98% pour readiness (no stockouts at scheduled pours).
•	20% improvement in silo utilization efficiency.
•	30% reduction in material write-offs.

### Business Challenge
Midlands Infrastructure Group (MIG) Ltd. is a Tier-1 UK civil engineering and construction company headquartered in Birmingham, England. Founded in 1994 as a regional roadworks contractor, the company has grown strategically over three decades to become a national operator delivering complex infrastructure projects across highways, rail, energy, and utilities sectors.
MIG's growth trajectory reflects a commitment to operational excellence and technological advancement. The 2000s marked the company's expansion into multi-site operations with regional hubs across the UK. In 2012, MIG standardized its planning and cost coding systems, successfully integrating site operations with commercial teams to enhance financial visibility and project controls. A significant milestone occurred in 2018 when the company secured framework agreements with leading cement suppliers, stabilizing material flows and pricing. The digital transformation accelerated in 2021 with the rollout of integrated weighbridge systems and electronic proof-of-delivery (e-POD) tracking tools across all operational sites.
Today, MIG manages between 25 and 40 concurrent construction sites, serving a diverse client portfolio that includes government bodies such as the Department for Transport and National Highways, regional councils, and private developers. The company maintains a workforce of approximately 850 employees and generates annual revenues exceeding £350 million, with sustained year-over-year growth. MIG's operational capabilities span full-service civil engineering, groundworks, reinforced concrete structures, and major infrastructure delivery.
MIG's competitive advantages are built on three core pillars. 
First, standardized data capture across all sites ensures consistent operational intelligence. 
Second, framework agreements with suppliers provide stable pricing and guaranteed material availability. Third, strong digital adoption—including IoT-enabled weighbridges, tablet-based site reporting, and e-POD systems—positions MIG ahead of competitors in operational visibility. Additionally, the company's commitment to sustainability through waste reduction and carbon footprint minimization has become a key differentiator in an increasingly environmentally conscious construction sector.
Cement is mission-critical for MIG's infrastructure projects, yet demand forecasting remains highly volatile due to the complex interplay of pour schedules, weather conditions, and site-specific ground conditions. MIG currently relies on rolling 4-week construction schedules and manual estimator-driven projections, resulting in significant operational inefficiencies with direct financial consequences.

Problem Statement: MIG lacks a reliable, data-driven cement demand forecasting system, leading to unpredictable inventory levels, reactive ordering patterns, and inefficient resource allocation across its 25–40 active construction sites.

### Key Obstacles & Pain Points:
Stockouts and Idle Resources: When cement is unavailable for scheduled pours, crews remain idle while equipment stands unused. This directly impacts project timelines and exposes MIG to contractual penalty clauses.
Overstocking and Capital Tie-up: Excessive cement inventory strains silo capacity, risks material expiry (particularly for specialized grades), and ties up working capital that could be deployed elsewhere.
Reactive Ordering Culture: Last-minute urgent deliveries command premium pricing and disrupt supplier logistics, eroding the benefits of MIG's framework agreements.
Limited Visibility: Planning relies on disparate spreadsheets, preventing meaningful site-level optimization or consolidation of purchasing power across multiple sites.
Business Impact: These issues collectively inflate material and logistics costs, damage client confidence through project delays, and undermine MIG's sustainability objectives by generating unnecessary waste and associated embodied carbon. Leadership recognizes that addressing these forecasting challenges is essential for maintaining competitive positioning and achieving strategic growth targets.
Why It Matters: Without accurate demand forecasting, MIG cannot optimize its supply chain, control costs, or deliver the predictable project outcomes that clients expect. A proactive, data-driven approach is essential to transform cement logistics from a source of operational friction into a strategic advantage.
Rational for the Project
Concept Overview: This project aims to develop a robust demand forecasting system for cement across MIG's multi-site operations. The solution will combine historical consumption patterns, planned pour schedules, real-time inventory positions, and external weather data to generate accurate site-level forecasts. The outputs will drive automated reorder point calculations and silo utilization planning.
Industry Relevance: Cement is inherently bulky, perishable, and critical to construction project schedules. Major contractors increasingly adopt data-driven forecasting to reduce delays, minimize waste, and mitigate supply chain risk. This project positions MIG at the forefront of this industry transformation.
Strategic Drivers:
•	Operational Efficiency: Guarantee "pour-ready" availability across all sites while minimizing idle time and schedule disruptions.
•	Data-Driven Decision-Making: Replace reactive, manual ordering with proactive, evidence-based procurement strategies.
•	Cost Optimization: Reduce material waste and capital tie-up by precisely aligning inventory levels with actual demand and silo capacity.
•	Resource Optimization: Improve crew utilization by eliminating stockout-related downtime.
•	Continuous Improvement: Establish a feedback loop where forecast accuracy is systematically measured and improved.
•	Sustainability: Support MIG's environmental commitments by reducing material waste and associated embodied carbon emissions.
Strategic Outcome: A scalable forecasting solution that reduces operational risk, enhances supply chain visibility, and delivers measurable financial and environmental returns through improved inventory management across MIG's national operations.

### Proejct Objectives
Forecast Accuracy: Achieve Mean Absolute Percentage Error (MAPE) ≤ 15% for 8-week site-level cement demand forecasts. This target ensures reliable predictions that support confident procurement and inventory decisions.
Service Level: Achieve ≥ 98% pour readiness, meaning no stockouts occur at scheduled pours across all sites. This metric directly addresses the business impact of idle crews and project delays.
Inventory Efficiency: Realize a 20% improvement in inventory utilization and a 30% reduction in write-offs by aligning stock levels with forecasted demand and site-specific silo capacities.
Decision Visibility: Deploy an interactive Plotly Dash application providing operations managers with real-time access to forecasts, automated reorder alerts, and silo utilization metrics at both site and aggregate levels.

### Data & Dataset Design
Data Requirements Overview
The project requires integrated data from multiple operational sources to enable comprehensive forecasting and inventory simulation:
Types of Data:
•	Operational Data: Daily cement consumption, planned pour quantities, and site-specific silo capacities.
•	Logistics Data: Opening inventory positions, daily deliveries received, and closing inventory balances.
•	External Data: Local weather conditions including rainfall and temperature that impact concrete setting times and pour feasibility.

### Data Sources:
•	Site-level weighbridge systems (consumption and delivery data).
•	Project management systems (planned pour schedules).
•	Inventory management spreadsheets (stock positions).
•	External weather APIs (daily precipitation and temperature).
•	Supplier delivery logs (real-time shipment tracking).

### Core Tables (Data Dictionary)
Table: Cement_Demand
Description: Daily site-level cement consumption, inventory, and environmental data.
Primary Key: (date, site_id, cement_type)
Foreign Keys: None explicitly provided
 
 
Column Name	Data Type	Description
date	DATE	Daily timestamp for the record
site_id	VARCHAR	Unique identifier for each construction site
cement_type	VARCHAR	Cement grade (e.g., CEM_I, CEM_II)
consumed_tonnes	FLOAT	Actual daily cement consumption in tonnes
planned_pour_tonnes	FLOAT	Scheduled pour quantities in tonnes
opening_inventory_tonnes	FLOAT	Start-of-day inventory position in tonnes
deliveries_tonnes	FLOAT	Cement deliveries received in tonnes
closing_inventory_tonnes	FLOAT	End-of-day inventory position in tonnes
rain_mm	FLOAT	Daily rainfall in millimeters
avg_temp_c	FLOAT	Average daily temperature in Celsius
silo_capacity	FLOAT	Maximum site silo storage in tonnes

### Data Model

### Entity Relationships:
The Cement_Demand table serves as the central fact table, linking operational consumption, logistics, and environmental data at the site-day-cement_type grain.
Table Relationships:
•	One-to-many relationship between site_id and daily records (each site has multiple daily observations).
•	One-to-many relationship between cement_type and daily consumption records.
•	Inventory balance integrity: closing_inventory = opening_inventory + deliveries - consumed.
Data Integrity Considerations:
•	Primary key uniqueness ensures no duplicate site-day-type records.
•	Referential integrity checks prevent orphaned inventory records.
•	Balance validation rules detect data entry errors and system integration issues.
•	Historical data must maintain consistent schema across time periods.
 
### Dataset Download Link
Technological Stack
Layer	Tool / Technology	Purpose
Database	SQLite	Lightweight, versionable data storage for historical and simulation data
Data Processing	Python (pandas, numpy)	Data ingestion, cleaning, transformation, and feature engineering
Machine Learning	scikit-learn, statsmodels	Time-series modeling, forecasting with external regressors, and model evaluation
Visualization & App	Plotly, Dash	Multi-page dashboards for forecasts, inventory projections, and reorder alerts
Version Control	Git	Source code management, collaboration, and project versioning
 
### Data Science Scope
Step 1: Data Ingestion and Cleaning
Import site data from SQLite into Python pandas environment. Validate schema consistency, handle missing values, fix negative inventory or consumption entries, and ensure inventory flow balance equations hold across all records.
Step 2: Exploratory Data Analysis
Analyze demand patterns by site, cement type, and time periods. Identify seasonality, trends, and correlation with weather variables. Quantify impact of planned pours on actual consumption and detect outliers or data quality issues.
Step 3: Feature Engineering
Create lag features, rolling aggregates, and interaction variables. Engineer weather-adjusted pour indicators and calculate inventory turnover metrics to capture site-specific operational characteristics for modeling.
Step 4: Model Development
Baseline model using SARIMAX with external regressors. Compare against machine learning approaches including Random Forest with exogenous variables. Evaluate and select best-performing model using MAPE and RMSE metrics.
Step 5: Inventory Simulation
Forecast silo levels using predicted demand, scheduled deliveries, and opening inventory positions. Define dynamic reorder points for each site based on forecasted demand, lead times, and silo capacity constraints.
Step 6: Dashboard Application
Develop Plotly Dash application with interactive visualizations for forecasts, inventory projections, and reorder alerts. Enable site-level drill-down and aggregate views for operations management.
Step 7: Validation and Deployment
Validate model predictions against hold-out data. Deploy forecasting pipeline to production environment. Establish monitoring framework to track forecast accuracy and trigger model retraining when performance degrades beyond acceptable thresholds.

git add README.md