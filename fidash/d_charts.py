"""
Created on Mon Nov 17 07:53:18 2021

@author: Saran Connolly saran.c@pwecapital.com

"""
import os
from datetime import datetime, date, timedelta, timezone
import pandas as pd
from pandas_summary import DataFrameSummary
from pwe.pwetools import check_folder, file_datetime, assign_tz, first_day_of_current_year
import plotly
import cufflinks as cf
import plotly.graph_objects as go
import webbrowser
import dateutil
import re
import pytz


def get_chart_dates(df, start_date=None, end_date=None, utc=True, auto_start=None, auto_end=None):
    """
    Get dates for chart functions.
    More info on date string formats at: https://strftime.org/
    Parameters:
    df              :   The dataframe for the chart, needed to acertain start and end dates, if none are provided.
    start_date      :   The start date for the entire series to be contained in the chart (start of max range).
    end_date        :   The end date for the entire series to be contained in the chart (end of max range).
    auto_start      :   The start of the default range to display on charts, until a user clicks a differnt range.
    auto_end        :   The end of the default range to display on charts, until a user clicks a differnt range.
    """
    if utc:
        utc_now = pytz.utc.localize(datetime.utcnow())
        utc_now.isoformat()
        utc_td_dmy_str = utc_now.strftime("%d-%m-%Y")
        utc_td_ymd_str = utc_now.strftime('%Y-%m-%d')
        t = utc_now
        t_dmy_str = utc_td_dmy_str
        t_ymd_str = utc_td_ymd_str
    elif not utc:
        now = datetime.now()
        td_dmy_str = now.strftime("%d-%m-%Y")
        td_ymd_str = now.strftime('%Y-%m-%d')
        t = now
        t_dmy_str = td_dmy_str
        t_ymd_str = td_ymd_str

    # End date:
    if end_date == None:
        end = df.index.max()
        chart_end = end.strftime("%d-%m-%Y")
    elif (end_date != None) and (isinstance(end_date, str)):
        end = datetime.strptime(end_date, '%Y-%m-%d')
        chart_end = end.strftime("%d-%m-%Y")
    elif (end_date != None) and (type(end_date) == datetime):
        end = end_date
        chart_end = end.strftime("%d-%m-%Y")
    elif (end_date != None) and (type(end_date) == date):
        end = end_date
        chart_end = end.strftime("%d-%m-%Y")
    elif isinstance(end_date, pd.Timestamp):
        end = pd.to_datetime(end_date)
        chart_end = end.strftime("%d-%m-%Y")

    # Start date:
    if start_date == None:
        start = df.index.min()
        chart_start = start.strftime("%d-%m-%Y")
    elif (end_date != None) and (isinstance(end_date, str)):
        end = datetime.strptime(end_date, '%Y-%m-%d')
        chart_end = end.strftime("%d-%m-%Y")
    elif (end_date != None) and (type(end_date) == datetime):
        end = end_date
        chart_end = end.strftime("%d-%m-%Y")
    elif (end_date != None) and (type(end_date) == date):
        end = end_date
        chart_end = end.strftime("%d-%m-%Y")
    elif isinstance(end_date, pd.Timestamp):
        end = pd.to_datetime(end_date)
        chart_end = end.strftime("%d-%m-%Y")

    # Auto end
    if auto_end == None:
        auto_end = t_ymd_str
    elif auto_end == 'yst':
        at_end = t - timedelta(days=1)
        auto_end = at_end.strftime('%Y-%m-%d')
    elif (auto_end != None) and (isinstance(auto_end, str)):
        at_end = datetime.strptime(auto_end, '%Y-%m-%d')
        auto_end = at_end.strftime('%Y-%m-%d')
    elif (auto_end != None) and (type(auto_end) == datetime):
        at_end = auto_end
        auto_end = at_end.strftime('%Y-%m-%d')
    elif (auto_end != None) and (type(auto_end) == date):
        at_end = auto_end
        auto_end = at_end.strftime('%Y-%m-%d')
    elif isinstance(auto_end, pd.Timestamp):
        at_end = pd.to_datetime(auto_end)
        auto_end = at_end.strftime('%Y-%m-%d')

    # Auto start
    if auto_start == None or auto_start == 'ytd':
        at_st = first_day_of_current_year(time=False, utc=False)
        auto_start = at_st.strftime('%Y-%m-%d')
    elif auto_start == '1yr':
        at_st = t - timedelta(days=365)
        auto_start = at_st.strftime('%Y-%m-%d')
    elif (auto_start != None) and (isinstance(auto_start, str)):
        at_start = datetime.strptime(auto_start, '%Y-%m-%d')
        auto_start = at_start.strftime('%Y-%m-%d')
    elif (auto_start != None) and (type(auto_start) == datetime):
        at_start = auto_start
        auto_start = at_start.strftime('%Y-%m-%d')
    elif (auto_start != None) and (type(auto_start) == date):
        at_start = auto_start
        auto_start = at_start.strftime('%Y-%m-%d')
    elif isinstance(auto_start, pd.Timestamp):
        at_start = pd.to_datetime(auto_start)
        auto_start = at_start.strftime('%Y-%m-%d')

    return chart_start, chart_end, auto_start, auto_end


def chart_file_dates(df, start_date=None, end_date=None, time=True):
    if (not isinstance(start_date, datetime)) or (not isinstance(end_date, datetime)):
        time = False
    if time:
        if start_date == None:
            sdate = df.index.strftime('%Y-%m-%d_%H:%M:%S').min()
            title_start = df.index.strftime('%Y-%m-%d %H:%M:%S%z').min()
        elif start_date != None and not (isinstance(start_date, str)):
            try:
                sdate = datetime.strftime(start_date, "%Y-%m-%d_%H:%M:%S")
            except ValueError:
                sdate = datetime.strftime(start_date, '%Y-%m-%d')
            try:
                title_start = datetime.strftime(
                    start_date, '%Y-%m-%d %H:%M:%S%z')
            except ValueError:
                title_start = assign_tz(start_date, 'UTC')
                title_start = datetime.strftime(
                    title_start, '%Y-%m-%d %H:%M:%S%z')
        elif start_date != None and isinstance(start_date, str):
            sdate = start_date
        sdate = sdate.strip().replace(':', ',')

        if end_date == None:
            edate = df.index.strftime('%Y-%m-%d_%H:%M:%S').max()
            if str(df.index.max().time()) == '23:00:00':
                title_end = df.index.max() + timedelta(minutes=59, seconds=59)
                title_end = title_end.strftime('%Y-%m-%d %H:%M:%S%z')
            else:
                title_end = df.index.strftime('%Y-%m-%d %H:%M:%S%z').max()
        elif end_date != None and not (isinstance(end_date, str)):
            try:
                edate = datetime.strftime(end_date, "%Y-%m-%d_%H:%M:%S")
            except ValueError:
                edate = datetime.strftime(end_date, '%Y-%m-%d')
            try:
                title_end = datetime.strftime(end_date, '%Y-%m-%d %H:%M:%S%z')
            except ValueError:
                title_end = assign_tz(start_date, 'UTC')
                title_end = datetime.strftime(title_end, '%Y-%m-%d %H:%M:%S%z')
        elif end_date != None and isinstance(end_date, str):
            edate = end_date
        edate = edate.strip().replace(':', ',')

    else:
        if start_date == None:
            sdate = df.index.strftime('%Y-%m-%d').min()
            title_start = df.index.strftime('%Y-%m-%d').min()
        elif start_date != None and not (isinstance(start_date, str)):
            try:
                sdate = datetime.strftime(start_date, "%Y-%m-%d")
            except ValueError:
                sdate = datetime.strftime(start_date, '%Y-%m-%d')
            try:
                title_start = datetime.strftime(start_date, '%Y-%m-%d')
            except ValueError:
                title_start = assign_tz(start_date, 'UTC')
                title_start = datetime.strftime(title_start, '%Y-%m-%d')
        elif start_date != None and isinstance(start_date, str):
            sdate = start_date
        sdate = sdate.strip().replace(':', ',')

        if end_date == None:
            edate = df.index.strftime('%Y-%m-%d').max()
            if str(df.index.max().time()) == '23:00:00':
                title_end = df.index.max() + timedelta(minutes=59, seconds=59)
                title_end = title_end.strftime('%Y-%m-%d')
            else:
                title_end = df.index.strftime('%Y-%m-%d').max()
        elif end_date != None and not (isinstance(end_date, str)):
            try:
                edate = datetime.strftime(end_date, "%Y-%m-%d")
            except ValueError:
                edate = datetime.strftime(end_date, '%Y-%m-%d')
            try:
                title_end = datetime.strftime(end_date, '%Y-%m-%d')
            except ValueError:
                title_end = assign_tz(start_date, 'UTC')
                title_end = datetime.strftime(title_end, '%Y-%m-%d')
        elif end_date != None and isinstance(end_date, str):
            edate = end_date
        edate = edate.strip().replace(':', ',')

    chart_dates = str(title_start+" : "+title_end)
    return sdate, edate, chart_dates


def get_chart_title(title, chart_ticker, title_dates, ticker, chart_dates):
    if title != None and chart_ticker == True:
        if title_dates != None and title_dates != False:
            chart_title = '{} ({}) - {}'.format(title, ticker, chart_dates)
        elif title_dates == None or title_dates == False:
            chart_title = '{} ({})'.format(title, ticker)
    elif title != None and chart_ticker == False:
        if title_dates != None and title_dates != False:
            chart_title = '{} - {}'.format(title, chart_dates)
        elif title_dates == None or title_dates == False:
            chart_title = '{}'.format(title)
    elif title == None and chart_ticker == True:
        if title_dates != None and title_dates != False:
            chart_title = '{} - {}'.format(ticker, chart_dates)
        elif title_dates == None or title_dates == False:
            chart_title = '{}'.format(ticker)
    elif title == None and chart_ticker == False:
        if title_dates != None and title_dates != False:
            chart_title = '{}'.format(chart_dates)
        elif title_dates == None or title_dates == False:
            chart_title = ''
    return chart_title

PWE_skin = "#DCBBA6" # "rgb(220,187,166)"
skin_lighter = "#E5CDBF" # "rgb(229,205,191)"
skin_lightest = "#EDDDD5" # "rgb(237,221,213)"
skin_darker = "#d3ab95" # "rgb(211,171,149)"
pwe_darkest = "#C48E71"
black = "#000000"
PWE_grey = "#64646F"
PWE_lgrey = "#7D7D89"
PWE_blue = "#a4b3c1"
PWE_dark_blue = "#869AAC"
ironsidegrey = "#6F6F64"
PWE_light_grey = "#a5a5a5"
PWE_ig_light_grey = '#58595b'
PWE_ig_dark_grey = '#403d3e'
vic_teal = '#d1d3d4'
pwe_teal = '#99B7BD'
pwe_light_teal = '#b8cdd1'
pwe_teal2 = '#b6b6b6'
PWE_black = '#231f20'

transparent = '#DCBBA600'

PWE_mono_darker = "#CE9F81"

# analagous:
PWE_yellow = "#DCD6A6"
PWE_red = "#DCA6AC"

PWE_triadic_teal = "#A6DCBB"
PWE_triadic_purple = "#BBA6DC"

# tetradic:
PWE_green = "#ACDCA6"
RegentStBlue = "#A6C7DC"
PWE_pinkyPurple = "#D6A6DC"

PWE_video_teal = "#006C5E"

# transparent: https://gist.github.com/lopspower/03fb1cc0ac9f32ef38f4
PWE_skin80_h = "#dcbaa6"
PWE_skin_20 = "#DCBBA633"
PWE_skin_38 = "#DCBBA661"
henanigans_light1 = "#A4A4A4"

cf.go_offline()
cf.set_config_file(offline=False, world_readable=True)

"""
Cuffliks:
Tweak paramaters: check the signature of these methods by pressing Shift + Tab in the Jupyter notebook.
- add_bollinger_bands() - It adds Bollinger Bands (BOLL) study to the figure.
- add_volume() - It adds volume bar charts to the figure.
- add_sma() - It adds Simple Moving Average (SMA) study to the figure.
- add_rsi() - It adds Relative Strength Indicator (RSI) study to the figure.
- add_adx() - It adds Average Directional Index (ADX) study to the figure.
- add_cci() - It adds Commodity Channel Indicator study to the figure.
- add_dmi() - It adds Directional Movement Index (DMI) study to the figure.
- add_ema() - It adds Exponential Moving Average (EMA) to the figure.
- add_atr() - It adds Average True Range (ATR) study to the figure.
- add_macd() - It adds Moving Average Convergence Divergence (MACD) to the figure.
- add_ptps() - It adds Parabolic SAR (PTPS) study to the figure.
- add_resistance() - It adds resistance line to the figure.
- add_trendline() - It adds trend line to the figure.
- add_support() - It adds support line to the figure.

Use: cf.help() or cf.help(figure) to see paramaters

"""


def add_tags(qf, tags=None, theme='white', showarrow=True, arrowhead=6, fontsize=6, textangle=0, yanchor="bottom", fontfamily='Roboto'):
    """
    Add settlement dates or other annotations to a figure.
    Pass in a column of annotations in string format.

    """
    if tags != None:
        dark = ("henanigans", "solar", "space")
        if str(theme) in dark:
            fontcolor = 'henanigans_light1'
            arrowcolor = 'henanigans_light1'
            style = 'dark'
        else:
            fontcolor = PWE_ig_light_grey
            arrowcolor = PWE_ig_light_grey
            style = theme

        # Add an annotation:
        qf.layout['annotations']['values'] = []
        qf.add_annotations(tags,
                           showarrow=True, y=0,
                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                           fontsize=fontsize, textangle=0, yanchor=yanchor, fontfamily=fontfamily)
        # qf.iplot(xrange=[auto_start,auto_end])
    else:
        pass
    return qf


def pwe_format(f_name):
    print(f_name)
    cwd = os.getcwd()
    file_path_str = f'{cwd}{f_name}'
    file_path = f'{file_path_str}.html'
    # file_path = file_path.replace(' ', '\\ ')
    # print(file_path_str)
    # print(file_path)
    # print('')

    prefix = cwd
    relative_path = f'/{os.path.relpath(file_path,prefix)}'
    # print(prefix)
    # print(relative_path)
    # print('')

    local_path_str = f'{f_name}'
    local_file_path = f'/{local_path_str}.html'
    unf_link = f'http://localhost:8888/view{relative_path}'
    # print(local_path_str)
    # print(local_file_path)
    # print(unf_link,"(unformatted)")

    # Swap between local_path_str and relative_path for the "unf_link" calc and the 'link" clac below if
    # the charts arent displaying in browser automatically. Or else change cwd.

    text_wrapper = open(file_path, encoding="utf-8")
    html_text = text_wrapper.read()
    # print(html_text)

    # https://www.freecodeformat.com/svg-editor.php
    plotly_svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 132 132'><defs><style>.cls-1 {fill: #3f4f75;} .cls-2 {fill: #80cfbe;} .cls-3 {fill: #fff;}</style></defs><title>plotly-logomark</title><g id='symbol'><rect class='cls-1' width='132' height='132' rx='6' ry='6'/><circle class='cls-2' cx='78' cy='54' r='6'/><circle class='cls-2' cx='102' cy='30' r='6'/><circle class='cls-2' cx='78' cy='30' r='6'/><circle class='cls-2' cx='54' cy='30' r='6'/><circle class='cls-2' cx='30' cy='30' r='6'/><circle class='cls-2' cx='30' cy='54' r='6'/><path class='cls-3' d='M30,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,30,72Z'/><path class='cls-3' d='M78,72a6,6,0,0,0-6,6v24a6,6,0,0,0,12,0V78A6,6,0,0,0,78,72Z'/><path class='cls-3' d='M54,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,54,48Z'/><path class='cls-3' d='M102,48a6,6,0,0,0-6,6v48a6,6,0,0,0,12,0V54A6,6,0,0,0,102,48Z'/></g></svg>"
    pwe_svg = "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 127.74 132'><defs><style>.a{fill:#dcbba6;}.b{fill:none;}.c{fill:#646470;}</style></defs><title>pwe-logomark</title><g id='symbol'><rect class='a' x='0.34' y='9.19' width='122.81' height='122.81'/><path class='b' d='M109.16,16.78l-40,101.35L50,65.11c-1.86,2.81-3.78,5.82-5.86,8.88C31.8,92.18,17.09,113.56,4.33,131.88H122.81V52.56l-4-10.32C116.3,35.5,112.52,25.53,109.16,16.78Z'/><path d='M111.7,8.38,109.2,2,69.4,102.84,51.46,53.18l-3,4.46C45.8,61.7,42.87,66.27,39.65,71,28.58,87.34,13,110,0,128.64v3.24H4.33C17.09,113.56,31.8,92.18,44.16,74c2.08-3.06,4-6.07,5.86-8.88l19.16,53,40-101.35c3.36,8.75,7.14,18.72,9.67,25.46l4,10.32V37.47C119.62,29,115.12,17.19,111.7,8.38Z'/><polygon class='c' points='61.84 55.95 55.97 65.64 58.34 72.16 60.6 68.42 71.28 97.98 74.28 90.38 61.84 55.95'/><path class='c' d='M121.92,0c-3.13,7.94-6.47,16.37-10,25.12-3.9,9.82-8,20.05-12.12,30.48C93,72.78,86,90.48,79.88,105.9l-2.79-7.74-3,7.6,5.57,15.41,2.62-6.65C88.92,97.68,97,77.3,104.87,57.59c3.3-8.28,6.68-16.78,10-25.12C119.44,21,123.88,9.78,127.74,0Z'/></g></svg>"

    name = f_name
    file = open(file_path).read()

    replaced_txt = file.replace(
        '"linkText": "Export to plot.ly",', '"linkText": "PWE Capital",')
    replaced_txt2 = replaced_txt.replace(
        '"plotlyServerURL": "https://plot.ly"', '"plotlyServerURL": "https://pwecapital.com/"')
    replaced_txt3 = replaced_txt2.replace(
        '"X svg a":"fill:#447adb;","X svg a:hover":"fill:#3c6dc5;",', '"X svg a":"fill:#64646F;","X svg a:hover":"fill:#DCBBA6;",')
    replaced_txt4 = replaced_txt3.replace(plotly_svg, pwe_svg)
    replaced_txt5 = replaced_txt4.replace(
        'e.href="https://plotly.com/",', 'e.href="https://pwecapital.com/",')
    replaced_txt6 = replaced_txt5.replace(
        'Produced with Plotly', 'Redefining R.O.I.™')
    replaced_txt7 = replaced_txt6.replace(
        'background:#69738a', 'background:#64646F')
    replaced_txt8 = replaced_txt7.replace('#8c97af', '#64646F')
    replaced_txt9 = replaced_txt8.replace(
        'rgba(140,151,175,.9)', 'rgba(100, 100, 111, .9)')

    output_html = f"{file_path_str}_PWE.html"
    writer = open(output_html, 'w')
    writer.write(replaced_txt9)
    writer.close()

    ##
    output_html_path = f"{cwd}{f_name}"
    abs_path = f'/{os.path.abspath(output_html)}'
    chart_html = f"http://localhost:8888/view{local_path_str}"
    chart_file = f"file:///{abs_path}"

    # webbrowser.open_new_tab(chart_file)
    # print(output_html_path)
    # print(chart_html)
    # print(chart_file)

    # Swap between local_path_str and relative_path for the "chart_html" calc if
    # the charts aren't displaying in browser automatically. Or else change cwd to match the chart directory.

    return chart_html, chart_file


def quant_chart(df, start_date, end_date, ticker=None, title=None, theme='henanigans', auto_start=None, auto_end=None,
                asPlot=False, asFigure=True, showlegend=True, boll_std=2, boll_periods=20, showboll=False, showrsi=False, rsi_periods=14,
                showama=False, ama_periods=9, showvol=False, showkal=False, kal_periods=1, show_range=False, annots=None, textangle=0,
                file_tag=None, support=None, resist=None, annot_font_size=6, title_dates=False, title_time=False, chart_ticker=True,
                top_margin=0.9, spacing=0.08, range_fontsize=9.8885, title_x=0.5, title_y=0.933,
                arrowhead=6, arrowlen=-50):
    """

    df : The Pandas dataframe used for the chart. It must contain open, high, low and close, and may also contain volume. Anything else will be ignored, unless specified.

    Plots an interactive chart and opens it in a new browser tab. This function also formats the plot with PWE branding.

    # https://notebook.community/santosjorge/cufflinks/Cufflinks%20Tutorial%20-%20Colors

    Themes: ‘ggplot’,  'pearl’, 'solar’, 'space’, 'white’, 'polar’, 'henanigans’, 

    auto_start : The start date for the range that will automatically display on the chart. e.g. if set to the start of this year,
    the range will automatically display YTD, until a user clicks a different range. The default setting is 1 year prior to today's date, in GMT time.

    auto_end : The end date for the range that will automatically display on the chart. The default setting is today's date, in GMT time.

    asPlot : Whether to save it as a HTML plot. If True, it will save the plot and open it in a new browser tab.

    anns: Annotations. A dict.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = str(theme)

    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey]

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_interative_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_interative_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_interative_{style}'

    qf = cf.QuantFig(df, legend='top', name=ticker,
                     rangeslider=False, up_color=PWE_skin, down_color=PWE_grey, fontfamily='Roboto', theme=theme,
                     top_margin=top_margin, spacing=spacing, xrange=[
                         auto_start, auto_end],
                     title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    # To make a permanent change to theme:
    qf.theme.update(up_color=PWE_skin, down_color=PWE_grey)

    # A rangeselector allows us to select different periods on the same chart. This can be any variety of Year, Months, Hours etc.
    # For example: steps=['1y','2 months','5 weeks','ytd','2mtd']
    rangeselector = dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                         bgcolor=(PWE_skin, .2),
                         fontsize=range_fontsize, fontfamily='Roboto')

    qf.layout.update(rangeselector=rangeselector)

    # Add an annotations:
    if annots != None:
        qf.add_annotations(annots,
                           showarrow=True, y=0, arrowhead=arrowhead, arrowcolor=arrowcolor, arrowlen=arrowlen, fontcolor=fontcolor,
                           fontsize=annot_font_size, anntextangle=0, yanchor="bottom", fontfamily='Roboto')

    # Add a support or resistance line:
    # qf.add_support(date='2021-04-23',on='low',mode='starttoend', to_strfmt='%Y-%m-%d',color=PWE_blue) #text='resistance',

    if showboll == True:
        qf.add_bollinger_bands(periods=boll_periods, boll_std=boll_std, colors=[
                               'black', PWE_skin_38], fill=True, name=f"BOLL({boll_std},{boll_periods})")

    qf.layout.update(showlegend=showlegend)
    if showama == True:
        qf.add_ama(periods=ama_periods, width=2, color=[
                   PWE_blue, vic_teal], legendgroup=False)

    if showkal == True:
        qf.add_kalman(periods=kal_periods, width=2, column='Close', color=[
                   pwe_light_teal, pwe_teal], legendgroup=False)

    if showrsi == True:
        qf.add_rsi(periods=rsi_periods, color=PWE_skin, legendgroup=False)

    if showvol == True:
        qf.add_volume(datalegend=True, legendgroup=True,
                      name="Volume", showlegend=False, up_color=PWE_grey)


    # for trace in qf['data']:
    #    if(trace == 'Volume'): trace['datalegend'] = False

    if show_range == True:
        fig = qf.iplot(hspan=dict(y0=support, y1=resist, color=PWE_skin, fill=True, opacity=.3, yref='y2'),
                       rangeslider=False, asPlot=asPlot, asFigure=asFigure, filename=f'.{f_name}', auto_open=False)
    else:
        fig = qf.iplot(rangeslider=False, asPlot=asPlot,
                       asFigure=asFigure, filename=f'.{f_name}', auto_open=False)

    # chart_html, chart_file = pwe_format(f_name)

    return fig  # chart_html, chart_file


def single_line_chart(df, start_date, end_date, columns=None, kind='scatter', title=None, ticker=None,
                      yTitle=None, showlegend=False, legend='top', asPlot=False, asFigure=True,
                      theme='white', fontsize=6, auto_start=None, auto_end=None, connectgaps=False,
                      annots=None, annot_col='Close', file_tag=None,
                      title_dates=False, title_time=False, chart_ticker=True, top_margin=0.9, spacing=0.08,
                      range_fontsize=9.8885, title_x=0.5, title_y=0.933, arrowhead=6, arrowlen=-50):
    """

    Plots a line or scatter chart within an iPython notebook. It will not format HTML with PWE style or open in a browser window.

    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.

    kind : set 'scatter' for a line chart.

    Select the text 'iplot' in the function below and click shift and tab for more options.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, skin_lighter, skin_darker, PWE_ig_light_grey, PWE_ig_dark_grey]

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_singleline_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_singleline_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_singleline_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    if columns is None:
        if annots == None:
            plt_int = df.iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False, xTitle='Date', yTitle=yTitle,
                               colors=colors, fontfamily='Roboto', theme=theme, asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto', x=-0.025, y=1, visible=True),
                               xrange=[auto_start,
                                       auto_end], connectgaps=connectgaps,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})
        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                           anntextangle=0, arrowlen=arrowlen,)

            plt_int = df.iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                               xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                               asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                  x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                               annotations=ans, anntextangle=0,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    else:
        if annots == None:
            plt_int = df[columns].iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=[PWE_skin, PWE_grey], fontfamily='Roboto',
                                        theme=theme, asPlot=asPlot, asFigure=asFigure, filename=f'.{f_name}',
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, arrowlen=arrowlen,
                                           fontcolor=fontcolor, anntextangle=-0)

            plt_int = df[columns].iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                                        asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                                        annotations=ans, anntextangle=0,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    #rangeslider: {range:['2021-01-01', '2021-08-10']}
    # range=['2021-01-01','2021-08-10']
    #add_range_selector(plt_int, axis_name='xaxis', ranges=None, default=None)

    #fig = go.Figure(df)
    # fig.show()

    # print(f_name)
    return plt_int  # , f_name

# help(brr.iplot)
# cf.tools.get_range_selector


def get_cf_annots(df, annotations, annot_col='Close', fontsize=6, arrowhead=6, arrowcolor='#58595b',
                  fontcolor='#58595b', anntextangle=0):
    ans = cf.tools.get_annotations(df=df, annotations=annotations, annot_col=annot_col,
                                   fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                   arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                   anntextangle=-anntextangle)

    return ans


def pwe_line_chart(df, start_date, end_date, columns=None, kind='scatter', title=None, ticker=None,
                   yTitle=None, asPlot=False, asFigure=True, theme='white', showlegend=False, legend='top',
                   auto_start=None, auto_end=None, connectgaps=False, annots=None,
                   anntextangle=0, fontsize=6, annot_col=None, file_tag=None,
                   title_dates=False, title_time=False, chart_ticker=True,
                   top_margin=0.9, spacing=0.08, range_fontsize=9.8885,
                   title_x=0.5, title_y=0.933, arrowhead=6, arrowlen=-50):
    """
    Plots an interactive line or scatter chart and opens it in a new browser. It also formats HTML with PWE style.

    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.

    kind : set 'scatter' for a line chart.name

    Select the text 'iplot' in the function below and click shift and tab for more options.
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_light_grey
        style = theme

    colors = [PWE_skin, PWE_grey, black, pwe_light_teal, PWE_blue,
                skin_darker, PWE_ig_light_grey, skin_lighter, PWE_ig_dark_grey, pwe_darkest, PWE_lgrey, PWE_black, pwe_teal, PWE_dark_blue, vic_teal]

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_line_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_line_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_line_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    if columns is None:
        if annots == None:
            plt_int = df.iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                               xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                               asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                  x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})
        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                           anntextangle=-anntextangle, arrowlen=arrowlen)

            plt_int = df.iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                               xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                               asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                  x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end],
                               connectgaps=connectgaps, annotations=ans, anntextangle=anntextangle,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    else:
        if annots == None:
            plt_int = df[columns].iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto',
                                        theme=theme, asPlot=asPlot, asFigure=asFigure, filename=f'.{f_name}',
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1.05, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                           anntextangle=-anntextangle, arrowlen=arrowlen)

            plt_int = df[columns].iplot(kind=kind, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                                        asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end],
                                        connectgaps=connectgaps, annotations=ans, anntextangle=anntextangle,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def pwe_return_dist_chart(df, start_date, end_date, tseries='Price_Returns', kind='scatter', title=None, ticker=None, yTitle=None, asPlot=False, asFigure=True,
                          theme='white', showlegend=False, auto_start=None, auto_end=None, connectgaps=False, tickformat='.2%', decimals=2, file_tag=None,
                          title_dates=False, title_time=False, chart_ticker=True, range_fontsize=9.8885, top_margin=0.9, spacing=0.08,
                          title_x=0.5, title_y=0.933):  # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """
        *Put start_date ad end_date after df and before other arguemets, with no = to any value or it will throw an error.

    Plots an interactive returns distribiution chart and formats the HTML with PWE style.

    df : The dataframe to plot. 

    returns : a pandas series within the dataframe which contains % returns per time period.

    tickformat : the format for the y axis. e.g % or $.

    decimals: the number of decimals to round the number quoted in the hover info panel.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey]

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    df['Series_str'] = df[tseries]

    df['Series_str'] = pd.Series([round(val, 6)
                                 for val in df[tseries]], index=df.index)
    df['Series_str'] = pd.Series(
        [f"{val*100:.{decimals}f}%" for val in df['Series_str']], index=df.index)

    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(
            str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        try:
            df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
        except:
            pass
            df['Date'] = df.index.to_series().dt.date.astype(str)
            pass
        try:
            df['Date'] = df.index.to_series().astype(str)
        except:
            raise ValueError
        if 'Date_Ret_str' not in df:
            df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']

    text = df['Date_Ret_str'].values.tolist()

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_dist_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_dist_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_dist_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    plt_int = df[tseries].iplot(kind=kind, showlegend=showlegend, legend='top', rangeslider=False, xTitle='Date', yTitle=yTitle,
                                colors=colors, fontfamily='Roboto', theme=theme, asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                                rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'], bgcolor=(PWE_skin, .2),
                                                   fontsize=range_fontsize, fontfamily='Roboto', x=-0.025, y=1, visible=True),
                                xrange=[auto_start, auto_end], connectgaps=connectgaps, yaxis_tickformat=tickformat, hoverinfo="text", text=text,
                                title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})  # hovertemplate=hovertemplate

    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    # plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def pwe_return_bar_chart(df, start_date, end_date, tseries='Price_Returns', kind='scatter', title=None, ticker=None, yTitle=None, xTitle=None,
                         asPlot=False, asFigure=True, theme='white', showlegend=False, auto_start=None, auto_end=None, tickformat='.2%', decimals=2,
                         orientation='v', textangle=0, file_tag=None, title_dates=False, title_time=False, chart_ticker=True, range_fontsize=9.8885,
                         top_margin=0.9, spacing=0.08, title_x=0.5, title_y=0.933):  # text=None hovermode='x', hovertemplate="%{y:.6%}",
    """

    Plots an interactive bar chart with the HTML formatted to the PWE style. It opens the plot in a new browser tab.

    orientation :     'v' is vertical.
                    'h' is horizontal.

    textangle :        The angle of the text to display on each bar. 0 is horizontal and -90 is vertical.

    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    # colors = [PWE_skin, PWE_grey, black, vic_teal,
    #           PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey]
    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, skin_lighter, skin_darker, PWE_ig_light_grey, PWE_ig_dark_grey]

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    df['Series_str'] = df[tseries]
    df['Series_str'] = pd.Series([round(val, 6)
                                 for val in df[tseries]], index=df.index)
    df['Series_str'] = pd.Series(
        [f"{val*100:.{decimals}f}%" for val in df['Series_str']], index=df.index)

    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(
            str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']

    hovertext = df['Date_Ret_str'].values.tolist()
    text = df['Series_str'].values.tolist()

    if orientation == 'h':
        xTitle = yTitle
        yTitle = 'Date'
    else:
        xTitle = 'Date'
        yTitle = yTitle

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_bar_chart_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_bar_chart_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_bar_chart_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    plt_int = df[tseries].iplot(kind=kind, showlegend=showlegend, legend='top', rangeslider=False, xTitle=xTitle, yTitle=yTitle,
                                colors=colors, fontfamily='Roboto', theme=theme, asPlot=asPlot, asFigure=asFigure, filename=f'./{f_name}',
                                rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'], bgcolor=(PWE_skin, .2),
                                                   fontsize=range_fontsize, fontfamily='Roboto', x=-0.025, y=1, visible=True),
                                xrange=[
                                    auto_start, auto_end], yaxis_tickformat=tickformat, hoverinfo="text",
                                hovertext=hovertext, text=text, orientation=orientation, textangle=textangle,
                                title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})  # hovertemplate=hovertemplate

    #plt_int['layout']['hovermode'] = dict(side='left')
    #plt_int['layout']['hovermode'] = hovermode
    # plt_int.iplot()
    # hovermode = ['x', 'y', 'closest', False, 'x unified', 'y unified'] '%{y:.2%}'

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def pwe_hist(df, start_date, end_date, tseries='Price_Returns', title=None, ticker=None, yTitle=None, xTitle=None, asPlot=False,
             asFigure=True, theme='white', showlegend=False, decimals=2, orientation='v', textangle=0, file_tag=None, interval='Daily',
             bins=100, histnorm='frequency', histfunc='count', yaxis_tickformat='.2%', xaxis_tickformat='.2%', linecolor=None,
             title_dates=True, title_time=True, chart_ticker=True, top_margin=0.9, spacing=0.08, title_x=0.5, title_y=0.933):
    """

    Plots an interactive histogram with the HTML formatted to the PWE style. It opens the plot in a new browser tab.

    orientation :     'v' is vertical.
                    'h' is horizontal.

    textangle :        The angle of the text to display on each bar. 0 is horizontal and -90 is vertical.

    histnorm : string - '', 'percent', 'probability', 'density', 'probability density'
    histfunc : string - count, sum, avg, min, max

    linecolor : string - specifies the line color of the histogram

    bins : int or tuple 
                        if int:
                                Specifies the number of bins 
                        if tuple:
                                (start, end, size)
                                start : starting value
                                end: end value
                                size: bin size

    See: https://github.com/santosjorge/cufflinks/blob/master/cufflinks/plotlytools.py
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    if linecolor == None or linecolor == 'PWE_grey':
        linecolor = PWE_grey
    elif linecolor == 'PWE':
        linecolor = PWE_skin
    if bins == None:
        bins = int(df[tseries].count())

    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey]

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    # format_dict = { tseries : '{:.2%}'}
    # df.style.format(format_dict)

    df['Series_str'] = pd.Series([round(val, decimals)
                                 for val in df[tseries]], index=df.index)
    df['Series_str'] = pd.Series(
        [f"{val*100:.{decimals}f}%" for val in df['Series_str']], index=df.index)

    if 'DateTime_str' in df:
        df['Date_Ret_str'] = df['DateTime_str'].astype(
            str)+", "+df['Series_str']
    elif 'DateTime' in df:
        df['Date_Ret_str'] = df['DateTime'].astype(str)+", "+df['Series_str']
    elif 'Date' in df:
        df['Date_Ret_str'] = df['Date'].astype(str)+", "+df['Series_str']
    else:
        df['Date_Ret_str'] = df.index.astype(str)+", "+df['Series_str']

    hovertext = df['Date_Ret_str'].values.tolist()
    text = df['Series_str'].values.tolist()

    if xTitle == None:
        xTitle = f'{interval} Return (%)'
    if yTitle == None:
        if histnorm == '':
            yTitle = 'Frequency'
            yTitle.capitalize()
        else:
            yTitle = histnorm.capitalize()

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_').replace(' ', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_hist_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_hist_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_hist_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    plt_int = df[[tseries]].iplot(kind="histogram", bins=bins, theme=theme, showlegend=showlegend, legend='top', rangeslider=False,
                                  xTitle=xTitle, yTitle=yTitle, colors=colors, fontfamily='Roboto', asPlot=asPlot, asFigure=asFigure,
                                  filename=f'./{f_name}', hoverinfo="text", hovertext=hovertext, text=text, orientation=orientation, textangle=textangle,
                                  linecolor=linecolor, histnorm=histnorm, histfunc=histfunc, yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                                  title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})
    # xaxis = dict(
    # tickformat = '%.format.%5f%',
    # title = xTitle,
    # hoverformat = '.5f',
    # showgrid = True),)

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def pwe_box(df, start_date=None, end_date=None, title=None, ticker=None, yTitle=None, xTitle=None, asPlot=False,
            asFigure=True, theme='white', showlegend=False, decimals=2, orientation='v', textangle=0, file_tag=None,
            interval='Daily', yaxis_tickformat='.2%', xaxis_tickformat='.2%', linecolor=None, title_dates=True,
            title_time=True, chart_ticker=True, top_margin=0.9, spacing=0.08, title_x=0.5, title_y=0.933):
    """

    Plots an interactive box plot with the HTML formatted to the PWE style. It opens the plot in a new browser tab.

    orientation :     'v' is vertical.
                    'h' is horizontal.

    textangle :        The angle of the text to display on each box. 0 is horizontal and -90 is vertical.m

    boxpoints : string
                Displays data points in a box plot
                    outliers
                    all
                    suspectedoutliers
                    False

    See: https://github.com/santosjorge/cufflinks/blob/master/cufflinks/plotlytools.py
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    if linecolor == None or linecolor == 'PWE_grey':
        linecolor = PWE_grey
    elif linecolor == 'PWE':
        linecolor = PWE_skin

    # colors = [PWE_skin, PWE_grey, black, vic_teal,
    #           PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey,]
    # colors = [PWE_skin, PWE_grey, black, vic_teal, PWE_blue,
    #             skin_darker, PWE_ig_light_grey, PWE_ig_dark_grey, skin_lighter]
    # colors = [PWE_skin, PWE_grey, black, vic_teal,
    #           PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey, skin_darker, skin_lighter]
    colors = [PWE_skin, PWE_grey, black, pwe_light_teal, PWE_blue,
                PWE_ig_light_grey, PWE_ig_dark_grey, skin_darker, PWE_lgrey, PWE_black, pwe_teal, PWE_dark_blue, vic_teal, skin_lighter, pwe_darkest,]

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    if xTitle == None:
        xTitle = f'{interval} Return (%)'

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_').replace(' ', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_box_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_box_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_box_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    plt_int = df.iplot(kind="box", theme=theme, showlegend=showlegend, legend='top', rangeslider=False,
                       xTitle=xTitle, yTitle=yTitle, colors=colors, fontfamily='Roboto', asPlot=asPlot, asFigure=asFigure,
                       filename=f'./{f_name}', hoverinfo="text", orientation=orientation, textangle=textangle,
                       yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                       title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})
    # xaxis = dict(
    # tickformat = '%.format.%5f%',
    # title = xTitle,
    # hoverformat = '.5f',
    # showgrid = True),)

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def calc_table_height(df, base=244, height_per_row=20, char_limit=30, height_padding=16.5):
    '''
    df: The dataframe with only the columns you want to plot
    base: The base height of the table (header without any rows)
    height_per_row: The height that one row requires
    char_limit: If the length of a value crosses this limit, the row's height needs to be expanded to fit the value
    height_padding: Extra height in a row when a length of value exceeds char_limit
    '''
    total_height = 0 + base
    for x in range(df.shape[0]):
        total_height += height_per_row
    for y in range(df.shape[1]):
        if len(str(df.iloc[x][y])) > char_limit:
            total_height += height_padding
    return total_height


def pwe_table(df, file_tag=None, ticker=None, head_text_size=16, text_size=12, head_align='left', text_align='right', fill_style='alternate',
              autosize=False, width=730, height=388):
    """
    Create a Plotly table in PWE style.
    fill_style  :   'alternate' will display alternating bands for each row.
                    'left_index' will display a darker left column with no alternaing rows.
                    Alternatively, pass a custom list. e.g. fill_style=[pwe_r618, pwe_r382, pwe_r382, pwe_r382 ]*2
    """

    import plotly.graph_objects as go
    from plotly.offline import iplot  # init_notebook_mode
    from cufflinks.colors import to_rgba

    pwe_r618 = to_rgba("#DCBBA6", 0.618)
    pwe_r382 = to_rgba("#DCBBA6", 0.382)
    rowOddColor = pwe_r382
    rowEvenColor = pwe_r618

    n_cols = df.shape[1]
    n_rows = df.shape[0]

    alternate = [[rowOddColor, rowEvenColor]*n_rows]
    left_index = dict(color=[pwe_r618, pwe_r382])

    if fill_style == 'alternate':
        fill_color = alternate
        fill = None
    elif fill_style == 'left_index':
        fill_color = None
        fill = left_index
    else:
        fill_color = None
        fill = dict(color=fill_style)

    if fill_color:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color="#DCBBA6",
                        align=head_align,
                        font=dict(family='Roboto', size=head_text_size)),
            cells=dict(values=df.transpose().values.tolist(),
                       #fill_color = [pwe_r618, pwe_r382, pwe_r382, pwe_r382 ]*2,
                       fill_color=fill_color,
                       align=text_align, font=dict(family='Roboto', size=text_size)))])

    else:
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(df.columns),
                        fill_color="#DCBBA6",
                        align=head_align,
                        font=dict(family='Roboto', size=head_text_size)),  # cells=dict(values=df.transpose().values.tolist(),
            cells=dict(values=df.transpose().values.tolist(),
                       fill=fill,
                       align=text_align, font=dict(family='Roboto', size=text_size)))])

    fig.update_layout(
        autosize=autosize,
        width=width,
        height=height,
        margin=dict(
            l=0,
            r=0,
            b=0,
            t=0,
            pad=0))

    # fig.show()
    iplot(fig)

    style = 'table'
    tkr = ticker.replace('/', '_')
    if file_tag == None:
        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{style}'
        else:
            f_name = f'/charts/{tkr}_{style}'
    else:
        f_name = f'/charts/{tkr}_{file_tag}_{style}'

    fig.write_html(f'.{f_name}.html')

    # chart_html, chart_file = pwe_format(f_name)

    return fig  # chart_html, chart_file


def pwe_line_scatter_chart(df, marker_x, marker_y, start_date, end_date, columns=None, kind='scatter', title=None,
                           ticker=None, yTitle=None, asPlot=False, asFigure=True, theme='white', showlegend=False,
                           legend='top', auto_start=None, auto_end=None, connectgaps=False, annots=None, anntextangle=0,
                           fontsize=6, annot_col=None, file_tag=None, title_dates=False, title_time=False, chart_ticker=True,
                           top_margin=0.9, spacing=0.08, range_fontsize=9.8885, yaxis_tickformat='.2%', xaxis_tickformat='',
                           title_x=0.5, title_y=0.933, arrowhead=6, arrowlen=-50, mode="lines+markers",
                           marker_color=None, marker_name=None, marker_size=2):
    """
    THIS FUNCTION NEEDS TO BE PASTED INTO THE PROJECT FILE TO MANUALLY FORMAT THE HTML.

    Plots an interactive line or scatter chart and opens it in a new browser. It also formats HTML with PWE style.

    auto_start, auto_end : Set default dates to display on the chart. Needs to be '%Y-%m-%d'.

    kind : set 'scatter' for a line chart.name

    Select the text 'iplot' in the function below and click shift and tab for more options.
    """
    import plotly as py
    import plotly
    import cufflinks as cf
    import pandas as pd
    import numpy as np
    from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
    init_notebook_mode(connected=True)
    cf.go_offline()
    import plotly.graph_objects as go

    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_light_grey
        style = theme

    colors = [PWE_skin, PWE_grey, black, vic_teal,
              PWE_blue, PWE_ig_light_grey, PWE_ig_dark_grey]

    if marker_color == None:
        marker_color = vic_teal

    chart_start, chart_end, auto_start, auto_end = get_chart_dates(
        df=df, start_date=None, end_date=None, utc=True, auto_start=auto_start, auto_end=auto_end)

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_line_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_line_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_line_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    if columns is None:
        if annots == None:
            plt_int = df.iplot(asFigure=asFigure, kind=kind, mode=mode, showlegend=showlegend, legend=legend, rangeslider=False,
                               xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                               asPlot=asPlot, filename=f'./{f_name}', yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                  x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})
        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                           anntextangle=-anntextangle, arrowlen=arrowlen)

            plt_int = df.iplot(asFigure=asFigure, kind=kind, mode=mode, showlegend=showlegend, legend=legend, rangeslider=False,
                               xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                               asPlot=asPlot, filename=f'./{f_name}', yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                               rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                  bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                  x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end],
                               connectgaps=connectgaps, annotations=ans, anntextangle=anntextangle,
                               title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    else:
        if annots == None:
            plt_int = df[columns].iplot(asFigure=asFigure, kind=kind, mode=mode, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=[PWE_skin, PWE_grey], fontfamily='Roboto',
                                        theme=theme, asPlot=asPlot, filename=f'.{f_name}', yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end], connectgaps=connectgaps,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

        else:

            ans = cf.tools.get_annotations(df=df[annot_col], annotations=annots, annot_col=annot_col,
                                           fontsize=fontsize, yanchor='auto', yref="y", showarrow=True,
                                           arrowhead=arrowhead, arrowcolor=arrowcolor, fontcolor=fontcolor,
                                           anntextangle=-anntextangle, arrowlen=arrowlen)

            plt_int = df[columns].iplot(asFigure=asFigure, kind=kind, mode=mode, showlegend=showlegend, legend=legend, rangeslider=False,
                                        xTitle='Date', yTitle=yTitle, colors=colors, fontfamily='Roboto', theme=theme,
                                        asPlot=asPlot, filename=f'./{f_name}', yaxis_tickformat=yaxis_tickformat, xaxis_tickformat=xaxis_tickformat,
                                        rangeselector=dict(steps=['Reset', '3Y', '2Y', '1Y', 'YTD', '6M', '1M'],
                                                           bgcolor=(PWE_skin, .2), fontsize=range_fontsize, fontfamily='Roboto',
                                                           x=-0.025, y=1, visible=True), xrange=[auto_start, auto_end],
                                        connectgaps=connectgaps, annotations=ans, anntextangle=anntextangle,
                                        title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    plt_int = plt_int.add_trace(go.Scatter(x=marker_x, y=marker_y, mode='markers',
                                name=marker_name, marker_color=marker_color, marker_size=marker_size))

    plotly.offline.plot(plt_int, filename=f'./{f_name}.html')

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file


def custom_html(f_name, string_from, string_to):
    """
    Manually append HTML code for a chart or table.
    string_from :   The string of code to be replaced.
    string_to   :   The string of code to append.
    """
    print(f_name)
    cwd = os.getcwd()
    file_path_str = f'{cwd}{f_name}'
    file_path = f'{file_path_str}.html'

    prefix = cwd
    relative_path = f'/{os.path.relpath(file_path,prefix)}'

    local_path_str = f'{f_name}'
    local_file_path = f'/{local_path_str}.html'
    unf_link = f'http://localhost:8888/view{relative_path}'

    text_wrapper = open(file_path, encoding="utf-8")
    html_text = text_wrapper.read()
    # print(html_text)

    name = f_name
    file = open(file_path).read()

    replaced_txt = file.replace(string_from, string_to)

    output_html = f"{file_path_str}_PWE.html"
    writer = open(output_html, 'w')
    writer.write(replaced_txt)
    writer.close()

    output_html_path = f"{cwd}{f_name}"
    abs_path = f'/{os.path.abspath(output_html)}'
    chart_html = f"http://localhost:8888/view{local_path_str}"
    chart_file = f"file:///{abs_path}"

    webbrowser.open_new_tab(chart_file)

    return chart_html, chart_file


def add_range_selector(layout, axis_name='xaxis', ranges=None, default=None):
    """Add a rangeselector to the layout if it doesn't already have one.

    This code is only needed if switching to Plotly from Cufflinks.

    :param ranges: which ranges to add, e.g. ['3m', '1y', 'ytd']
    :param default_range: which range to choose as the default, e.g. '3m'
    """
    axis = layout.setdefault(axis_name, dict())
    axis.setdefault('type', 'date')
    axis.setdefault('rangeslider', dict())
    if ranges is None:
        ranges = ['1m', '6m', 'ytd', '1y', 'all']
    re_split = re.compile('(\d+)')

    def range_split(range):
        split = re.split(re_split, range)
        assert len(split) == 3
        return (int(split[1]), split[2])
    # plotly understands m, but not d or y!
    step_map = dict(d='day', m='month', y='year')

    def make_button(range):
        range = range.lower()
        if range == 'all':
            return dict(step='all')
        elif range == 'ytd':
            return dict(count=1,
                        label='YTD',
                        step='year',
                        stepmode='todate')
        else:
            (count, step) = range_split(range)
            step = step_map.get(step, step)
            return dict(count=count,
                        label=range,
                        step=step,
                        stepmode='backward')
    axis.setdefault('rangeselector', dict(
        buttons=[make_button(r) for r in ranges]))
    if default is not None and default != 'all':
        end_date = datetime.datetime.today()
        if default.lower() == 'ytd':
            start_date = datetime.date(end_date.year, 1, 1)
        else:
            (count, step) = range_split(default)
            step = step_map[step] + 's'  # relativedelta needs plurals
            start_date = (
                end_date - dateutil.relativedelta.relativedelta(**{step: count}))
        axis.setdefault('range', [start_date, end_date])


def calc_interval(df):
    """Calculate the interval between timestamps for chart labels."""
    if df.index[1] - df.index[0] == timedelta(days=1):
        chart_interval = "Daily"
        interval = "daily"
    if df.index[1] - df.index[0] == timedelta(hours=1):
        chart_interval = "Hourly"
        interval = "hourly"
    if df.index[1] - df.index[0] == timedelta(minutes=1):
        chart_interval = "Per Minute"
        interval = "minutes"
    if df.index[1] - df.index[0] == timedelta(seconds=1):
        chart_interval = "Per Second"
        interval = "seconds"
    if df.index[1] - df.index[0] == timedelta(weeks=1):
        chart_interval = "Weekly"
        interval = "weekly"
    if timedelta(days=32) >= df.index[1] - df.index[0] >= timedelta(days=27):
        chart_interval = "Monthly"
        interval = "monthly"
    if timedelta(days=182) >= df.index[1] - df.index[0] >= timedelta(days=90):
        chart_interval = "Semi-Annual"
        interval = "semi-annual"
    if timedelta(days=360) >= df.index[1] - df.index[0] >= timedelta(days=182):
        chart_interval = "Annual"
        interval = "annual"
    return chart_interval, interval


def pwe_heatmap(df, start_date=None, end_date=None, title=None, ticker=None, yTitle=None, xTitle=None, asPlot=False,
                asFigure=True, theme='white', showlegend=False, decimals=2, textangle=0, file_tag=None,
                interval='Daily', linecolor=None, title_dates=True, colorscale=None,
                title_time=True, chart_ticker=True, top_margin=0.9, spacing=0.08, title_x=0.5, title_y=0.933):
    """

    Plots an interactive heatmap formatted in the PWE style.

    center_scale : float
        Centers the colorscale at a specific value
        Automatically sets the (zmin,zmax) values
    zmin : float
        Defines the minimum range for the z values. 
        This affects the range for the colorscale
    zmax : float
        Defines the maximum range for the z values. 
        This affects the range for the colorscale

    See: https://github.com/santosjorge/cufflinks/blob/master/cufflinks/plotlytools.py
    """
    dark = ("henanigans", "solar", "space")
    if str(theme) in dark:
        fontcolor = 'henanigans_light1'
        arrowcolor = 'henanigans_light1'
        style = 'dark'
    else:
        fontcolor = PWE_ig_light_grey
        arrowcolor = PWE_ig_dark_grey
        style = theme

    if linecolor == None or linecolor == 'PWE_grey':
        linecolor = PWE_grey
    elif linecolor == 'PWE':
        linecolor = PWE_skin

    # colors = [PWE_skin, PWE_grey]
    if not colorscale:
        colorscale=["rgb(100, 100, 111)", "rgb(255, 255, 255)", 'rgb(220, 187, 166)',]
        # colorscale=[[0, "rgb(100, 100, 111)"],
        #             [0.0555555555555556, "rgb(106, 104, 116)"],
        #             [0.1111111111111111, "rgb(112,108,120)"],
        #             [0.1666666666666667, "rgb(118,111,125)"],
        #             [0.2222222222222222, "rgb(125,115,129)"],
        #             [0.2777777777777778, "rgb(132,119,133)"],
        #             [0.3333333333333333, "rgb(139,123,136)"],
        #             [0.3888888888888889, "rgb(146,127,139)"],
        #             [0.4444444444444444, "rgb(152,131,142)"],
        #             [0.4999999999999999, "rgb(159,135,145)"],
        #             [0.5555555555555556, "rgb(166,139,148)"],
        #             [0.6180339887498948, "rgb(173,143,150)"],
        #             [0.6666666666666666, "rgb(179,147,152)"],
        #             [0.7222222222222215, "rgb(186,151,154)"],
        #             [0.7777777777777778, "rgb(192,156,156)"],
        #             [0.8333333333333333, "rgb(197,161,157)"],
        #             [0.8888888888888888, "rgb(203,166,159)"],
        #             [0.9194444444444444, "rgb(208,171,161)"],
        #             [0.95, "rgb(212,176,162)"],
        #             [0.975, "rgb(216,181,164)"],
        #             [1.0, "rgb(220,187,166)"]]

    sdate, edate, chart_dates = chart_file_dates(
        df, start_date, end_date, time=title_time)

    if xTitle == None:
        xTitle = f'{interval} Return Correlation Matrix'

    check_folder('charts')

    tkr = ticker.replace('/', '_')

    if file_tag == None:

        if hasattr(df, 'name'):
            df_name = df.name.replace('/', '_').replace(' ', '_')
            f_name = f'/charts/{tkr}_{df_name}_{sdate}-{edate}_heatmap_{style}'
        else:
            f_name = f'/charts/{tkr}_{sdate}-{edate}_heatmap_{style}'

    else:
        f_name = f'/charts/{tkr}_{file_tag}_{sdate}-{edate}_heatmap_{style}'

    chart_title = get_chart_title(
        title, chart_ticker, title_dates, ticker, chart_dates)

    plt_int = df.iplot(kind="heatmap", theme=theme, showlegend=showlegend, legend='top', rangeslider=False,
                       xTitle=xTitle, yTitle=yTitle, colorscale=colorscale, fontfamily='Roboto', asPlot=asPlot, asFigure=asFigure,
                       filename=f'./{f_name}', hoverinfo="text", textangle=textangle,
                       title={'text': f'{chart_title}', 'y': title_y, 'x': title_x, 'xanchor': 'center', 'yanchor': 'top'})

    # chart_html, chart_file = pwe_format(f_name)

    return plt_int  # chart_html, chart_file
