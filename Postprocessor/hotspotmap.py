import pandas as pd
import numpy as np
import json
import plotly.express as px
import plotly
import sys

file = sys.argv[1]
areas = sys.argv[2]
type = sys.argv[3]

def reshape_dataset(dtfrm):
    out_df = pd.DataFrame()
    day_col = dtfrm['day']
    col_name = dtfrm.iloc[:, 1].name
    col_data = dtfrm.iloc[:, 1]
    region_name = pd.Series(len(dtfrm.iloc[:, 1]) * [col_name])
    out_df['day'] = day_col
    out_df['cases'] = col_data
    out_df['region'] = region_name
    # day_col_size=len(dtfrm['day'])
    for i in range(2, len(dtfrm.columns)):
        temp_df = pd.DataFrame()
        col_name = dtfrm.iloc[:, i].name
        col_data = dtfrm.iloc[:, i]
        region_name = pd.Series(len(dtfrm.iloc[:, i]) * [col_name])
        temp_df['day'] = day_col
        temp_df['cases'] = col_data
        temp_df['region'] = region_name

        out_df = out_df.append(temp_df)
    out_df.sort_values('day', inplace=True)
    return out_df


data = pd.read_csv(file)

with open(areas) as f:
    geojso = json.load(f)

for i in range(0, len(geojso["features"])):
    for j in range(0, len(geojso["features"][i]['geometry']['coordinates'])):
        try:
            geojso["features"][i]['geometry']['coordinates'][j] = np.round(
                np.array(geojso["features"][i]['geometry']['coordinates'][j]), 3)
        except:
            print(i, j)

test = reshape_dataset(data.iloc[:, :-1])


if (type == "dynmaic"):
    # Dynamic Scale range
    # Create figure
    fig = px.choropleth_mapbox(test, geojson=geojso, locations='region', color='cases', featureidkey='properties.id',
                               animation_frame='day',
                               color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                               mapbox_style="carto-positron",
                               zoom=10, center={"lat": 33.6937, "lon": 73.0652},

                               )
    # Define layout specificities
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})
else:
    # Static Scale range
    fig = px.choropleth_mapbox(test, geojson=geojso, locations='region', color='cases', featureidkey='properties.id',
                               animation_frame='day',
                               color_continuous_scale=px.colors.diverging.RdYlGn[::-1],
                               range_color=(0, test['cases'].max()),
                               mapbox_style="carto-positron",
                               zoom=10, center={"lat": 33.6937, "lon": 73.0652},

                               )

    # Define layout specificities
    fig.update_layout(margin={'r': 0, 't': 0, 'l': 0, 'b': 0})

plotly.offline.plot(fig, filename='hotspot-map.html')
