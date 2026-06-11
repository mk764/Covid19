import pandas as pd

# Load WHO COVID-19 data
who_covid_df = pd.read_csv(r'D:\DataAnalysis\VSCode\P3\raw data\WHO COVID-19 cases.csv')

# Get the latest cumulative deaths for each country
countries_by_deaths = who_covid_df.groupby('Country')['Cumulative_deaths'].max().sort_values(ascending=False)

# Display top 20 countries by deaths
print("="*60)
print("TOP 20 COUNTRIES BY COVID-19 DEATHS")
print("="*60)
print(f"{'Rank':<6}{'Country':<30}{'Deaths':>20}")
print("-"*60)

for rank, (country, deaths) in enumerate(countries_by_deaths.head(20).items(), 1):
    print(f"{rank:<6}{country:<30}{int(deaths):>20,}")

# Display full ranking
print("\n" + "="*60)
print("FULL RANKING (ALL COUNTRIES)")
print("="*60)
print(f"{'Rank':<6}{'Country':<30}{'Deaths':>20}")
print("-"*60)

for rank, (country, deaths) in enumerate(countries_by_deaths.items(), 1):
    print(f"{rank:<6}{country:<30}{int(deaths):>20,}")

# Create and save ranking to CSV
countries_ranking_df = pd.DataFrame({
    'Rank': range(1, len(countries_by_deaths) + 1),
    'Country': countries_by_deaths.index,
    'Cumulative_Deaths': countries_by_deaths.values.astype(int)
})

countries_ranking_df.to_csv(r'D:\DataAnalysis\VSCode\P3\countries_ranked_by_deaths.csv', index=False)
print("\n✓ Ranking saved to 'countries_ranked_by_deaths.csv'")
