import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

try:
    import geopandas as gpd
    HAS_GEOPANDAS = True
except ImportError:
    HAS_GEOPANDAS = False

# Load CSV files from raw data folder
daily_continent_df = pd.DataFrame(pd.read_csv(r'D:\DataAnalysis\VSCode\P3\raw data\daily_continent_data.csv'))
who_covid_df = pd.DataFrame(pd.read_csv(r'D:\DataAnalysis\VSCode\P3\raw data\WHO COVID-19 cases.csv'))

# Display basic information
print("Daily Continent Data:")
print(daily_continent_df.head())
print(f"\nShape: {daily_continent_df.shape}")
print(f"\nColumns: {daily_continent_df.columns.tolist()}")

print("\n" + "="*50 + "\n")

print("WHO COVID-19 Cases Data:")
print(who_covid_df.head())
print(f"\nShape: {who_covid_df.shape}")
print(f"\nColumns: {who_covid_df.columns.tolist()}")

# Create separate dataframes for each continent
print("\n" + "="*50 + "\n")
print("Creating separate dataframes for each continent...\n")

continents = who_covid_df['Continent'].unique()
continent_dfs = {}

for continent in continents:
    continent_dfs[continent] = who_covid_df[who_covid_df['Continent'] == continent]
    print(f"{continent}: {len(continent_dfs[continent])} countries")


# RANK COUNTRIES BY DEATHS
print("\n" + "="*50 + "\n")
print("RANKING COUNTRIES BY DEATHS\n")

# Get the latest cumulative deaths for each country
countries_by_deaths = who_covid_df.groupby('Country')['Cumulative_deaths'].max().sort_values(ascending=False)

# Display top 20 countries by deaths
print("Top 20 Countries by Cumulative Deaths:\n")
print(f"{'Rank':<6}{'Country':<30}{'Deaths':>15}")
print("-" * 52)

for rank, (country, deaths) in enumerate(countries_by_deaths.head(20).items(), 1):
    print(f"{rank:<6}{country:<30}{deaths:>15,.0f}")

# Display full ranking
print("\n" + "="*50 + "\n")
print("FULL RANKING (All Countries):\n")
print(f"{'Rank':<6}{'Country':<30}{'Deaths':>15}")
print("-" * 52)

for rank, (country, deaths) in enumerate(countries_by_deaths.items(), 1):
    print(f"{rank:<6}{country:<30}{deaths:>15,.0f}")



# Create a DataFrame with rankings
countries_ranking_df = pd.DataFrame({
    'Rank': range(1, len(countries_by_deaths) + 1),
    'Country': countries_by_deaths.index,
    'Cumulative_Deaths': countries_by_deaths.values
})

# Save to CSV
countries_ranking_df.to_csv(r'D:\DataAnalysis\VSCode\P3\countries_ranked_by_deaths.csv', index=False)
print("\nRanking saved to 'countries_ranked_by_deaths.csv'")

# DISPLAY BAR GRAPHS FOR TOP 10 COUNTRIES OF EACH CONTINENT
print("\n" + "="*50 + "\n")
print("Creating bar graphs for top 10 countries by continent (Cases vs Deaths)...\n")

continents_list = [c for c in who_covid_df['Continent'].unique() if c not in ['Uncategorized', 'island']]
num_continents = len(continents_list)

# Create subplots (2 rows, 3 columns for 6 continents)
fig, axes = plt.subplots(2, 3, figsize=(18, 12))
axes = axes.flatten()

for idx, continent in enumerate(continents_list):
    if idx < len(axes):
        # Get top 10 countries by cumulative cases for this continent
        continent_data = who_covid_df[who_covid_df['Continent'] == continent]
        top_10_countries = continent_data.groupby('Country')[['Cumulative_cases', 'Cumulative_deaths']].max().sort_values('Cumulative_cases', ascending=False).head(10)
        
        # Prepare data for plotting
        countries = top_10_countries.index
        x = np.arange(len(countries))
        width = 0.35
        
        # Create bars
        bars1 = axes[idx].bar(x - width/2, top_10_countries['Cumulative_cases'], width, label='Confirmed Cases', color='steelblue', alpha=0.8)
        bars2 = axes[idx].bar(x + width/2, top_10_countries['Cumulative_deaths'], width, label='Deaths', color='coral', alpha=0.8)
        
        # Customize the plot
        axes[idx].set_title(f'{continent}', fontsize=13, fontweight='bold')
        axes[idx].set_xlabel('Country', fontsize=10)
        axes[idx].set_ylabel('Count', fontsize=10)
        axes[idx].set_xticks(x)
        axes[idx].set_xticklabels(countries, rotation=45, ha='right', fontsize=9)
        axes[idx].legend(fontsize=9)
        axes[idx].grid(axis='y', alpha=0.3)
        
        # Format y-axis labels with commas
        axes[idx].yaxis.set_major_formatter(plt.FuncFormatter(lambda x, p: f'{int(x):,}'))

# Hide unused subplots
for idx in range(len(continents_list), len(axes)):
    axes[idx].axis('off')

plt.tight_layout()
plt.savefig(r'D:\DataAnalysis\VSCode\P3\top_10_countries_by_continent.png', dpi=300, bbox_inches='tight')
print("✓ Bar graph saved as 'top_10_countries_by_continent.png'")
plt.show()

# CREATE INTERACTIVE PLOTLY HTML MAP WITH TOP 10 COUNTRIES BY CONTINENT
print("\n" + "="*50 + "\n")
print("Creating interactive HTML map with top 10 countries by continent...\n")

from plotly.subplots import make_subplots

# Prepare data for all continents
subplot_data = []
for continent in continents_list:
    continent_data = who_covid_df[who_covid_df['Continent'] == continent]
    top_10 = continent_data.groupby('Country')[['Cumulative_cases', 'Cumulative_deaths']].max().sort_values('Cumulative_cases', ascending=False).head(10)
    subplot_data.append((continent, top_10))

# Create subplots with Plotly
num_subplots = len(subplot_data)
rows = (num_subplots + 1) // 2
cols = 2
specs = [[{'type': 'bar'} for _ in range(cols)] for _ in range(rows)]
fig = make_subplots(
    rows=rows,
    cols=cols,
    subplot_titles=[data[0] for data in subplot_data],
    specs=specs,
    vertical_spacing=0.12,
    horizontal_spacing=0.1
)

# Add bars for each continent
for idx, (continent, top_10) in enumerate(subplot_data):
    row = (idx // 2) + 1
    col = (idx % 2) + 1
    
    # Add cases bars
    fig.add_trace(
        go.Bar(
            x=top_10.index,
            y=top_10['Cumulative_cases'],
            name='Confirmed Cases',
            marker=dict(color='steelblue'),
            showlegend=(idx == 0),
            hovertemplate='<b>%{x}</b><br>Cases: %{y:,}<extra></extra>'
        ),
        row=row, col=col
    )
    
    # Add deaths bars
    fig.add_trace(
        go.Bar(
            x=top_10.index,
            y=top_10['Cumulative_deaths'],
            name='Deaths',
            marker=dict(color='coral'),
            showlegend=(idx == 0),
            hovertemplate='<b>%{x}</b><br>Deaths: %{y:,}<extra></extra>'
        ),
        row=row, col=col
    )
    
    # Update x and y axes
    fig.update_xaxes(title_text='Country', row=row, col=col, tickangle=-45)
    fig.update_yaxes(title_text='Count', row=row, col=col)

# Update layout
fig.update_layout(
    title_text='COVID-19: Top 10 Countries by Continent (Confirmed Cases vs Deaths)',
    height=1000,
    width=1400,
    barmode='group',
    font=dict(size=10),
    hovermode='closest'
)

# Save to HTML
fig.write_html(r'D:\DataAnalysis\VSCode\P3\top_10_countries_by_continent.html')
print("✓ Interactive map saved as 'top_10_countries_by_continent.html'")
fig.show()
