# BMI6016 Group 5 - COVID-19 Vaccine Hesitancy Analysis
Team Members 

Abbey Marye	abbey.marye@utah.edu

Sandi Alshahwan	sandi.alshahwan@utah.edu

Chang Ni	chang.ni@utah.edu

Kim Lanaghen	kim.lanaghen@utah.edu

Clara Garcia	clara.garcia@utah.edu

## Project Overview

This project analyzes the relationship between COVID-19 vaccine hesitancy, social determinants of health (SDOH), and COVID-19 death rates at the county level in the United States.

## Data Sources

Vaccine Hesitancy Data: Vaccine Hesitancy for COVID-19: County and Local Estimates (CDC)
COVID-19 Deaths Data: JHU CSSE COVID-19 Time Series - Deaths (US) (Johns Hopkins University)
SDOH Measures Data: https://catalog.data.gov/dataset/sdoh-measures-for-county-acs-2017-2021

## Generated Datasets

### 1. `combined_hesitancy_death_rate.csv`
- Weekly COVID-19 death rates (per 100,000 population) combined with vaccine hesitancy
- **Rows:** 3,140 counties
- **Columns:** 169 (FIPS, County, State, Population, Hesitancy_Rate, weekly death rates)

### 2. `combined_hesitancy_cumulative_death_rate.csv`
- Cumulative COVID-19 death rates combined with vaccine hesitancy
- Same structure as above but with cumulative rates

### 3. `combined_hesitancy_sdoh_death_rate.csv`
- Weekly death rates + vaccine hesitancy + SDOH measures
- **Rows:** 3,140 counties
- **Columns:** 178

### 4. `combined_hesitancy_sdoh_cumulative_death_rate.csv`
- Cumulative death rates + vaccine hesitancy + SDOH measures
- **Rows:** 3,140 counties
- **Columns:** 178

## SDOH Measures Included

| Column Name | Description |
|-------------|-------------|
| `SDOH_Poverty` | % of population below poverty level |
| `SDOH_No broadband` | % of households without broadband internet |
| `SDOH_No high school diploma` | % of adults without high school diploma |
| `SDOH_Unemployment` | % unemployment rate |
| `SDOH_Single-parent households` | % of single-parent households |
| `SDOH_Housing cost burden` | % of households with housing cost burden |
| `SDOH_Crowding` | % of households with crowding conditions |
| `SDOH_Aged 65 years or older` | % of population aged 65+ |
| `SDOH_Racial or ethnic minority status` | % racial/ethnic minority population |

## Key Findings: SDOH Correlation with Vaccine Hesitancy

| SDOH Measure | Correlation | Interpretation |
|--------------|-------------|----------------|
| **Poverty** | **+0.412** | 🔴 Strongest predictor |
| **No broadband** | **+0.394** | 🔴 Strong predictor |
| **No high school diploma** | **+0.279** | 🔴 Moderate predictor |
| Single-parent households | +0.185 | Weak positive |
| Unemployment | +0.158 | Weak positive |
| Housing cost burden | -0.153 | Weak negative |
| Aged 65 years or older | -0.055 | No significant correlation |
| Racial or ethnic minority status | +0.053 | No significant correlation |
| Crowding | +0.041 | No significant correlation |

### Summary of Findings

**Top 3 predictors of vaccine hesitancy:**
1. 💰 **Poverty** (r = 0.41) - Counties with higher poverty rates have higher vaccine hesitancy
2. 📡 **No broadband access** (r = 0.39) - Limited internet access correlates with higher hesitancy
3. 🎓 **No high school diploma** (r = 0.28) - Lower educational attainment correlates with higher hesitancy

These findings suggest that **economic factors** and **information access** are strongly associated with vaccine hesitancy at the county level.

## Data Processing Scripts

| Script | Description |
|--------|-------------|
| `merge_hesitancy_deaths.py` | Merges vaccine hesitancy data with COVID-19 death rates |
| `merge_SDOH_English.py` | Adds SDOH measures to the combined dataset |

## Column Descriptions

| Column | Description |
|--------|-------------|
| `FIPS` | 5-digit Federal Information Processing Standard county code |
| `County` | County name |
| `State` | State name |
| `Population` | County population |
| `Hesitancy_Rate` | Estimated % of population hesitant to receive COVID-19 vaccine |
| `SDOH_*` | Social Determinants of Health measures (see table above) |
| `YYYY-MM-DD/YYYY-MM-DD` | Weekly death rate per 100,000 population for that date range |

## How to Use

```python
import pandas as pd

# Load the complete dataset
df = pd.read_csv('combined_hesitancy_sdoh_death_rate.csv')

# View basic info
print(df.shape)
print(df.columns.tolist())

# Analyze correlation between hesitancy and a specific SDOH measure
correlation = df['Hesitancy_Rate'].corr(df['SDOH_Poverty'])
print(f"Correlation between Hesitancy and Poverty: {correlation:.4f}")
