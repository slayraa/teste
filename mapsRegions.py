import geopandas as gpd
from pathlib import Path
import pandas as pd

datafolder = Path.cwd()
shapefile = datafolder / "data/ne_110m_admin_0_countries/ne_110m_admin_0_countries.shp"

# Read shapefile using Geopandas
gdf = gpd.read_file(shapefile)[['ADMIN', 'ADM0_A3', 'geometry']]

# Rename columns
gdf.columns = ['country', 'country_code', 'geometry']
print(gdf.head())
#print(gdf[gdf['country'] == 'Antarctica'])

# Drop row corresponding to 'Antarctica'
gdf = gdf.drop(gdf.index[159])

datafile = datafolder / "data/obesity.csv"
# Read csv file using pandas
df = pd.read_csv(datafile, names=['entity', 'code', 'year', 'per_cent_obesity'], skiprows=1)
print(df.head())

# To keep it simple, let us ignore the missing data for Sudan.
#print(df.info())
df = df[~df['code'].isnull()]

# Filter data for 2016
df_2016 = df[df['year'] == 2016]
# Merge dataframes gdf and df_2016
merged = gdf.merge(df_2016, left_on='country_code', right_on='code')

print(merged.head())