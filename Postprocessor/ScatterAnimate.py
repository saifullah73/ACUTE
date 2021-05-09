import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import  plotly as py
import pandas as pd
import sys
import os
from os import walk
import glob
import fnmatch
import numpy as np
#
# path = os.getcwd() + '/sample_output'
# print(path)
# # path = sys.argv[1]
# df_name = []
# df_list = []
# for root, dirs, files in os.walk(path, topdown=False):
#     for name in files:
#         if "covid_out_infections_small.csv" in name:
#             filepath = os.path.join(root, name)
#             df = pd.read_csv(filepath)
#             columns = ["time",  "x", "y", "type"]
#             df.columns = columns
#             for column in df:
#                 df_name.append(column)
#             df_list.append(df)
# # df = pd.read_csv(path)
# # columns = ["time",  "x", "y", "location_type"]
# # df.columns = columns
# # for column in df:
# #     df_name.append(column)
# # df_list.append(df)
# df = pd.concat(df_list, axis=1, ignore_index=True)
# df.columns = df_name
# # df = df[(df['time']>0) & (df['time']<=414)]
# df = df[(df['time']>0)]


df_name = []
df_list = []
df = pd.read_csv('sample_output/covid_out_infections.csv')
columns = ["time",  "x", "y", "type"]
df.columns = columns
for column in df:
    df_name.append(column)
df_list.append(df)




df = pd.concat(df_list, axis=1, ignore_index=True)
df.columns = df_name
# df = df[(df['time']>0) & (df['time']<=414)]
df = df[(df['time']>0)]




#create dataframe for each day
cdf = pd.DataFrame(columns = ["time",  "x", "y", "type"])
frames = []
grouped = df.groupby('time')
for group in grouped:
      day = group[0]
      data = df[(df['time']<=day)]
      data['time'] = day
      print(day, "  ", len(group[1]), "  ", len(data))
      cdf = cdf.append(data, ignore_index = True)

x = cdf['x'].mean()
y = cdf['y'].mean()
print(x,y)
cdf['size'] = 1

# cdf2 = cdf[(cdf['time']<=20)]
# cdf2['type'].unique()

# color_discrete_map = {'house': px.colors.qualitative.G10[1],
#                       'office': px.colors.qualitative.G10[5],
#                       'shopping': px.colors.qualitative.G10[2],
#                       'school': px.colors.qualitative.G10[4],
#                       'leisure': px.colors.qualitative.G10[3],
#                       'park': px.colors.qualitative.G10[7],
#                       'hospital': px.colors.qualitative.G10[6],
#                       'traffic': px.colors.qualitative.G10[0],
#                       'place_of_worship': px.colors.qualitative.G10[8]}

color_discrete_map = {'house': px.colors.qualitative.G10[1],
                      'office': px.colors.qualitative.G10[2],
                      'shopping': px.colors.qualitative.G10[3],
                      'school': px.colors.qualitative.G10[4],
                      'leisure': px.colors.qualitative.G10[5],
                      'park': px.colors.qualitative.G10[6],
                      'hospital': px.colors.qualitative.G10[7],
                      'traffic': px.colors.qualitative.G10[8],
                      'place_of_worship': px.colors.qualitative.G10[9]}


fig = px.scatter_mapbox(
    cdf, lat="y", lon="x",
    size= "size",
    color = "type",
    size_max=3,
    color_discrete_map=color_discrete_map,
    hover_name="type",
    animation_frame="time", animation_group="time",
)


# fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
# fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
# # fig.layout.coloraxis.showscale = True
# fig.layout.sliders[0].pad.t = 0
# fig.layout.sliders[0].x = 0
# fig.layout.sliders[0].y = -0.1
# fig.layout.updatemenus[0].pad.t= 0
# fig["layout"].pop("updatemenus")
# fig.layout.mapbox={
#                       'accesstoken':'pk.eyJ1IjoiaW1haG1vb2QiLCJhIjoiY2tjdnE0MDBjMDZuYjJ6cXY2aGE4OWN2aCJ9.bRfBBl_o-iRCv90oKtqdsA',
#                       'center':{"lat": y, "lon":x},
#                       'zoom':11,
#                       'style':'open-street-map'
#                   }
# fig.update_layout(
#     title='Islamabad - Locationwise Infected Cases per day',
#     width = 1024,
#     height = 600,
#     legend=dict(
#         title = 'Building Type',
#         orientation="h",
#         y=0,
#         x=0,
#         traceorder='reversed'
#     )
# )
# py.offline.plot(fig, filename='scatter_animate.html')
# fig.show()

fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 200
fig.layout.updatemenus[0].buttons[0].args[1]["transition"]["duration"] = 200
fig.layout.coloraxis.showscale = True
fig.layout.sliders[0].pad.t = 0
fig.layout.sliders[0].x = 0
fig.layout.sliders[0].y = -0.1
fig.layout.updatemenus[0].pad.t= 0
fig["layout"].pop("updatemenus")
fig.layout.mapbox={
                      'accesstoken':'pk.eyJ1IjoiaW1haG1vb2QiLCJhIjoiY2tjdnE0MDBjMDZuYjJ6cXY2aGE4OWN2aCJ9.bRfBBl_o-iRCv90oKtqdsA',
                      'center':{"lat":y, "lon":x},
                      'zoom':11,
                      'style':'open-street-map'
                  }


fig.update_layout(
    title='Islamabad - Locationwise Infected Cases per day',
    width = 1280,
    height = 600,
    legend=dict(
        title = 'Building Type',
        orientation="h",
        y=0,
        x=0,
        traceorder='reversed'
    )
)
py.offline.plot(fig, filename='scatter_animate.html')
# fig.show()