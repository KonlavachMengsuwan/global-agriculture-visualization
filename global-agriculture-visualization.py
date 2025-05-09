# ✅ Install packages
!pip install pandas plotly pycountry matplotlib

import pandas as pd
import plotly.express as px
import pycountry
import matplotlib.pyplot as plt

# ✅ Upload CSV manually
from google.colab import files
uploaded = files.upload()

for fn in uploaded.keys():
    fao_file = fn
print(f"Uploaded file: {fao_file}")

# ✅ Load FAOSTAT CSV
fao = pd.read_csv(fao_file)

print("FAOSTAT shape:", fao.shape)
print(fao.head())

# ✅ Map country names to ISO3
def country_to_iso3(country_name):
    try:
        return pycountry.countries.lookup(country_name).alpha_3
    except:
        return None

# ✅ Filter for wheat production in 2023
prod = fao[(fao['Item'] == 'Wheat') & (fao['Element'] == 'Production') & (fao['Year'] == 2023)]
area = fao[(fao['Item'] == 'Wheat') & (fao['Element'] == 'Area harvested') & (fao['Year'] == 2023)]

# =========================
# 1️⃣ Top 10 producing countries bar chart
# =========================
top10 = prod.sort_values('Value', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top10['Area'], top10['Value'], color='green')
plt.ylabel('Production (tonnes)')
plt.title('Top 10 Wheat Producing Countries (2023)')
plt.xticks(rotation=45)
plt.show()

# =========================
# 2️⃣ Global map of yield (tonnes/ha)
# =========================
merged = pd.merge(prod[['Area','Value']], area[['Area','Value']], on='Area', suffixes=('_prod','_area'))
merged['Yield'] = merged['Value_prod'] / merged['Value_area']
merged['iso_alpha'] = merged['Area'].apply(country_to_iso3)
merged = merged.dropna(subset=['iso_alpha'])

fig = px.choropleth(
    merged,
    locations='iso_alpha',
    color='Yield',
    hover_name='Area',
    color_continuous_scale='Viridis',
    projection='natural earth',
    title='Global Wheat Yield (tonnes/ha, 2023)',
    labels={'Yield': 'Yield (t/ha)'}
)
fig.show()

# =========================
# 3️⃣ Crop portfolio bar chart per country (top 10 items, better spacing)
# =========================
country_name = 'India'  # 👉 change country here if needed
portfolio = fao[(fao['Area'] == country_name) & (fao['Element'] == 'Production') & (fao['Year'] == 2023)]
portfolio = portfolio.groupby('Item')['Value'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
plt.bar(portfolio.index, portfolio.values, color='orange')
plt.ylabel('Production (tonnes)')
plt.title(f'{country_name} Top 10 Crop Production (2023)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()  # add spacing to prevent overlap
plt.show()

# =========================
# 4️⃣ Yield vs Area scatter plot
# =========================
plt.figure(figsize=(10,6))
plt.scatter(merged['Value_area'], merged['Yield'])
plt.xscale('log')
plt.xlabel('Area harvested (ha, log scale)')
plt.ylabel('Yield (tonnes/ha)')
plt.title('Wheat Yield vs Area Harvested (2023)')
plt.show()
