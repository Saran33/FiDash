import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from dtools import start_date, end_date, str_start, str_end, wdr_ticker, wdr_multi_ticker, indexed_vals
from d_charts import quant_chart, single_line_chart, pwe_line_chart
from sqlalch import all_tickers
from ntwrkx import plot_mst

labels, symbols = all_tickers()

# Define Dash App — https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],  # LUX, BOOTSTRAP
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]  # meta tags for mobile view
                )


# Dash Layout — https://hackerthemes.com/bootstrap-cheatsheet/
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("PWE Markets Dashboard",
                        className='text-center text-primary mb-4 header-1'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            dcc.Dropdown(id='sec-drpdwn', multi=False, value=None,
                         options=[{'label': x, 'value': y}
                                  for x, y in zip(labels, symbols)], searchable=True, placeholder='Select security...',
                         persistence=True, persistence_type='session', # persistence_type= session, memory
                         ),
            dcc.Graph(id='line-fig', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                                                        # 'modeBarButtonsToRemove': ['pan2d','select2d'], modeBarButtonsToAdd
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False})
        ],  # width={'size':5, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Dropdown(id='sec-drpdwn2', multi=True, value=[],
                         options=[{'label': x, 'value': x}
                                  for x in symbols], placeholder='Select security...',
                         persistence=True, persistence_type='session',
                         ),
            dcc.Graph(id='line-fig2', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], className="g-3", justify='center'),  # justify: start_date,center,end_date,between,around

    dbc.Row([
        dbc.Col([
            html.P("Select Security:",
                   style={"textDecoration": "underline"}),
            dcc.Checklist(id='my-checklist', value=['FB', 'GOOGL', 'AMZN'],
                          options=[{'label': x, 'value': x}
                                   for x in symbols[:3]],
                          className="sel-sec-cb", labelClassName="mb-3"),
            # spacing class: mr-3, mt-3, mb-3 # labelStyle={"display": "inline-block"}
            dcc.Graph(id='my-hist', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Graph(id='corr-mst', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], align="center", justify='center')  # Vertical: start_date, center, end_date

], fluid=True)


# Callback section: connecting the components
# --------------------------------------------
# Line chart - Single
@app.callback(
    Output('line-fig', 'figure'),
    Input('sec-drpdwn', 'value')
)

def update_graph(sltd_sec):
    if sltd_sec:
        if len(sltd_sec) > 0:
            df1 = wdr_ticker(sltd_sec, start_date, end_date, source='stooq')
            ticker = sltd_sec
            auto_start = df1.index.min()
            auto_end = df1.index.max()
            # plt_int = single_line_chart(df['Close'], start_date=start_date, end_date=end_date, kind='scatter',
            #                             title=f'{ticker} - {srt_start}:{srt_end}', ticker=ticker, yTitle='USD', showlegend=False,
            #                             theme='white', auto_start=srt_start, auto_end=None, connectgaps=False, annots=None, annot_col=None)

            plt_int = quant_chart(df1, start_date, end_date, ticker=ticker, title=f'{ticker}', theme='white', auto_start=auto_start, auto_end=auto_end,
                                asPlot=False, asFigure=True, showlegend=False, boll_std=2, boll_periods=20, showboll=False, showrsi=False,
                                rsi_periods=14, showama=False, ama_periods=9, showvol=True, show_range=False, annots=None, textangle=0,
                                file_tag=None, support=None, resist=None, annot_font_size=6, title_dates=False, title_time=False,
                                chart_ticker=True, top_margin=0.9, spacing=0.08, range_fontsize=9.8885, title_x=0.5,
                                title_y=0.933, arrowhead=6, arrowlen=-50)

            return plt_int

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Line chart - multiple
@app.callback(
    Output('line-fig2', 'figure'),
    Input('sec-drpdwn2', 'value')
)

def update_graph(sltd_sec):
    if sltd_sec:
        if len(sltd_sec) > 0:
            df2 = wdr_multi_ticker(sltd_sec, start_date, end_date,
                                source='stooq', price='Close')
            df2 = indexed_vals(df2)
            auto_start = df2.index.min()
            auto_end = df2.index.max()
            symbol = ''

            comp_lc1 = pwe_line_chart(df2, columns=sltd_sec, start_date=df2.index.min(), end_date=df2.index.max(),
                                    kind='scatter', title=f'{", ".join(map(str, sltd_sec))}', ticker=symbol,
                                    yTitle='Indexed Returns', asPlot=False, asFigure=True, showlegend=True,
                                    theme='white', auto_start=auto_start, auto_end=auto_end, connectgaps=False,
                                    file_tag=None, chart_ticker=False, annots=None)
            return comp_lc1

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate

# # Histogram
# @app.callback(
#     Output('my-hist', 'figure'),
#     Input('my-checklist', 'value')
# )
# def update_graph(sltd_sec):
#     dff = df[df['Symbols'].isin(sltd_sec)]
#     dff = dff[dff['Date'] == '2020-12-03']
#     fighist = px.histogram(dff, x='Symbols', y='Close')
#     return fighist



# Correlations Network - Minimum Spanning Tree
@app.callback(
    Output('corr-mst', 'figure'),
    Input('sec-drpdwn2', 'value')
)

def update_graph(sltd_sec):
    if sltd_sec:
        if len(sltd_sec) > 0:
            df4 = wdr_multi_ticker(sltd_sec, start_date, end_date,
                                source='stooq', price='Close')
            df4 = df4.pct_change().fillna(0).add(1).cumprod().mul(100)

            MST = plot_mst(df4, ann_factor=252, corr_threshold=0.05, node_size_factor=10, savefig=True)

            return MST

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate

if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
