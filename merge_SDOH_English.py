import pandas as pd
import numpy as np

# ========== 1. Load existing data and SDOH data ==========

# Load the previously combined hesitancy + death rate data
combined_df = pd.read_csv('combined_hesitancy_death_rate.csv')

# Load SDOH data
# Download from: https://data.cdc.gov/ (SDOH Measures for County, ACS 2017-2021)
sdoh = pd.read_csv('Non-Medical_Factor_Measures_for_County__ACS_2017-2021.csv/Non-Medical_Factor_Measures_for_County__ACS_2017_2021.csv')

print("=== SDOH Data Overview ===")
print(f"Shape: {sdoh.shape}")
print(f"\nColumn names: {sdoh.columns.tolist()}")
print(f"\nUnique SDOH measures (Short_Question_Text):")
print(sdoh['Short_Question_Text'].unique())

# ========== 2. Clean and prepare SDOH data ==========

# Keep only the columns we need:
# - LocationID: FIPS code for matching
# - Short_Question_Text: describes what the measure is (e.g., "Crowding")
# - Data_Value: the actual percentage value
sdoh_clean = sdoh[['LocationID', 'LocationName', 'StateAbbr', 'Short_Question_Text', 'Data_Value']].copy()

# Rename columns for clarity
sdoh_clean = sdoh_clean.rename(columns={
    'LocationID': 'FIPS',
    'LocationName': 'County',
    'StateAbbr': 'State',
    'Short_Question_Text': 'SDOH_Measure',
    'Data_Value': 'Value'
})

# Convert FIPS to numeric for matching
sdoh_clean['FIPS'] = pd.to_numeric(sdoh_clean['FIPS'], errors='coerce')

# ========== 3. Reshape SDOH data from long to wide format ==========

# Original format (long): each row is one county + one SDOH measure
# Target format (wide): each row is one county, each SDOH measure is a column

sdoh_wide = sdoh_clean.pivot_table(
    index='FIPS',
    columns='SDOH_Measure',
    values='Value',
    aggfunc='first'  # In case of duplicates, take the first value
).reset_index()

# Add 'SDOH_' prefix to all measure columns for easy identification
sdoh_wide.columns = ['FIPS'] + ['SDOH_' + col for col in sdoh_wide.columns[1:]]

print(f"\n=== SDOH Data (Wide Format) ===")
print(f"Shape: {sdoh_wide.shape}")
print(f"Number of SDOH measures: {len(sdoh_wide.columns) - 1}")
print(f"\nSDOH measures included:")
for col in sdoh_wide.columns[1:]:
    print(f"  - {col}")

# ========== 4. Merge SDOH with existing combined data ==========

# Make sure FIPS types match
combined_df['FIPS'] = pd.to_numeric(combined_df['FIPS'], errors='coerce')

# Merge on FIPS code (inner join keeps only counties present in both datasets)
final_dataset = combined_df.merge(
    sdoh_wide,
    on='FIPS',
    how='inner'
)

print(f"\n=== Merge Summary ===")
print(f"Original combined data rows: {len(combined_df)}")
print(f"SDOH data counties: {len(sdoh_wide)}")
print(f"After merge rows: {len(final_dataset)}")
print(f"Total columns: {len(final_dataset.columns)}")

# ========== 5. Analyze correlation between SDOH and Vaccine Hesitancy ==========

print(f"\n=== Correlation Analysis: SDOH vs Vaccine Hesitancy ===")

# Get all SDOH column names
sdoh_cols = [col for col in final_dataset.columns if col.startswith('SDOH_')]

# Calculate correlation for each SDOH measure
correlations = {}
for col in sdoh_cols:
    corr = final_dataset['Hesitancy_Rate'].corr(final_dataset[col])
    correlations[col] = corr

# Sort by absolute correlation value (strongest relationships first)
corr_sorted = sorted(correlations.items(), key=lambda x: abs(x[1]) if not np.isnan(x[1]) else 0, reverse=True)

print("\nCorrelation between SDOH measures and Vaccine Hesitancy Rate:")
print("-" * 65)
print(f"{'SDOH Measure':<45} {'Correlation':>15}")
print("-" * 65)
for measure, corr in corr_sorted:
    if not np.isnan(corr):
        # Remove 'SDOH_' prefix for cleaner display
        measure_name = measure.replace('SDOH_', '')
        print(f"{measure_name:<45} {corr:>15.4f}")

# ========== 6. Reorder columns and save ==========

# Desired column order:
# 1. Basic info (FIPS, County, State, Population)
# 2. Hesitancy Rate
# 3. SDOH measures
# 4. Weekly death rates (date columns)

info_cols = ['FIPS', 'County', 'State', 'Population', 'Hesitancy_Rate']

# Get date columns (weekly death rates) - they contain year format like "2020-01" or "2021/1/1"
date_cols = [col for col in final_dataset.columns 
             if col not in info_cols and not col.startswith('SDOH_')]

# Final column order
final_cols = info_cols + sdoh_cols + date_cols
final_dataset = final_dataset[final_cols]

print(f"\n=== Preview of Final Dataset ===")
print(final_dataset.head())

# Save to CSV
final_dataset.to_csv('combined_hesitancy_sdoh_death_rate.csv', index=False)
print(f"\nSaved as: combined_hesitancy_sdoh_death_rate.csv")

# ========== 7. Also process cumulative death rate version ==========

print(f"\n=== Processing cumulative death rate version ===")

cumulative_df = pd.read_csv('combined_hesitancy_cumulative_death_rate.csv')
cumulative_df['FIPS'] = pd.to_numeric(cumulative_df['FIPS'], errors='coerce')

# Merge with SDOH data
final_cumulative = cumulative_df.merge(
    sdoh_wide,
    on='FIPS',
    how='inner'
)

# Reorder columns
date_cols_cum = [col for col in final_cumulative.columns 
                 if col not in info_cols and not col.startswith('SDOH_')]
final_cols_cum = info_cols + sdoh_cols + date_cols_cum
final_cumulative = final_cumulative[final_cols_cum]

# Save
final_cumulative.to_csv('combined_hesitancy_sdoh_cumulative_death_rate.csv', index=False)
print(f"Saved as: combined_hesitancy_sdoh_cumulative_death_rate.csv")

print(f"\n=== All done! ===")
print(f"Generated files:")
print(f"  1. combined_hesitancy_sdoh_death_rate.csv (weekly death rates)")
print(f"  2. combined_hesitancy_sdoh_cumulative_death_rate.csv (cumulative death rates)")