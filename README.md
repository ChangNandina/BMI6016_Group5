Team Members 

Abbey Marye	abbey.marye@utah.edu

Sandi Alshahwan	sandi.alshahwan@utah.edu

Chang Ni	chang.ni@utah.edu

Kim Lanaghen	kim.lanaghen@utah.edu

Clara Garcia	clara.garcia@utah.edu


## Data Sources

- **Vaccine Hesitancy Data**: [Vaccine Hesitancy for COVID-19: County and Local Estimates](https://data.cdc.gov/Vaccinations/Vaccine-Hesitancy-for-COVID-19-County-and-local-es/q9mh-h2tw) (CDC)
- **COVID-19 Deaths Data**: [JHU CSSE COVID-19 Time Series - Deaths (US)](https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_time_series) (Johns Hopkins University)

## Datasets

### 1. `combined_hesitancy_death_rate.csv`

Weekly COVID-19 death rates (new deaths per week) combined with vaccine hesitancy estimates.

| Column | Description |
|--------|-------------|
| `FIPS` | Federal Information Processing Standards county code |
| `County` | County name |
| `State` | State name |
| `Population` | County population |
| `Hesitancy_Rate` | Estimated proportion of population hesitant to receive COVID-19 vaccine |
| `YYYY-WW` | Weekly death rate per 100,000 population (new deaths that week) |

### 2. `combined_hesitancy_cumulative_death_rate.csv`

Cumulative COVID-19 death rates combined with vaccine hesitancy estimates.

| Column | Description |
|--------|-------------|
| `FIPS` | Federal Information Processing Standards county code |
| `County` | County name |
| `State` | State name |
| `Population` | County population |
| `Hesitancy_Rate` | Estimated proportion of population hesitant to receive COVID-19 vaccine |
| `YYYY-WW` | Cumulative death rate per 100,000 population (total deaths up to that week) |

## Key Differences Between Datasets

| Feature | `death_rate.csv` | `cumulative_death_rate.csv` |
|---------|------------------|----------------------------|
| Metric | Weekly new deaths | Total deaths to date |
| Trend | Fluctuates weekly | Monotonically increasing |
| Use Case | Analyzing outbreak patterns, peak mortality periods | Analyzing overall mortality burden, long-term trends |

## Data Processing

1. **Death Data Processing**:
   - Converted daily cumulative death counts to weekly aggregates
   - For weekly death rate: calculated daily new deaths, then summed by week
   - For cumulative death rate: extracted end-of-week cumulative values
   - Normalized to rate per 100,000 population

2. **Data Merging**:
   - Merged datasets using FIPS county codes
   - Retained only counties present in both datasets

## Usage

```python
import pandas as pd

# Load weekly death rate data
weekly_df = pd.read_csv('combined_hesitancy_death_rate.csv')

# Load cumulative death rate data
cumulative_df = pd.read_csv('combined_hesitancy_cumulative_death_rate.csv')

# Example: correlation between hesitancy and cumulative death rate
last_week = cumulative_df.columns[-1]
correlation = cumulative_df['Hesitancy_Rate'].corr(cumulative_df[last_week])
print(f"Correlation: {correlation:.4f}")
