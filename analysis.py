import pandas as pd

# Load dataset
df = pd.read_csv('bank-additional-full.csv', sep=';')

# ── CLEAN ──────────────────────────────
# Convert y to 1/0 for easier analysis
df['converted'] = df['y'].apply(lambda x: 1 if x == 'yes' else 0)

# Create age groups
df['age_group'] = pd.cut(df['age'], 
                          bins=[0,25,35,45,55,65,100],
                          labels=['<25','25-35','35-45','45-55','55-65','65+'])

# Create call duration in minutes
df['duration_mins'] = round(df['duration'] / 60, 2)

# ── FUNNEL STAGES ──────────────────────
funnel = pd.DataFrame({
    'Stage': ['Total Contacted', 'Engaged (duration>0)', 
              'Interested (previous>0)', 'Converted'],
    'Count': [
        len(df),
        len(df[df['duration'] > 0]),
        len(df[df['previous'] > 0]),
        len(df[df['converted'] == 1])
    ]
})
funnel['Conversion_Rate'] = round(funnel['Count'] / len(df) * 100, 2)

# ── EXPORT CSVs FOR POWER BI ───────────
df.to_csv('clean_data.csv', index=False)
funnel.to_csv('funnel_stages.csv', index=False)

# Conversion by job
df.groupby('job')['converted'].mean().mul(100).round(2)\
  .reset_index().rename(columns={'converted':'conversion_rate'})\
  .to_csv('conversion_by_job.csv', index=False)

# Conversion by age group
df.groupby('age_group', observed=True)['converted'].mean().mul(100).round(2)\
  .reset_index().rename(columns={'converted':'conversion_rate'})\
  .to_csv('conversion_by_age.csv', index=False)

# Conversion by month
df.groupby('month')['converted'].mean().mul(100).round(2)\
  .reset_index().rename(columns={'converted':'conversion_rate'})\
  .to_csv('conversion_by_month.csv', index=False)

print("All files exported successfully!")
print("\nFunnel Stages:")
print(funnel)