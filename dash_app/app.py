# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
external_scripts = ['https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/assets/java_2.js', 'https://www.statcounter.com/counter/counter.js']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets, external_scripts=external_scripts)
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "COVID-19 in New York State - Interactive Map by PEESE @ Cornell Univerisity"

# app.scripts.append_script = html.Script(src='https://www.statcounter.com/counter/counter.js',type='text/javascript')
server = app.server

###################################################################################
###################################################################################


# app.scripts.append_script(html.Script(['var sc_project=12226718; ','var sc_invisible=1; ','var sc_security="2df363f3"; '],type='text/javascript'))
# app.scripts.append_script(html.Script(['var sc_project=12226718; ','var sc_invisible=1; ','var sc_security="2df363f3"; '],type='text/javascript'))

'''
app.scripts.append_script({
    'external_url':'https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/assets/java_1.js'
    })
app.scripts.append_script({
    'external_url':'https://www.statcounter.com/counter/counter.js'
    })
'''



# add other codes before the callback section
# https://community.plotly.com/t/append-script-when-dash-components-are-loaded/8023/4
# import grasia_dash_components as gdc

from base64 import urlsafe_b64encode
def write_to_data_uri(s):
    """
    Writes to a uri.
    Use this function to embed javascript into the dash app.
    Adapted from the suggestion by user 'mccalluc' found here:
    https://community.plotly.com/t/problem-of-linking-local-javascript-file/6955/2
    """
    uri = (
        ('data:;base64,').encode('utf8') +
        urlsafe_b64encode(s.encode('utf8'))
    ).decode("utf-8", "strict")
    return uri


from urllib.request import urlopen
import json
import pandas as pd
import plotly.graph_objects as go
import plotly as py
import math
import datetime
from dateutil import rrule
import numpy as np
import pandas as pd

import json

with urlopen('https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/NYS_Counties.geojson') as response:
    counties = json.load(response)

# ==================  Data  ===================

# display number of rows
pd.set_option('display.max_rows', 10)
pd.set_option('display.max_columns', None)

df0 = pd.read_csv("https://raw.githubusercontent.com/PEESEgroup/PEESE-COVID19/master/ny%20cases%20by%20county.csv")
df_name = pd.read_csv(
    "https://raw.githubusercontent.com/nz225/ning-lib/master/Map_NYS/data_positive_test/data_0301.csv")
df0 = df0.fillna(0)
# print (df0.head())

pieces = {}
i = 1
for column in df0.columns[1:len(df0.columns)]:
    df_temp = pd.DataFrame()
    df_temp['fips'] = df_name['fips'].copy()
    df_temp['name'] = df_name['name'].copy()

    df_temp['infected_num'] = df0[column].copy()

    # NEW YORK CITY - replacing the value for its five counties
    for t in range(len(df_temp)):
        if "New York City" in df_temp.loc[t, 'name']:
            df_temp.loc[t, 'infected_num'] = df0.loc[df0['region'] == 'new york', column].iloc[0]

    temp_num = df_temp['infected_num'].copy().to_numpy().astype(int)
    temp_str = []
    for j in range(len(temp_num)): temp_str.append(str(format(temp_num[j], ',d')))
    df_temp['infected'] = temp_str

    # Log scales
    df_temp['infected_log'] = df_temp['infected_num'].replace(0, np.nan)
    df_temp['infected_log'] = np.log10(df_temp['infected_log']) + 1
    df_temp = df_temp.fillna(0)

    # New cases (increase)
    if i == 1:
        df_temp['increase_num'] = df_temp['infected_num']
    else:
        df_temp['increase_num'] = df_temp['infected_num'] - previous_day

    temp_inc = df_temp['increase_num'].copy().to_numpy().astype(int)
    temp_str = []
    for k in range(len(temp_num)): temp_str.append(str(format(temp_inc[k], ',d')))
    df_temp['increase'] = temp_str

    # Increase rate
    if i == 1:
        df_temp['increase_rate'] = '0%'
    else:
        current_day = df_temp['infected_num'].to_numpy()
        rate_temp = np.divide(current_day - previous_day, previous_day)
        df_temp['increase_rate'] = rate_temp
        df_temp = df_temp.fillna(0)
        df_temp['increase_rate'] = df_temp['increase_rate'].astype(float).map(lambda n: '{:.0%}'.format(n))

    previous_day = df_temp['infected_num'].to_numpy()
    # print (previous_day, current_day)

    # generate dictionary
    # pieces["df_{}".format(i)] = df_temp.copy()
    key = datetime.datetime.strptime(column, '%m/%d/%Y').strftime('%b-%d')
    pieces[key] = df_temp.copy()
    i = i + 1

AllNames = []
df = pd.concat(pieces)
for key in pieces.keys():
    print (key, '\n', df.loc[key], '\n')
    AllNames.append(str(key))
DayNum = len(AllNames)

dailysum = []
totalsum = []
date = []
temp = 0
for key, lis in pieces.items():
    date.append(key)
    totalsum.append(sum(lis.infected_num) - (lis.infected_num[2] * 4))
    if temp == 0:
        dailysum.append(0)
    else:
        dailysum.append(totalsum[temp] - totalsum[temp - 1])
    temp = temp + 1


# max tick for axis
def roundup1(x):
    return int(math.ceil(x / 10000.0)) * 10000


def roundup2(x):
    return int(math.ceil(x / 1000.0)) * 1000

def find_range(x):
    ymax = 10
    if x == 0:       ymax = 10
    elif x < 100:    ymax = int(math.ceil(x / 10.0)) * 10
    elif x < 1000:   ymax = int(math.ceil(x / 100.0)) * 100
    elif x < 10000:  ymax = int(math.ceil(x / 1000.0)) * 1000
    else:            ymax = int(math.ceil(x / 10000.0)) * 10000
    return ymax

def gen_ticks(x):
    tick_vals = np.linspace(0,find_range(x),5)
    tick_text = []
    for j in tick_vals: tick_text.append(str(format(j.astype(int), ',d')))
    return tick_vals,tick_text

def log_ticks(x):
    tick_vals = [0]
    tick_text = ['0']
    flag = 0
    i = 0
    while flag == 0:
        temp = 10**i
        tick_vals.append(i+1)
        tick_text.append(str(format(temp, ',d')))
        if x < 10**i: flag = 1
        i = i+1
    return tick_vals,tick_text



dailymax = np.amax(dailysum)
totalmax = np.amax(totalsum)
ymax_daily = roundup2(dailymax)
ymax_total = roundup1(totalmax)
# barmax   = df['infected_log'].max()
# xmax_bar    = roundup2(barmax)
df_top = pd.DataFrame()  # used for the column chart

# ========== Yanqiu ==========
# ========== Yanqiu ==========

df_yt = pd.read_csv("https://raw.githubusercontent.com/PEESEgroup/PEESE-COVID19/master/ny%20cases%20by%20county.csv")
df_yt = df_yt.fillna(0)
df_yt.columns.values[1:] = AllNames
df_yt.iloc[2, 1:DayNum + 1] = df_yt.iloc[30, 1:DayNum + 1].copy()
df_yt.iloc[23, 1:DayNum + 1] = df_yt.iloc[30, 1:DayNum + 1].copy()
df_yt.iloc[40, 1:DayNum + 1] = df_yt.iloc[30, 1:DayNum + 1].copy()
df_yt.iloc[42, 1:DayNum + 1] = df_yt.iloc[30, 1:DayNum + 1].copy()
print(df_yt.columns.values)

df_log = df_yt.copy()
df_log = df_log.drop(columns=['region'])
df_yt = df_yt.drop(columns=['region'])
df_log = df_log.replace(0, np.nan)
df_log = np.log10(df_log) + 1
df_log = df_log.fillna(0)
df_yt['fips'] = df_name['fips'].copy()
df_log['fips'] = df_name['fips'].copy()
df_yt['name'] = df_name['name'].copy()
df_log['name'] = df_name['name'].copy()
print(df_log.head())
print(df_yt.head())

dailydf = df_yt.copy()
dailydf.iloc[:, 0:DayNum] = df_yt.iloc[:, 0:DayNum].diff(axis=1).fillna(0)
print(dailydf.head())

# ==================  Figure  ===================
# ==================  Figure  ===================

# Legend values
temp_zero = np.array([0])
temp_log = np.log10(np.logspace(0, 4, num=5)) + 1
temp_log_2 = np.log10(np.logspace(0, 5, num=6)) + 1
legend_vals = np.concatenate([temp_zero, temp_log])
legend_text = np.array([0, 1, 10, 100, '1,000', '>10,000'])
tick_vals_bar = np.concatenate([temp_zero, temp_log_2])
tick_text_bar = np.array([0, 1, 10, 100, '1,000', '10,000', '100,000'])

# Define Frames
frames_dict = []
for i, key in enumerate(pieces.keys()):
    my_text = ['Confirmed: ' + '<b>{}</b><br>'.format(con) +
               'New: ' + '<b>{}</b><br>'.format(inc) +
               'Increase: ' + '<b>{}</b><br>'.format(rate)
               for con, inc, rate in zip(list(df.loc[key]['infected']),
                                         list(df.loc[key]['increase']),
                                         list(df.loc[key]['increase_rate']))]
    frame_trace_1 = dict(
        type='choroplethmapbox',
        geojson=counties,
        featureidkey="properties.fips",
        locations=df.loc[key]['fips'],
        z=df.loc[key]['infected_log'],
        text=my_text,
        name=key,
        zmin=0,
        zmax=5,
        hovertext=df.loc[key]['name'],
        hoverinfo='text',
        hovertemplate='<b>%{hovertext}</b><br>' + \
                      '%{text}',
        colorscale='Blues',
        marker_line_width=0.5,
        marker_line_color='rgb(169,164,159)',
        colorbar={'tickmode': 'array',
                  'tickvals': legend_vals,
                  'ticktext': legend_text,
                  'x': 0.95,
                  'y': 0.715,
                  'len': 0.53,
                  },
    )

    # use xsrc later !!!!!!!!!
    frame_trace_2 = dict(
        type='scatter',
        x=date[0:i + 1],
        y=dailysum[0:i + 1],
        mode='lines+markers',
        marker=dict(
            size=10,
            color=dailysum,
            colorscale="Peach",
            showscale=False,
        ),
        name='',
        line=dict(color='#fb6a4a', width=1, shape='linear', smoothing=1.2),
        text=dailysum[0:i + 1],
        hovertext=date[0:i + 1],
        hoverinfo='text',
        hovertemplate='New cases' + \
                      '<br>on %{hovertext}: <b>%{text}</b><br>',
        xaxis="x1",
        yaxis="y1",
        showlegend=False,
    )

    frame_trace_3 = dict(
        type='scatter',
        x=date[0:i + 1],
        y=totalsum[0:i + 1],
        mode='lines+markers',
        fill='tozeroy',
        fillcolor='#c7e9c0',
        marker=dict(
            size=10,
            color=totalsum,
            colorscale="algae",
            showscale=False,
        ),
        name='',
        line=dict(color='#41ab5d', width=1, shape='linear', smoothing=1.2),
        text=totalsum[0:i + 1],
        hovertext=date[0:i + 1],
        hoverinfo='text',
        hovertemplate='Total cases' + \
                      '<br>on %{hovertext}: <b>%{text}</b><br>',
        xaxis="x2",
        yaxis="y2",
        showlegend=False,
    )

    df_top = df.loc[key]
    df_top = df_top.drop([23, 30, 40, 42], axis=0)
    # df_top = df_top.sort_values(by='infected_log', ascending=True).tail(20)

    frame_trace_4 = dict(
        type='bar',
        x=df_top['infected_log'],
        y=df_top['name'],
        orientation='h',
        name=key,
        text=df_top['infected'],
        hovertext=df_top['name'],
        hoverinfo='text',
        hovertemplate='Confirmed cases' + \
                      '<br>in %{hovertext}: <b>%{text}</b><br>',
        marker=dict(
            # color='#80b1d3'
            # colorscale='Blues',
            color=df_top['infected_log'],
            colorscale="Purp",
            cmin=0,
            cmid=5,
            cmax=6,
            showscale=False,
        ),
        xaxis="x3",
        yaxis="y3",
        showlegend=False,
    )

    frame = dict(
        data=[frame_trace_1, frame_trace_2, frame_trace_3, frame_trace_4],
        name=str(key),
        traces=[0, 1, 2, 3],
    )

    frames_dict.append(frame)

fig5 = go.Figure(frames=frames_dict)

# Define Data : add data to be displayed before animation starts
last_key = list(pieces.keys())[-1]  # get the last key (date)

# customized hover text
increase = df.loc[last_key]['increase']
# my_text = ['(test: '+'{}'.format(inc)+')' for inc in list(df.loc[last_key]['increase'])]
my_text = ['Confirmed: ' + '<b>{}</b><br>'.format(con) +
           'New: ' + '<b>{}</b><br>'.format(inc) +
           'Increase: ' + '<b>{}</b><br>'.format(rate)
           for con, inc, rate in zip(list(df.loc[last_key]['infected']),
                                     list(df.loc[last_key]['increase']),
                                     list(df.loc[last_key]['increase_rate']))]

data_trace_1 = dict(
    type='choroplethmapbox',
    geojson=counties,
    featureidkey="properties.fips",
    locations=df.loc[last_key]['fips'],
    z=df.loc[last_key]['infected_log'],
    text=my_text,
    name=key, zmin=0, zmax=5,
    hovertext=df.loc[last_key]['name'], hoverinfo='text',
    hovertemplate='<b>%{hovertext}</b><br>' + \
                  '%{text}',
    colorscale='Blues',
    marker_line_width=0.5,
    marker_line_color='rgb(169,164,159)',
    colorbar={'tickmode': 'array',
              'tickvals': legend_vals,
              'ticktext': legend_text,
              'x': 0.95,
              'y': 0.715,
              'len': 0.53,
              },
)

data_trace_2 = dict(
    type='scatter',
    x=date,
    y=dailysum,
    mode='lines+markers',
    marker=dict(
        size=10,
        color=dailysum,
        colorscale="Peach",
        showscale=False,
    ),
    name='',
    line=dict(color='#fb6a4a', width=1, shape='linear', smoothing=1.2),
    text=dailysum,
    hovertext=date,
    hoverinfo='text',
    hovertemplate='New cases' + \
                  '<br>on %{hovertext}: <b>%{text}</b><br>',
    xaxis="x1",
    yaxis="y1",
    # title = 'Total Confirmed Cases',
    showlegend=False,
)

data_trace_3 = dict(
    type='scatter',
    x=date,
    y=totalsum,
    mode='lines+markers',
    fill='tozeroy',
    fillcolor='#c7e9c0',
    marker=dict(
        size=10,
        color=totalsum,
        colorscale="algae",
        showscale=False,
    ),
    name='',
    line=dict(color='#41ab5d', width=1, shape='linear', smoothing=1.2),
    text=totalsum,
    hovertext=date,
    hoverinfo='text',
    hovertemplate='Total cases' + \
                  '<br>on %{hovertext}: <b>%{text}</b><br>',
    xaxis="x2",
    yaxis="y2",
    showlegend=False,
)

data_trace_4 = dict(
    type='bar',
    x=df_top['infected_log'],
    y=df_top['name'],
    orientation='h',
    name=key,
    text=df_top['infected'],
    hovertext=df_top['name'],
    hoverinfo='text',
    hovertemplate='Confirmed cases' + \
                  '<br>in %{hovertext}: <b>%{text}</b><br>',
    marker=dict(
        # color='#80b1d3'
        color=df_top['infected_log'],
        colorscale="Purp",
        cmin=0,
        cmid=5,
        cmax=6,
        showscale=False,
    ),
    xaxis="x3",
    yaxis="y3",
    showlegend=False,
)

data_dict = [data_trace_1, data_trace_2, data_trace_3, data_trace_4]


# Sliders and buttons
def frame_args(duration):
    return {
        "frame": {"duration": duration},
        "mode": "immediate",
        "fromcurrent": True,
        "transition": {"duration": duration, "easing": "linear"},
    }


steps_dict = [
    {
        "args": [[f.name], frame_args(0)],
        "label": str(f.name),
        "method": "animate",
    }
    for k, f in enumerate(fig5.frames)
]

sliders_dict = [dict(
    active=len(fig5.frames) - 1,
    # currentvalue={"prefix": "Date: "},
    currentvalue={"visible": False},
    # pad={"t": len(fig5.frames)},
    pad={"t": 0},
    x=0.15,
    len=0.7,
    y=1.05,
    steps=steps_dict
)]

updatemenus_dict = [
    {
        "buttons": [
            {
                "args": [None, frame_args(300)],  # speed of playing
                "label": "&#9654;",  # play symbol
                "method": "animate",
            },
            {
                "args": [[None], frame_args(0)],
                "label": "&#9724;",  # pause symbol
                "method": "animate",
            },
        ],
        "direction": "left",
        "pad": {"r": 10, "t": 0},
        "type": "buttons",
        "x": 0.1,
        "y": 1.05,
    }
]

# Define Layout
layout_dict = dict(
    # width  = 1000,
    height=950,
    # autosize = True,

    # MAPBOX
    mapbox=dict(
        # style   = "carto-positron",
        accesstoken='pk.eyJ1Ijoiemhhb24xNCIsImEiOiJjazg0cXppYzcxaWVxM2VvY2V0bG1ubzgzIn0.ZmGHEZLr-SFwNXywaO57tw',
        style="light",
        # style = "dark",
        center=dict(
            lon=-75.75,
            lat=42.8,
        ),
        zoom=5.5,
        domain=dict(
            x=[0, 0.95],
            y=[0.46, 0.97],
            # x = [0, 0.7],
            # y = [0.29, 1],
        ),
        # layers  = dict(below='')
    ),

    # GEO PLOTS. ?????

    # AXIS -- see current bug !!!!!!!! (reverse y axis)
    xaxis=dict(
        range=[0, len(date) - 1],
        showgrid=False,
        domain=[0, 0.48],
        anchor="y1",
        title="Daily New Cases",
        nticks=round(len(date) / 9),
    ),
    yaxis=dict(
        range=[0, ymax_daily],
        showgrid=False,
        domain=[0.27, 0.44],
        anchor="x1",
    ),
    xaxis2=dict(
        range=[0, len(date) - 1],
        showgrid=False,
        domain=[0.52, 1],
        anchor="y2",
        title="Total Confirmed Cases",
        nticks=round(len(date) / 9),
    ),
    yaxis2=dict(
        range=[0, ymax_total],
        showgrid=False,
        domain=[0.27, 0.44],
        anchor="x2",
    ),
    xaxis3=dict(
        range=[0, 6],
        tickmode='array',
        tickvals=tick_vals_bar,
        ticktext=tick_text_bar,
        showgrid=False,
        domain=[0, 1],
        anchor="y3",
        title="",
    ),
    yaxis3=dict(
        range = [len(df_top)-10.5,len(df_top)],
        domain=[0.00, 0.20],
        anchor="x3",
        categoryorder = 'total ascending',
        # autorange='reversed'
    ),

    # dragmode=False, # should put this to "config" instead of "layout"
    # title={'text':'Coronavirus (COVID-19) in New York State <a href="https://peese.org">[PEESE @Cornell]</a>','xref':'paper','x':0.5,'y':0.98},
    margin={"r": 10, "t": 0, "l": 100, "b": 10},
    updatemenus=updatemenus_dict,
    sliders=sliders_dict,
    plot_bgcolor='#fcfbfd',
)

# Creating figures
fig = go.Figure(data=data_dict, frames=frames_dict, layout=layout_dict)

###################################################################################
###################################################################################
colors = {
    'blue': '#015680'
}

app.layout = html.Div(children=[
    html.Br(),

    html.Div(children=[
        html.Div([
            html.A(
                html.Img(
                    src=app.get_asset_url('peese.JPG'),
                    id="peese-image",
                    style={
                        "height": "100px",
                        "width": "auto",
                        "margin-bottom": "0px",
                        "margin-left": "50px",
                        "float": "left"
                    }
                ),
                href="https://www.peese.org",
            )
        ],  # className="one-fourth column"
        ),

        html.Div([
            html.Img(
                src=app.get_asset_url('cornell.png'),
                id="cornell-image",
                style={
                    "height": "100px",
                    "width": "auto",
                    "margin-bottom": "0px",
                    "margin-right": "50px",
                    "float": "right"
                }
            )
        ],  # className="row flex-display",
        ),

        html.Div([
            html.H1(
                children='COVID-19 in New York State',
                style={
                    'textAlign': 'center',
                    'color': colors['blue'],
                    'font-size': 56,
                    'font-family': "Palatino Linotype",
                    "margin-top": "0px",

                }
            ),
            html.H1(
                children='Interactive Map by PEESE @ Cornell Univerisity',
                style={
                    'textAlign': 'center',
                    'color': colors['blue'],
                    'font-size': 32,
                    'font-family': "Palatino Linotype",
                    "margin-top": "0px",

                }
            ),

        ],  # className="row flex-display",
        ),

    ]),

    html.Hr(),
    # html.Br(),

    ### 1st graph ###
    html.Div([
        dcc.Graph(
            id='county-choropleth',
            figure=fig,
            config={
                'displayModeBar': False
                }
        )
    ],
        # className='six columns',
        className='one-half column',
        style={
            'margin': 0,
            # 'width':'40%',
            # 'width': '1000px',
            'dispay': 'flex',
            'flex-direction': 'column',
            'width': '50%',
            # 'height':'70%',
            # 'background-color': '#C4CDD5',
            'float': 'left',
            'min-width': '800px',
        }
    ),

    html.Div([
        html.H3(
            children='County-level Statistics',
            style={
                'textAlign': 'center',
                'color': colors['blue'],
                # 'font-size': ,
                'font-family': "Palatino Linotype",
                # "margin-top": "20px",
                # 'width':'100%',
                'margin': 0
            }
        ),

        # html.P('', style={'textAlign': 'center'}),
        # dcc.Dropdown(
        #  options=[{'label': 'Scatter plot of daily new cases in NYS',
        #        'value': 'daily_new_cases'},
        #       {'label': 'Area plot of total confirmed cases in NYS',
        #        'value': 'total_confirmed_cases'}],
        #  value='daily new cases',
        #  id='chart-dropdown'
        # ),

        # html.Br(),

        dcc.Checklist(
            options=[{'label': 'Log scale', 'value': 'log'}],
            value=[],
            labelStyle={'display': 'inline-block'},
            id='log-scale',
            style={'textAlign': 'center'}
            # style={'position': 'absolute', 'right': 80, 'top': 10}
        ),
        # html.Br(),

        ### 2nd graph ###
        html.Div([

            dcc.Graph(
                id='selected-data',
                figure=dict(
                    data=[dict(x=0, y=0)],
                    layout=dict(
                        paper_bgcolor='#F4F4F8',
                        plot_bgcolor='#F4F4F8',
                        autosize=True,
                        # width='100%',
                        # height='100%',
                        margin={"r": 100, "t": 0, "l": 10, "b": 0},
                        # height=500
                    ),
                ),
                config={
                'displayModeBar': False
                }
                # animate = True
            ),
        ],
            style={
                'left': '50%',
                'width': '50%',
                'min-width': '800px',
            }
        ),

        ### 3rd graph ###
        html.Div([
            dcc.Graph(
                id='selected-data-2',
                figure=dict(
                    data=[dict(x=0, y=0)],
                    layout=dict(
                        paper_bgcolor='#F4F4F8',
                        plot_bgcolor='#F4F4F8',
                        autosize=True,
                        width='100%',
                        height='100%',
                        margin={"r": 50, "t": 0, "l": 10, "b": 0},
                        # height=500
                    ),
                ),
                config={
                'displayModeBar': False
                }
            ),
        ],
            style={
                'left': '50%',
                'width': '50%',
                'min-width': '800px',
            }
        ),
    ],

        # className='six columns',
        style={
            # 'margin': 0,
            'dispay': 'flex',
            'justify-content': 'space-between',
            # 'margin-bottom': '15px',
            "margin-top": "0px",
            'float': 'left',
            # "margin-right": "0px",
            'width': '50%',
            'height': '70%',
            'min-width': '800px',
            # 'background-color': '#082255',  # for debugging: showing the area
            # 'margin-left':'1000px'
        }
    ),

    html.Div([
        html.H3(
            children='Data Source: State, County and City Department of Health in New York State',
            style={
                'textAlign': 'left',
                'color': '#878787',
                'font-size': 18,
                'font-family': "Palatino Linotype",
                # "margin-top": "20px",
                'width': '100%',
            }
        ),
    ],  # className="one-half column",
        style={
            "margin-left": "100px",
            'width': '100%',
            'float': 'left',
            # 'position':'absolute',
        }
    ),

    html.Div([
        html.Hr(),
    ],
        style={
            'width': '100%',
            'float': 'left',
            'height': '30px',
        }),

    # Data source and acknowledgement
    html.Div([

        html.Div([
            html.A(
                html.Img(
                    src=app.get_asset_url('engage.JPG'),
                    id="Engaged_Cornell",
                    style={
                        "height": "80px",
                        "width": "auto",
                        "margin-bottom": "0px",
                        "margin-left": "50px",
                    }
                ),
                href="https://engaged.cornell.edu/",
            ),
        ],
            style={
                "float": "left",
                'margin-top': '30px',
            }
        ),

        html.Div([
            html.Img(
                src=app.get_asset_url('cacs.JPG'),
                id="atkinson-image",
                style={
                    "height": "29px",
                    "width": "auto",
                    "margin-bottom": "0px",
                    "margin-right": "50px",
                    "float": "right",
                    'margin-top': '30px',
                }
            ),
            # href="https://www.atkinson.cornell.edu/",
        ],
        ),

    ]),

    html.Script(['var sc_project=12231169;','var sc_invisible=1;','var sc_security="3feb63be";','var sc_https=1;'],type='text/javascript'),
    html.Script(src='https://www.statcounter.com/counter/counter.js',type='text/javascript'),

])



# app.scripts.append_script(html.Script(['var sc_project=12226718; ','var sc_invisible=1; ','var sc_security="2df363f3"; '],type='text/javascript'))


app.scripts.append_script({
    'external_url': write_to_data_uri("""
    var sc_project=12231169; 
    var sc_invisible=1; 
    var sc_security="3feb63be"; 
    var sc_https=1; 
    """)})

app.scripts.append_script({
    'external_url': 'https://www.statcounter.com/counter/counter.js'
    })



# ================== Callback =========================
# ================== Callback =========================

@app.callback(
    Output('selected-data', 'figure'),
    [Input('county-choropleth', 'clickData'),
	 Input('log-scale', 'value'),
	 # Input('chart-dropdown', 'value'),
	 # Input('days-slider', 'value')
	 ])
def display_selected_data(clickData, checklist_values):
    # print(chart_dropdown)
    print('FIRE SELECTION')

    temp_zero = np.array([0])

    def setrange(x):
        [legend_vals,legend_text]         = gen_ticks(x)
        [legend_vals_log,legend_text_log] = log_ticks(x)
        return legend_vals_log, legend_vals, legend_text_log, legend_text


    if clickData is None:
        print('SelectedData is None')
        FIPS = ['36109']
    else:
        print(clickData['points'])
        pts = clickData['points']
        FIPS = [str(pt['location']) for pt in pts]
        print('FIPS', '\n', FIPS)

    dff = df_yt[df_yt['fips'].isin(FIPS)]
    dff_log = df_log[df_log['fips'].isin(FIPS)]
    dailydff = dailydf[dailydf['fips'].isin(FIPS)]
    dailydff_log = dailydff.copy().drop(columns=['name', 'fips'])
    dailydff_log = dailydff_log.replace(0, np.nan)
    dailydff_log = np.log10(dailydff_log) + 1
    dailydff_log = dailydff_log.fillna(0)
    dailymax = dailydff.iloc[0, 0:DayNum].values.max()
    totalmax = dff.iloc[0, 0:DayNum].values.max()
    ymax_daily = dailymax
    ymax_total = totalmax
    dailymax_log = np.log10(dailymax) + 1
    totalmax_log = np.log10(totalmax) + 1

    index_total_log = len(setrange(ymax_total)[0]) - 1
    y_total_log = setrange(ymax_total)[0][index_total_log]
    index_total = len(setrange(ymax_total)[1]) - 1
    y_total = setrange(ymax_total)[1][index_total]

    index_daily_log = len(setrange(ymax_daily)[0]) - 1
    y_daily_log = setrange(ymax_daily)[0][index_daily_log]
    index_daily = len(setrange(ymax_daily)[1]) - 1
    y_daily = setrange(ymax_daily)[1][index_daily]

    title = 'Total confirmed cases for<b>{}</b> from {} to {}'.format(dff.name.to_string(index=False), AllNames[0],
                                                                      AllNames[DayNum - 1])
    data = go.Scatter(
        x=AllNames,
        # y=dff.iloc[0,0:DayNum],
        y=dff_log.iloc[0, 0:DayNum] if ('log' in checklist_values) else dff.iloc[0, 0:DayNum],
        mode='lines+markers',
        fill='tozeroy',
        fillcolor='#c7e9c0',
        marker=dict(
            size=10,
            color=dff_log.iloc[0, 0:DayNum] if ('log' in checklist_values) else dff.iloc[0, 0:DayNum],
            colorscale="algae",
            showscale=False
        ),
        name='',
        line=dict(color='#41ab5d', width=1, shape='linear', smoothing=1.2),
        text=dff.iloc[0, 0:DayNum],
        hovertext=AllNames,
        hoverinfo='text',
        hovertemplate='Total cases' + \
                      '<br>on %{hovertext}: <b>%{text}</b><br>',
        xaxis="x2",
        yaxis="y2",
        showlegend=False
    )

    layout = dict(
        xaxis2=dict(
            range=[0, len(AllNames) - 1],
            showgrid=False,
            # domain=[0, 1],
            anchor="y2",
            # title="Total Confirmed Cases",
            nticks=round(len(AllNames) / 4)
        ),
        yaxis2=dict(
            # range=[0, y_total],
            range=[0, y_total_log] if ('log' in checklist_values) else [0, y_total],
            showgrid=False,
            # domain=[0.27, 0.44],
            anchor="x2",
            tickmode='array',
            tickvals=setrange(ymax_total)[0] if ('log' in checklist_values) else setrange(ymax_total)[1],
            ticktext=setrange(ymax_total)[2] if ('log' in checklist_values) else setrange(ymax_total)[3]
        ),
        plot_bgcolor='#fcfbfd',
        title=title,
        autosize=True,
        # width='100%',
        # height='100%',
        margin={"r": 0, "t": 50, "l": 100, "b": 20},
    )
    return {"data": [data],
            "layout": layout}


## 3rd graph

@app.callback(
    Output('selected-data-2', 'figure'),
    [Input('county-choropleth', 'clickData'),
	 Input('log-scale', 'value'),
	 # Input('chart-dropdown', 'value'),
	 # Input('days-slider', 'value')
	 ])
def display_selected_data(clickData, checklist_values):
    # print(chart_dropdown)
    print('FIRE SELECTION')

    temp_zero = np.array([0])

    def setrange(x):
        [legend_vals,legend_text]         = gen_ticks(x)
        [legend_vals_log,legend_text_log] = log_ticks(x)
        return legend_vals_log, legend_vals, legend_text_log, legend_text

    if clickData is None:
        print('SelectedData is None')
        FIPS = ['36109']
    else:
        print(clickData['points'])
        pts = clickData['points']
        FIPS = [str(pt['location']) for pt in pts]
        print('FIPS', '\n', FIPS)

    dff = df_yt[df_yt['fips'].isin(FIPS)]
    dff_log = df_log[df_log['fips'].isin(FIPS)]
    dailydff = dailydf[dailydf['fips'].isin(FIPS)]
    dailydff_log = dailydff.copy().drop(columns=['name', 'fips'])
    dailydff_log = dailydff_log.replace(0, np.nan)
    dailydff_log = np.log10(dailydff_log) + 1
    dailydff_log = dailydff_log.fillna(0)
    dailymax = dailydff.iloc[0, 0:DayNum].values.max()
    totalmax = dff.iloc[0, 0:DayNum].values.max()
    ymax_daily = dailymax
    ymax_total = totalmax

    index_total_log = len(setrange(ymax_total)[0]) - 1
    y_total_log = setrange(ymax_total)[0][index_total_log]
    index_total = len(setrange(ymax_total)[1]) - 1
    y_total = setrange(ymax_total)[1][index_total]

    index_daily_log = len(setrange(ymax_daily)[0]) - 1
    y_daily_log = setrange(ymax_daily)[0][index_daily_log]
    index_daily = len(setrange(ymax_daily)[1]) - 1
    y_daily = setrange(ymax_daily)[1][index_daily]

    return dict(
        data=[dict(
            type='bar',
            x=AllNames,
            y=dailydff_log.iloc[0, 0:DayNum] if ('log' in checklist_values) else dailydff.iloc[0, 0:DayNum],
            marker=dict(
                # color='#80b1d3'
                color=dailydff_log.iloc[0, 0:DayNum] if ('log' in checklist_values) else dailydff.iloc[0, 0:DayNum],
                colorscale="Peach",
                showscale=False,
                ),
            name='',
            text=dailydff.iloc[0, 0:DayNum],
            hovertext=AllNames,
            hoverinfo='text',
            hovertemplate='New cases' + \
                          '<br>on %{hovertext}: <b>%{text}</b><br>',
            xaxis="x1",
            yaxis="y1",
            showlegend=False
        )],
        layout=dict(
            xaxis=dict(
                range=[0, len(AllNames)],
                showgrid=False,
                # domain=[0, 0.48],
                anchor="y1",
                # title="Daily New Cases",
                nticks=round(len(AllNames) / 4),
                # tickmode='array',
            ),
            yaxis=dict(
                range=[0, y_daily_log] if ('log' in checklist_values) else [0, y_daily],
                showgrid=False,
                # domain=[0.27, 0.44],
                anchor="x1",
                tickmode='array',
                tickvals=setrange(ymax_daily)[0] if ('log' in checklist_values) else setrange(ymax_daily)[1],
                ticktext=setrange(ymax_daily)[2] if ('log' in checklist_values) else setrange(ymax_daily)[3]
            ),
            plot_bgcolor='#fcfbfd',
            title = 'Daily new cases for<b>{}</b> from {} to {}'.format(dailydff.name.to_string(index=False), AllNames[0], AllNames[DayNum - 1]),
            autosize=True,
            # width='100%',
            # height='100%',
            margin={"r": 0, "t": 50, "l": 100, "b": 20},
        )
    )

    

# ================== Callback end =========================


if __name__ == '__main__':
    app.run_server(debug=True)












































