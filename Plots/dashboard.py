# =============================================================================
# Dashboard file. 
# =============================================================================

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np
import plotly.graph_objs as go
import chart_studio
import plotly.express as px
import plotly.offline as offline
from plotly.graph_objs import *
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import pycountry
import dataframe_manip

#Unclear if this enhances the end result at all:
init_notebook_mode(connected=True)

app = dash.Dash()

#======= Chloropleth maps ======================================================
fig = px.choropleth(data_frame = dataframe_manip.merged_df1,
                     locations= "ISOCode",
                     color= "DeathsC",
                     hover_name= "CountryName",
                     color_continuous_scale= 'RdYlGn_r',
                     range_color =(0,11),
                     animation_frame= "Year")
fig.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)

fig2 = px.choropleth(data_frame = dataframe_manip.merged_df1,
                     locations= "ISOCode",
                     color= "AidC",
                     hover_name= "CountryName",
                     color_continuous_scale= 'RdYlGn')
fig2.update_layout(
    autosize=False,
    width=500,
    height=500,
    margin=dict(
        l=50,
        r=50,
        b=100,
        t=100,
        pad=4
    ),
    paper_bgcolor="LightSteelBlue",
)
#==============================================================================

#=======First line chart: one country, two lines================================
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=dataframe_manip.df_country1.index,
                         y=dataframe_manip.df_country1[dataframe_manip.df_country1.columns[0]],
                         visible=True)
             )
updatemenu = []
buttons = []
# button with one option for each dataframe
for col in dataframe_manip.df_country1.columns:
    buttons.append(dict(method='restyle',
                        label=col,
                        visible=True,
                        args=[{'y':[dataframe_manip.df_country1[col]],
                               'x':[dataframe_manip.df_country1.index],
                               'type':'scatter'}, [0]],
                        )
                  )
# some adjustments to the updatemenus
updatemenu = []
your_menu = dict()
updatemenu.append(your_menu)

updatemenu[0]['buttons'] = buttons
updatemenu[0]['direction'] = 'down'
updatemenu[0]['showactive'] = True

# add dropdown menus to the figure
fig1.update_layout(showlegend=False, updatemenus=updatemenu)
fig1.show()
#==============================================================================

#=======Second line chart: multi-country chart ================================


#====== Layout for dash =======================================================
app.layout = html.Div(children=[
    html.H1(children='Python Dash',
            style={
                'textAlign': 'center',
                'color': '#ef3e18'
            }
            ),
    html.Div('Welcome to the Group 5 dashboard! In this project we investigated what kind of correlation existed between development aid distributed by the World Bank and mortality rates for children between the ages of 1 and 4. This was accomplished through the use of choropleth maps, first to indicate yearly child mortality rates, then using line maps to chart the decline of child deaths over time.'),
    html.Div('Class: ITSC 3155-Y04', style={'textAlign': 'center'}),
    html.Div(''),    
    html.Div('Group members: Coleman Mack, Venkat Madduri, Michael Nakhle, Jamie Stephens'),
    html.Hr(style={'color': '#7FDBFF'}),
    html.H3('Child Mortality Map', style={'color': '#df1e56'}),
    html.Div('This chloropleth map shows national mortality rates over time.'),
    dcc.Graph(figure=fig),
    dcc.Graph(figure=fig2),
    html.H3('Line Graph', style={'color': '#df1e56'}),
    html.Div('Same data, with a dropdown. Select one country at a time.'),
    dcc.Graph(figure=fig1),
    html.H3('Line Graph, II', style={'color': '#df1e56'}),
    html.Div('Select multiple countries for a line graph in this space.'),
    html.H3('Notes', style={'color': '#df1e56'}),
    html.Div('Why do some countries report negative aid?', style={'color': '#df1e56'}),
    html.Div(html.P(['Aid and aid per capita data show the net value of official development assistance (ODA). Thus, if countries pay back more than they receive, they can show negative values of net aid. Please note that net aid does not include aid provided to other countries. For example, donor countries such as United States and Canada show ".." for aid per capita rather than negative values because they do not receive official aid. Donor aid provided is tracked separately and published in the World Development Indicators (WDI) online tables and database.', html.Br(), 
                     'Source: https://datahelpdesk.worldbank.org'],style={'textAlign': 'left','marginLeft': 100, 'marginRight': 300,'backgroundColor':'LightGrey'})),
    
    html.H3('Data Sources', style={'color': '#df1e56'}),
    html.Div(''),
    html.A("UNICEF: Number of deaths among children aged 1-4", href='https://data.unicef.org/wp-content/uploads/2020/09/Child-deaths-age-1-to-4_2020.xlsx', target="_blank"),
    html.Br(),
    html.A("World Bank: Net official development assistance and official aid received (current US$)", href='http://api.worldbank.org/v2/en/indicator/DT.ODA.OATL.CD?downloadformat=csv', target="_blank"),
    html.Br(),    
    html.A("United Nations: Total population, both sexes combined (thousands)", href='https://data.un.org/Data.aspx?d=PopDiv&f=variableID%3A12', target="_blank"),
    ])
#==============================================================================

if __name__ == '__main__':
      app.run_server()