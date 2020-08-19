import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly
import logging
import numpy as np
from dash.dependencies import Input, Output
from statsmodels.tsa.seasonal import seasonal_decompose
import  AuxiliaryFunctions as AF
import plotly.express as px
import pandas as pd

Hourly,Monthly,Weekly,Business_Day = AF.clean_dataset()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options

colors = {'background': 'white', 'text': 'sienna'}

fig = go.Figure()


tab_1 = dcc.Tab(label='Analysis of Summary Statistics',value='tab_1',children=[
    html.Div(children='''
            Choose the Statistics
        '''),
    dcc.Dropdown(
        id = "statistics_drop_down",
        options=[{
            'label':'minimum', 'value':'minimum'},
            {'label':'maximum', 'value':'maximum'},
            {'label':'sums', 'value':'sums'},
            {'label': 'median','value': 'median'},
            {'label':'mean','value':'mean'},
            {'label':'std','value':'std'}],
        value='minimum',
        multi=False
    ),
    html.Div(children='''
           Choose the resampler
       '''),
    dcc.Dropdown(
        id="resample_drop_down",
        options=[{
            'label': 'hourly', 'value': 'hourly'},
            {'label': 'Business days', 'value': 'Business_Day'},
            {'label': 'weekly', 'value': 'weekly'},
            {'label':'monthly','value':'monthly'}],
        value='hourly',
        multi=False
    )
    ,
    html.Div(children='''
          Choose Year
      '''),
    dcc.Dropdown(

        id="Years",
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': '2016','value':'2016'},
            {'label': '2017', 'value':'2017'},
            {'label':'2018', 'value': '2018'}
        ],
        value='all',
        multi=False
    )
   ]

    )

tab_2 = dcc.Tab(label='Analysis of Detrended Data',value='tab_2',children=[

    html.Div(children='''
          Choose the resampler
      '''),
    dcc.Dropdown(
        id="resample_drop_down_dec",
        options=[{
            'label': 'hourly', 'value': 'hourly'},
            {'label': 'Business days', 'value': 'Business_Day'},
            {'label': 'weekly', 'value': 'weekly'},
            {'label': 'monthly', 'value': 'monthly'}],
        value='hourly',
        multi=False
    ),

    html.Div(children='''
                Choose the Statistics
            '''),
    dcc.Dropdown(
        id = "statistics_drop_down_dec",
        options=[
            {'label':'maximum', 'value':'max'},
            {'label': 'median','value': 'median'},
            {'label':'mean','value':'mean'},
            {'label':'std','value':'std'}],
        value='max',
        multi=False
    ),
    html.Div(children='''
         Choose Year
     '''),
    dcc.Dropdown(

        id="Years_dec",
        options=[
            {'label': 'All', 'value': 'all'},
            {'label': '2016', 'value': '2016'},
            {'label': '2017', 'value': '2017'},
            {'label': '2018', 'value': '2018'}
        ],
        value='2017',
        multi=False
    ),
    html.Div(children='''
             Choose Type of Decomposition
         '''),

    dcc.Dropdown(
        id="decomposition",
        options=[
            {'label': 'Additive', 'value': 'additive'},
            {'label': 'Multiplicative', 'value': 'multiplicative'}
        ],
        value='additive',
        multi=False
    )

    ])


app.layout = html.Div(children=[
    html.H1(children='Exploratory Analysis of Data'),
    dcc.Tabs(id = 'my_tabs',value='tab_1',children=[tab_1,tab_2]),

    dcc.Graph(
        id='presentation',
        figure=fig
    )
])

@app.callback(
    Output('presentation','figure'),
    [Input('my_tabs','value'),
     Input("statistics_drop_down",'value'),
     Input("resample_drop_down",'value'),
     Input("Years","value"),

     Input("statistics_drop_down_dec",'value'),
     Input("resample_drop_down_dec",'value'),
     Input("Years_dec","value"),
     Input("decomposition", "value")
     ]
)
def update_figure(tab,statistics,resampler,years,stat_dec,sample_dec,years_dec,decomp):


    val=dict(minimum = [True,False,False,False,False,False],
             maximum = [False,True,False,False,False,False],
             sums =    [False,False,True,False,False,False],
             median =  [False,False,False,True,False,False],
             mean =    [False,False,False,False,True,False],
             std =     [False,False,False,False,False,True]
             )

    traces = []
    if tab == "tab_1":

        datas = AF.what(years,resampler,Hourly,Weekly,Monthly,Business_Day)

        traces.append(go.Scatter(
            x=datas.index,
            y=datas['min'],
            line=dict(color='blue', width=1),
            opacity=0.8,
            name='minimum',
            visible=False
        ))

        traces.append(
            go.Scatter(
                x=datas.index,
                y=datas['max'],
                line=dict(color='red', width=1),
                opacity=0.8,
                name='maximum',
                visible=False
            )
        )

        traces.append(
            go.Scatter(
                x=datas.index,
                y=datas['sum'],
                line=dict(color='orange', width=1),
                opacity=0.8,
                name='sum',
                visible=False
            )
        )

        traces.append(
            go.Scatter(
                x=datas.index,
                y=datas['median'],
                line=dict(color='purple', width=1),
                opacity=0.8,
                name='median',
                visible=False
            )
        )

        traces.append(
            go.Scatter(
                x=datas.index,
                y=datas['mean'],
                line=dict(color='aqua', width=1),
                opacity=0.8,
                name='mean',
                visible=False
            )
        )

        traces.append(
            go.Scatter(
                x=datas.index,
                y=datas['std'],
                line=dict(color='darkolivegreen', width=1),
                opacity=0.8,
                name='std',
                visible=False
            )
        )



        layout = go.Layout(showlegend=True,
                           plot_bgcolor=colors['background'],
                           paper_bgcolor=colors['background'],
                           font={'color': colors['text']},
                           title=resampler + " Analysis",
                           hovermode="x unified",
                           updatemenus=[
                               dict(
                                   type="buttons",
                                   direction="right",
                                   active=0,
                                   x=0.2,
                                   y=1.9,
                                   buttons=list([
                                       dict(label="Plot Now-->Always click on after statistics)",
                                            method="update",
                                            args=[{
                                                "visible": val[statistics]}
                                            ]
                                            )

                                   ]

                                   )

                               )

                           ],
                           xaxis=dict(title="Date",
                                      rangeslider=dict(
                                          visible=True
                                      ),
                                      type="date"
                                      ),
                           yaxis=dict(title="KWh")
                           )
        return dict(data=traces, layout=layout)

    elif tab == "tab_2":

        datas = AF.what(years_dec, sample_dec, Hourly, Weekly, Monthly, Business_Day)
        logging.warning("data: {}".format(datas.head()))
        datas[stat_dec].fillna(method='ffill',inplace=True)

        assert  np.all(np.isfinite(datas[stat_dec])) == True

        assert  np.all(datas[stat_dec] >= 0 ) == True

        assert np.all(np.isnan(datas[stat_dec])) == False

        logging.warning("stat{}".format(datas[stat_dec].head()))

        print(decomp)

        result_fin1 = seasonal_decompose(datas[stat_dec],
                                    model='additive',
                                    extrapolate_trend='freq')

        result_fin2 = seasonal_decompose(datas[stat_dec],
                                         model='multiplicative',
                                         extrapolate_trend='freq')


        value = dict(additive = result_fin1,
                     multiplicative=result_fin2)

        result_fin = value[decomp]


        logging.warning("observed".format(result_fin.observed))

        fig = plotly.subplots.make_subplots(rows=4,cols=1)

        fig.add_trace(go.Scatter(x=result_fin.observed.index,y=result_fin.observed,mode='lines',name="Observed",
                                         opacity=0.9),1,1)
        fig.add_trace(go.Scatter(x=result_fin.seasonal.index,y= result_fin.seasonal, mode='lines',name="seasonal",
                                         opacity=0.9),2,1)
        fig.add_trace(go.Scatter(x=result_fin.trend.index,y=result_fin.trend, mode='lines',name="trend",
                                         opacity=0.9),3,1)
        fig.add_trace(go.Scatter(x=result_fin.resid.index,y=result_fin.resid, mode='lines',name="residual",
                                         opacity=0.9,),4,1)
        fig.update_layout(height=800, width=1200)

        return fig


if __name__ == '__main__':
    app.run_server(debug=True)