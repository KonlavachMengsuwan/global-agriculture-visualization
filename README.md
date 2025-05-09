# Global Agriculture Visualization

This repository provides Python code for visualizing global agricultural production data from FAOSTAT. It generates several insightful visualizations including global maps, top producer rankings, crop portfolios, and yield vs area plots.

![3](https://github.com/user-attachments/assets/5068a0d2-ac19-4acc-87c5-cd87a768c277)



## 📌 Objective

The goal of this project is to explore and visualize global agricultural production patterns using publicly available FAOSTAT data. It provides interactive and static plots to analyze production, yield, and crop distribution at country level.

## 🗂️ Dataset

- Source: [FAOSTAT Production Data](https://www.fao.org/faostat/en/#data/QC)
- Data Type: CSV export from FAOSTAT (Production - Crops and Livestock Primary)
- Example file: `FAOSTAT_data_en_5-9-2025.csv`

Columns include:
- `Area`: Country name
- `Item`: Crop or product
- `Element`: Measurement type (e.g., Production, Area harvested)
- `Year`: Year
- `Value`: Numeric value (e.g., tonnes)

## 📊 Visualizations

The code generates:
1. **Top 10 producing countries bar chart** (for wheat)
2. **Global map of yield (tonnes/ha)** (for wheat)
3. **Top 10 crops produced in a selected country (e.g., India)**
4. **Scatter plot of yield vs area harvested**

## 🚀 How to Run

1. Clone this repo or copy the notebook into Google Colab
2. Upload your FAOSTAT CSV when prompted
3. Visualizations will be generated automatically

## 📝 Requirements

- `pandas`
- `plotly`
- `matplotlib`
- `pycountry`

Install with:

```bash
pip install pandas plotly pycountry matplotlib
```


---

## ✅ **3. Code (Python script):**

Use the same **latest working code (from Colab) as a `.py` script:**

```python
# global_agriculture_visualization.py

import pandas as pd
import plotly.express as px
import pycountry
import matplotlib.pyplot as plt

# ✅ Load FAOSTAT CSV manually
fao_file = input("Enter the path to your FAOSTAT CSV file: ")
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

# 1️⃣ Top 10 producing countries bar chart
top10 = prod.sort_values('Value', ascending=False).head(10)
plt.figure(figsize=(10,6))
plt.bar(top10['Area'], top10['Value'], color='green')
plt.ylabel('Production (tonnes)')
plt.title('Top 10 Wheat Producing Countries (2023)')
plt.xticks(rotation=45)
plt.show()

# 2️⃣ Global map of yield (tonnes/ha)
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

# 3️⃣ Crop portfolio bar chart per country (top 10 items)
country_name = 'India'  # change country if needed
portfolio = fao[(fao['Area'] == country_name) & (fao['Element'] == 'Production') & (fao['Year'] == 2023)]
portfolio = portfolio.groupby('Item')['Value'].sum().sort_values(ascending=False).head(10)

plt.figure(figsize=(12,6))
plt.bar(portfolio.index, portfolio.values, color='orange')
plt.ylabel('Production (tonnes)')
plt.title(f'{country_name} Top 10 Crop Production (2023)')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.show()

# 4️⃣ Yield vs Area scatter plot
plt.figure(figsize=(10,6))
plt.scatter(merged['Value_area'], merged['Yield'])
plt.xscale('log')
plt.xlabel('Area harvested (ha, log scale)')
plt.ylabel('Yield (tonnes/ha)')
plt.title('Wheat Yield vs Area Harvested (2023)')
plt.show()
```
![1](https://github.com/user-attachments/assets/71267ab5-f93c-4b56-8420-af24239784f1)
![2](https://github.com/user-attachments/assets/05023928-e68a-4546-8741-3db183c886d3)
![4](https://github.com/user-attachments/assets/dc0d9b34-7277-489f-9a0b-92e3da3b9596)

Code: https://colab.research.google.com/drive/1BdZHim83vIDR0Y1YGuQnBiivk8j9s9FM?usp=sharing

