# This line gave an error since Jinja2 doesn't export Markup anymore.
# I edited it directly in the concerned package file: imported Markup from markupsafe instead.
from itertools import count
import holoviews as hv # Holoviews is actually designed to work with Jupyter notebook
from holoviews import opts
hv.extension('bokeh') # This is because holoviews can also work with other plotting libraries
from os.path import abspath
import webbrowser
import pandas as pd
from bokeh.sampledata.us_counties import data as counties

dataframe = pd.read_csv('census2010.csv', encoding="ISO-8859-1")
dataframe = pd.DataFrame(
    dataframe, 
    columns=['Target Geo Id2', 
    'Geographic area.1', 
    'Density per square mile of land area - Population'])

dataframe.rename(columns={
    'Target Geo Id2':'fips', 
    'Geographic area.1':'County', 
    'Density per square mile of land area - Population':'Density'
}, inplace=True)

print(f"\nInitial population data:\n {dataframe.head()}")
print(f"Shape of df = {dataframe.shape}\n")

dataframe = dataframe[dataframe['fips'] > 100]
# This sets the counties with density bigger than 65 people per square mile 
# to very high, so you can clearly see which counties to avoid
dataframe.loc[dataframe.Density >= 65, ['Density']] = 1000

print(f"Population data with non-county rows removed:\n {dataframe.head()}\n")
print(f"Shape of df = {dataframe.shape}\n")

# Get state id and county id from fips, which contains them both.
# //  is floor division (with no numbers after decimal point)
dataframe['state_id'] = (dataframe['fips'] // 1000).astype('int64')
dataframe['cid'] = (dataframe['fips'] % 1000).astype('int64')

print(f"Population data with new Id columns:\n {dataframe.head()}\n")
print(f"Shape of df = {dataframe.shape}\n")
print(f"Dataframe info:\n")
print(dataframe.info())

# Here we turn the dataframe data into a dictionary with the tuple of state and cid as key.
# This is to make it have the same format as the unemployment data (used in the example 
# mentioned in the book)
state_ids = dataframe.state_id.tolist()
cids = dataframe.cid.tolist()
densities = dataframe.Density.tolist()

tuple_list = tuple(zip(state_ids, cids))
population_density_dict = dict(zip(tuple_list, densities))

EXCLUDED = ('ak', 'hi', 'pr', 'gu', 'vi', 'mp', 'as')

# The 'counties' in counties.items() comes from the imported dataset, that is also called counties
counties = [dict(county, Density=population_density_dict[cid])
for cid, county in counties.items() if population_density_dict.get(cid) != None and county["state"] not in EXCLUDED]

print(counties[0])

chloropleth = hv.Polygons(counties, 
['lons', 'lats'],
[('detailed name', 'County'), 'Density'] # This is for hover tooltip
)

chloropleth.opts(opts.Polygons(logz=True,
tools=['hover'], # This enables the tooltip. There are also other tools, such as save, zoom and pan
xaxis=None,
yaxis=None,
show_grid=False,
show_frame=False,
width=1300,
height=780,
colorbar=True,
toolbar='above',
color_index='Density',
cmap="GnBu",
line_color=None,
title="2010 population density per square mile"
))

hv.save(chloropleth, 'chloropleth.html', backend='bokeh')
url=abspath('chloropleth.html')
webbrowser.open(url)