import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
from datetime import datetime
from pytz import timezone
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots


# specify Time zone
tz = timezone('US/Eastern')

styles = [dbc.themes.GRID]

app = Dash(name = __name__, external_stylesheets=styles)

timeNow = datetime.now(tz)


def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig

app.layout = html.Div([
    html.H1("Live Dashboard", style={'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.DatePickerSingle(
        id='date-picker',
        display_format='YYYY-MM-DD',
        date= timeNow.date()
    ),
    dcc.Graph(id="sub_graphs",figure = blank_fig()),
    ])
COLORS = [
    "#1e88e5",
    "#7cb342",
    "#fbc02d",
    "#ab47bc",
]

account_tables = ['yyyy_mm_dd_a', 'yyyy_mm_dd_b', 'yyyy_mm_dd_c', 'yyyy_mm_dd_d']
account_names = ['Account_a', 'Account_b', 'Account_c', 'Account_d']
    
# method to create all line graphs
def createPlot(y_axis_col_name, date_value, legandStatus):
    #Mysql Connection with database
    connection = mysql.connector.connect(host='localhost',
                                    database='dashboard',
                                    user='root',
                                    password='')
    connection.autocommit = True
    cursor = connection.cursor()
    dfs = []
    for account_table in account_tables:
        cursor.execute('''SELECT entry_id, {0}, ts FROM {1} Where DATE(ts) = '{2}' 
                        AND TIME(ts) >= '04:00:00' AND TIME(ts) <='20:00:00'
                        ORDER BY entry_id ASC;'''.format(y_axis_col_name, account_table, str(date_value)))
        plot_data = cursor.fetchall()
        df = pd.DataFrame(plot_data, columns= ['entry_id', y_axis_col_name, 'ts'])
        dfs.append(df)
    data = []
    for df in dfs:
        if len(df) != 0:
            trace = go.Scatter(
            x= df['ts'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist(),
            y= df[y_axis_col_name].tolist(),
            textposition="top center",
            mode='lines',
            name=account_names[len(data)],
            marker=dict(color=COLORS[len(data)]),
            legendgroup=account_names[len(data)],
            showlegend=legandStatus
            )
            data.append(trace)
        else:
            trace = go.Scatter(
            x= [str(date_value) + ' 04:00:00'],
            y= [0],
            textposition="top center",
            mode='lines',
            name=account_names[len(data)],
            marker=dict(color=COLORS[len(data)]),
            showlegend=legandStatus
            )
            data.append(trace)
    figure = go.Figure(data=data)
    if str(date_value) != str(timeNow.date()):
        max_intervals = 0
    else:
        max_intervals = -1
    cursor.close()
    connection.close()
    return figure, max_intervals

y_axis_names = ['PL Last Equity', 'Cash Last Equity', 'Daytrading Buying Power Last Equity', 'Initial Margin Last Equity',
'Last Maintenance Margin Last Equity', 'Long Market Value Last Equity', 'Maintenance Margin Last Equity', 'Portfolio Value Last Equity',
'Regt Buying Power Last Equity', 'Short Market Value Last Equity']
y_axis_col_names = ['pl_last_equity' , 'cash_last_equity', 'daytrading_buying_power_last_equity', 'initial_margin_last_equity'
, 'last_maintenance_margin_last_equity','long_market_value_last_equity', 'maintenance_margin_last_equity',
'portfolio_value_last_equity', 'regt_buying_power_last_equity', 'short_market_value_last_equity']
# Callback function for all subplots
@app.callback(
    [Output('sub_graphs', 'figure'),
    Output('interval-component', 'max_intervals')],
    [Input('interval-component', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig(n_intervals, date_value):
    # Initialize figure with subplots
    # merge all plots in subplots
    plotTitles = [s + ' Vs. Time' for s in y_axis_names]

    row_count = 1
    col_count = 0

    all_figures = make_subplots(
        rows=4, cols=3,
        specs=[[{}, {}, {}],
           [{}, {}, {}],
           [{}, {}, {}],
           [{"colspan": 3}, {}, {}]], 
            vertical_spacing = 0.10,
            horizontal_spacing=0.05,
            subplot_titles=plotTitles
        )
        
    subPlots_counter = 1
    for y_axis_col_name in y_axis_col_names:
        if subPlots_counter == 10:
            legandStatus = True
        else:
            legandStatus = False

        figure, max_intervals  = createPlot(y_axis_col_name, date_value, legandStatus)
        subPlots_counter+=1

        # subplots settings
        col_count+=1
        if col_count > 3:
            col_count = 1
            row_count+=1
        if row_count > 4:
            row_count=1
        
        for t in figure.data:
            all_figures.append_trace(t, row=row_count, col=col_count)
        
    all_figures.update_xaxes(
        type = 'date',
        range = [str(date_value) + ' 04:00:00', str(date_value) + ' 20:00:00'],
        autorange = False,
        dtick = 3600000.0 * 1,  #1 hour in milliseconds
        tickformat = "%X",
        showgrid = False,)
    all_figures.update_yaxes(
        type= 'linear',
        autorange= True,
        showgrid= False)

    all_figures.add_vline(
        x=str(date_value) + ' 09:30:00', line_width=3, line_dash="dash", 
        line_color="gray"
    )
    all_figures.add_vline(
        x=str(date_value) + ' 16:00:00', line_width=3, line_dash="dash", 
        line_color="gray"
    )
    # set y margin of title to each subplot 
    for annotation in all_figures['layout']['annotations']: 
        annotation['yshift']=15

    all_figures.update_layout(height=1400, width=1500,  uirevision= 'data', hovermode="closest",
    font= dict(
    size=12,
    color="#000000"
    ), 
    margin={"l": 0, "b": 45, "t": 80, "r": 0},
    )
    return all_figures, max_intervals


if __name__ == "__main__":
        app.run_server(debug=True, port=8050)
    