import dash
# import dash_core_components as dcc
from dash import dcc
# import dash_html_components as html
from dash import html
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import dash_datetimepicker as dash_dt
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# start_date, end_date, str_start, str_end
from dtools import wdr_ticker, wdr_multi_ticker, indexed_vals, ext_str_lst
from d_charts import quant_chart, single_line_chart, pwe_line_chart, pwe_hist, calc_interval, pwe_return_dist_chart, pwe_box, pwe_heatmap
from pwe.analysis import Security
from pwe.pwetools import str_to_dt, to_utc
from sqlalch import all_tickers
from ntwrkx import plot_mst
from datetime import datetime, timedelta
import pytz

labels, symbols = all_tickers()

# Define Dash App — https://www.bootstrapcdn.com/bootswatch/
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP],  # LUX, BOOTSTRAP
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]  # meta tags for mobile view
                )

# alert = dbc.Alert(f"No data available for selected security", color="dark",  # {sltd_sec} dark danger
#                   dismissable=True, duration=6000),  # use dismissable or duration=5000 for alert to close in x milliseconds

# Dash Layout — https://hackerthemes.com/bootstrap-cheatsheet/
app.layout = dbc.Container([

    dbc.Row(
        dbc.Col(html.H1("PWE Markets Dashboard",
                        className='text-center text-primary mb-4 header-1'),
                width=12)
    ),

    dbc.Row([

        dbc.Col([
            html.Div(id="sec-alert", children=[]),
            dcc.Dropdown(id='sec-drpdwn', multi=False, value=None,
                         options=[{'label': x, 'value': y}
                                  for x, y in zip(labels, symbols)], searchable=True, placeholder='Select security...',
                         # persistence_type= session, memory
                         persistence=True, persistence_type='session',
                         ),
            dcc.Store(id='intermediate-value1'),
            # html.Div(
            #     [dash_dt.DashDatetimepicker(id="dt-picker-range", utc=True, locale="en-GB"), html.Div(id="output-dt-picker-range")]
            # ),
            dcc.DatePickerRange(
                id='dt-picker-range',  # ID for callback
                calendar_orientation='horizontal',  # vertical or horizontal
                day_size=39,  # Size of calendar image. Default is 39
                # text that appears when no end date chosen
                end_date_placeholder_text="End Date",
                with_portal=False,  # If True, calendar opens in a full screen overlay portal
                # Display of calendar when open (0 = Sunday)
                first_day_of_week=0,
                reopen_calendar_on_clear=True,
                # True or False for direction of calendar (right to left)
                is_RTL=False,
                clearable=True,  # Whether the calendar is clearable
                number_of_months_shown=1,  # Number of months displayed in dropdown
                min_date_allowed=datetime(1900, 1, 1),
                max_date_allowed=datetime.now().date(),
                initial_visible_month=datetime(
                    2021, 1, 1),  # Default visible month
                start_date=(datetime.utcnow() - timedelta(days=365)).date(),
                end_date=datetime.now().date(),
                display_format='D MMM YYYY',  # Do
                # How calendar headers are displayed on open.
                month_format='MMMM, YYYY',
                # Minimum allowable days between start and end.
                minimum_nights=1,
                # Whether the user's selected dates will be cached.
                persistence=True,
                persisted_props=['start_date'],  # What will be cached
                persistence_type='session',  # session, local, or memory. Default is 'local'
                updatemode='singledate'  # singledate or bothdates. Select when callback is triggered
            ),
            dcc.Graph(id='cand-fig', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                                                        # 'modeBarButtonsToRemove': ['pan2d','select2d'], modeBarButtonsToAdd
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False})
        ],  # width={'size':5, 'offset':1, 'order':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            html.Div(id="multi-sec-alert", children=[]),
            dcc.Dropdown(id='sec-drpdwn2', multi=True, value=[],
                         options=[{'label': x, 'value': x}
                                  for x in symbols], placeholder='Select security...',
                         persistence=True, persistence_type='session',
                         ),
            dcc.Store(id='intermediate-value2'),
            dcc.Graph(id='line-fig', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

    ], className="g-3", justify='center'),  # justify: start_date,center,end_date,between,around

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='sec-hist', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
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
    ], align="center", justify='center'),  # Vertical: start_date, center, end_date

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='real-vol', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Graph(id='box-plt', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], align="center", justify='center'),  # Vertical: start_date, center, end_date

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='yz-vol', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':1},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),

        dbc.Col([
            dcc.Graph(id='heatmap', figure={}, config={'scrollZoom': False, 'doubleClick': 'reset',
                      'showTips': True, 'displayModeBar': 'hover', 'watermark': False, 'displaylogo': False}),
        ],  # width={'size':5, 'offset':0, 'order':2},
            xs=12, sm=12, md=12, lg=5, xl=5
        ),
    ], align="center", justify='center'),  # Vertical: start_date, center, end_date

], fluid=True)


# Callbacks (connect components)
# --------------------------------------------
# Load single security dataframe
@app.callback(
    [Output('intermediate-value1', 'data'),
     Output("sec-alert", "children")],
    [Input('sec-drpdwn', 'value'),
     Input('dt-picker-range', 'start_date'),
     Input('dt-picker-range', 'end_date')]
)
def get_data1(sltd_sec, start_date, end_date):
    if sltd_sec:
        if len(sltd_sec) > 0:
            start_date = str_to_dt(start_date, dayfirst=False)
            if start_date.tzinfo == None:
                start_date = to_utc(start_date)
            if start_date:
                print("START DATE:", start_date)
            end_date = str_to_dt(end_date)
            if end_date.tzinfo == None:
                end_date = to_utc(end_date)
            if end_date:
                print("END DATE:", end_date)

            alert = dbc.Alert(f"No data available for {sltd_sec}", color="dark",  # dark danger
                              dismissable=True, duration=6000, class_name="sec-alert", fade=True)  # use dismissable or duration=5000 for alert to close in x milliseconds
            try:
                df1 = wdr_ticker(sltd_sec, start_date,
                                 end_date, source='stooq')
                if df1.empty:
                    return dash.no_update, alert
            except:
                print("Error reading data from API")
                return dash.no_update, alert
                # html.Div(f"No data available for {sltd_sec}")

            json1 = df1.to_json(date_format='iso', orient='split')

            return json1, dash.no_update

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate
        # return dash.no_update, alert


# Load multi-security dataframe
@app.callback(
    [Output('intermediate-value2', 'data'),
     Output("multi-sec-alert", "children")],
    [Input('sec-drpdwn2', 'value'),
     Input('dt-picker-range', 'start_date'),
     Input('dt-picker-range', 'end_date')]
)
def get_data2(sltd_sec, start_date, end_date):
    if sltd_sec:
        if len(sltd_sec) > 0:
            start_date = str_to_dt(start_date, dayfirst=False)
            if start_date.tzinfo == None:
                start_date = to_utc(start_date)
            if start_date:
                print("START DATE:", start_date)
            end_date = str_to_dt(end_date)
            if end_date.tzinfo == None:
                end_date = to_utc(end_date)
            if end_date:
                print("END DATE:", end_date)

            try:
                df2, missing_secs = wdr_multi_ticker(sltd_sec, start_date,
                                                     end_date, source='stooq', price='Close')
                print(missing_secs)
                alert = dbc.Alert(f"No data available for {ext_str_lst(missing_secs)}", color="dark",  # dark danger
                                  dismissable=True, duration=6000, class_name="sec-alert", fade=True)
                if df2.empty:
                    return dash.no_update, alert
                else:
                    json2 = df2.to_json(date_format='iso', orient='split')

                if missing_secs:
                    return json2, alert

            except:
                print("Error reading data from API")
                raise dash.exceptions.PreventUpdate

            return json2, dash.no_update

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Line chart - Single
@ app.callback(
    Output('cand-fig', 'figure'),
    [Input('sec-drpdwn', 'value'),
     Input('intermediate-value1', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json1):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json1 != None:
                df1 = pd.read_json(json1, orient='split')
                if not df1.empty:
                    # df1['DateTime'] = pd.to_datetime(df1['DateTime'])
                    ticker = sltd_sec
                    start_date = df1.index.min()
                    auto_start = start_date
                    end_date = df1.index.max()
                    auto_end = end_date
                    # plt_int = single_line_chart(df['Close'], start_date=start_date, end_date=end_date, kind='scatter',
                    #                             title=f'{ticker} - {srt_start}:{srt_end}', ticker=ticker, yTitle='USD', showlegend=False,
                    #                             theme='white', auto_start=srt_start, auto_end=None, connectgaps=False, annots=None, annot_col=None)

                    plt_int = quant_chart(df1, start_date, end_date, ticker=ticker, title=None, theme='white', auto_start=auto_start, auto_end=auto_end,
                                          asPlot=False, asFigure=True, showlegend=False, boll_std=2, boll_periods=20, showboll=False, showrsi=False,
                                          rsi_periods=14, showama=False, ama_periods=9, showvol=True, show_range=False, annots=None, textangle=0,
                                          file_tag=None, support=None, resist=None, annot_font_size=6, title_dates=False, title_time=False,
                                          chart_ticker=True, top_margin=0.9, spacing=0.08, range_fontsize=9.8885, title_x=0.5,
                                          title_y=0.933, arrowhead=6, arrowlen=-50)

                    return plt_int

                else:
                    raise dash.exceptions.PreventUpdate
            else:
                raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Line chart - multiple
@ app.callback(
    Output('line-fig', 'figure'),
    [Input('sec-drpdwn2', 'value'),
     Input('intermediate-value2', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json2):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json2 != None:
                df2 = pd.read_json(json2, orient='split')
                df2 = indexed_vals(df2)
                start_date = df2.index.min()
                auto_start = start_date
                end_date = df2.index.max()
                auto_end = end_date
                symbol = ''

                comp_lc1 = pwe_line_chart(df2, columns=sltd_sec, start_date=start_date, end_date=end_date,
                                        kind='scatter', title=f'{ext_str_lst(sltd_sec)}', ticker=symbol,
                                        yTitle='Indexed Returns', asPlot=False, asFigure=True, showlegend=True,
                                        theme='white', auto_start=auto_start, auto_end=auto_end, connectgaps=False,
                                        file_tag=None, chart_ticker=False, annots=None)
                return comp_lc1
            else:
                raise dash.exceptions.PreventUpdate
        else:
            raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Histogram
@ app.callback(
    Output('sec-hist', 'figure'),
    [Input('sec-drpdwn', 'value'),
     Input('intermediate-value1', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json1):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json1 != None:
                df3 = pd.read_json(json1, orient='split')
                if not df3.empty:
                    ticker = sltd_sec
                    df3.name = ticker
                    Sec = Security(df3)
                    Sec.get_returns(price='Close')
                    chart_interval, interval = calc_interval(Sec.df)
                    bins = int(Sec.df['Price_Returns'].count()/2)

                    hist = pwe_hist(Sec.df, tseries='Price_Returns', start_date=None, end_date=None, title='Returns',
                                    ticker=ticker, yTitle=None, xTitle=None, asPlot=False, asFigure=True, theme='white', showlegend=False,
                                    decimals=2, orientation='v', textangle=0, file_tag=None, interval=chart_interval,
                                    bins=bins, histnorm='probability', histfunc='count', yaxis_tickformat='', xaxis_tickformat='.2%')
                    return hist

                else:
                    raise dash.exceptions.PreventUpdate
            else:
                raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Correlations Network - Minimum Spanning Tree
@ app.callback(
    Output('corr-mst', 'figure'),
    [Input('sec-drpdwn2', 'value'),
     Input('intermediate-value2', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json2):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json2 != None:
                df4 = pd.read_json(json2, orient='split')
                df4 = df4.pct_change().fillna(0).add(1).cumprod().mul(100)

                MST = plot_mst(df4, ann_factor=252, corr_threshold=0.05,
                            node_size_factor=10, savefig=True)

                return MST
            else:
                raise dash.exceptions.PreventUpdate
        else:
            raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Realised Volatility
@ app.callback(
    Output('real-vol', 'figure'),
    [Input('sec-drpdwn', 'value'),
     Input('intermediate-value1', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json1):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json1 != None:
                df5 = pd.read_json(json1, orient='split')
                if not df5.empty:
                    ticker = sltd_sec
                    df5.name = ticker
                    Sec = Security(df5)
                    Sec.get_returns(price='Close')
                    chart_interval, interval = calc_interval(Sec.df)
                    vol_window = 30
                    trading_periods = 252
                    Sec.get_vol(window=vol_window, returns='Price_Returns',
                                trading_periods=trading_periods, interval=interval)
                    ann_factor, t, p = Sec.get_ann_factor(
                        interval, trading_periods, 24)
                    start_date = Sec.df.index[Sec.df[f'Ann_Vol_{vol_window}_{p}'] > 0][0]
                    auto_start = start_date
                    end_date = Sec.df.index.max()
                    auto_end = end_date

                    vol_fig = pwe_return_dist_chart(Sec.df, start_date, end_date, tseries=f'Ann_Vol_{vol_window}_{p}', kind='scatter',
                                                    title=f'Annualized {vol_window} {p} Volatility', ticker=f'{ticker} Vol.', yTitle=f'{ticker} Vol.',
                                                    asPlot=False, asFigure=True, showlegend=False, theme='white', auto_start=auto_start, auto_end=auto_end,
                                                    connectgaps=False, tickformat='.0%', decimals=2)
                    return vol_fig
                else:
                    raise dash.exceptions.PreventUpdate
            else:
                raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Multi-Asset Box Plot
@ app.callback(
    Output('box-plt', 'figure'),
    [Input('sec-drpdwn2', 'value'),
     Input('intermediate-value2', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json2):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json2 != None:
                df6 = pd.read_json(json2, orient='split')
                df6 = df6.pct_change()
                chart_interval, interval = calc_interval(df6)
                if interval in ['hourly', 'minutes', 'seconds']:
                    title_time = True
                else:
                    title_time = False
                if len(df6.columns) < 4:
                    ticker = ext_str_lst(df6.columns)
                    chart_ticker = True
                else:
                    ticker = ''
                    chart_ticker = False

                box_fig = pwe_box(df6, title=f'{chart_interval} Returns', ticker=ticker, yTitle='Returns (%)', xTitle='Returns Distribution', asPlot=True, theme='white',
                                showlegend=False, decimals=2, orientation='v', textangle=0, file_tag=None, chart_ticker=chart_ticker,
                                interval='Daily', yaxis_tickformat='.2%', xaxis_tickformat='.2%', linecolor=None, title_dates='Yes', title_time=title_time)

                return box_fig
            else:
                raise dash.exceptions.PreventUpdate
        else:
            raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Yang-Zhang Volatility Estimator
@ app.callback(
    Output('yz-vol', 'figure'),
    [Input('sec-drpdwn', 'value'),
     Input('intermediate-value1', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json1):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json1 != None:
                df7 = pd.read_json(json1, orient='split')
                if not df7.empty:
                    ticker = sltd_sec
                    df7.name = ticker
                    Sec = Security(df7)
                    Sec.get_returns(price='Close')
                    chart_interval, interval = calc_interval(Sec.df)
                    vol_window = 30
                    trading_periods = 252
                    Sec.YangZhang_estimator(
                        window=vol_window, trading_periods=trading_periods, clean=True, interval=interval)
                    ann_factor, t, p = Sec.get_ann_factor(
                        interval, trading_periods, 24)
                    start_date = Sec.df.index[Sec.df[f'YangZhang{vol_window}_{p}_Ann'] > 0][0]
                    auto_start = start_date
                    end_date = Sec.df.index.max()
                    auto_end = end_date

                    vz_fig = pwe_return_dist_chart(Sec.df, start_date, end_date, tseries=f'YangZhang{vol_window}_{p}_Ann', kind='scatter',
                                                   title=f'Annualized Yang-Zhang {vol_window} {p} Vol.',
                                                   ticker=f'{ticker} YZ Vol.', yTitle=f'{ticker} YZ Vol.',
                                                   asPlot=False, asFigure=True, showlegend=False, theme='white',
                                                   auto_start=auto_start, auto_end=auto_end,
                                                   connectgaps=False, tickformat='.0%', decimals=2)
                    return vz_fig
                else:
                    raise dash.exceptions.PreventUpdate
            else:
                raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


# Correlation Matrix Heatmap
@ app.callback(
    Output('heatmap', 'figure'),
    [Input('sec-drpdwn2', 'value'),
     Input('intermediate-value2', 'data'),
     # Input('dt-picker-range', 'start_date'),
     # Input('dt-picker-range', 'end_date')
     ]
)
def update_graph(sltd_sec, json2):
    if sltd_sec:
        if len(sltd_sec) > 0:
            if json2 != None:
                df8 = pd.read_json(json2, orient='split')
                df_corr = df8.pct_change().corr()
                chart_interval, interval = calc_interval(df8)
                if interval in ['hourly', 'minutes', 'seconds']:
                    title_time = True
                else:
                    title_time = False
                if len(df8.columns) < 4:
                    ticker = ext_str_lst(df8.columns)
                    chart_ticker = True
                else:
                    ticker = ''
                    chart_ticker = False
                start_date = df8.index.min()
                end_date = df8.index.max()

                hmap_fig = pwe_heatmap(df_corr, start_date=start_date, end_date=end_date, title=None, ticker=ticker, yTitle=None, xTitle=None, asPlot=False,
                                    asFigure=True, theme='white', showlegend=False, decimals=2, textangle=0, file_tag=None,
                                    interval='Daily', linecolor=None, title_dates=True, colorscale=["rgb(100, 100, 111)", "rgb(255, 255, 255)", 'rgb(220, 187, 166)', ],
                                    title_time=title_time, chart_ticker=chart_ticker, top_margin=0.9, spacing=0.08, title_x=0.5, title_y=0.933)

                return hmap_fig
            else:
                raise dash.exceptions.PreventUpdate
        else:
            raise dash.exceptions.PreventUpdate

    elif (not sltd_sec) or (len(sltd_sec) == 0):
        raise dash.exceptions.PreventUpdate


if __name__ == '__main__':
    app.run_server(debug=True, port=8000)
