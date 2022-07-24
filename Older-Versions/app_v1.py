import mysql.connector
from mysql.connector import Error
import pandas as pd
import plotly.graph_objects as go
from dash import Dash, dcc, html
import dash_auth
from dash.dependencies import Input, Output
from datetime import datetime
from pytz import timezone
import flask
import dash_bootstrap_components as dbc


# specify Time zone
tz = timezone('US/Eastern')

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', dbc.themes.GRID]

server = flask.Flask(__name__)
app = Dash(__name__, external_stylesheets=external_stylesheets, server=server)

VALID_USERNAME_PASSWORD_PAIRS = {
    'hello': 'tyler'
}
auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS
)

timeNow = datetime.now(tz)
app.layout = html.Div([
    html.H1("Live Dashboard", style={'textAlign': 'center'}),
    dcc.Interval(
        id='interval-component_1',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_2',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_3',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_4',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_5',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_6',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_7',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_8',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_9',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.Interval(
        id='interval-component_10',
        interval=6*1000, # in milliseconds
        n_intervals=0,
        max_intervals=-1
        ),
    dcc.DatePickerSingle(
        id='date-picker',
        display_format='YYYY-MM-DD',
        date= timeNow.date()
    ),
    html.Div(
        [
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='plot_1')], width=12),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='plot_2', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_3', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_4', style={'height': '40vh'})], width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='plot_5', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_6', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_7', style={'height': '40vh'})], width=4),
            ]
        ),
        dbc.Row(
            [
                dbc.Col([dcc.Graph(id='plot_8', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_9', style={'height': '40vh'})], width=4),
                dbc.Col([dcc.Graph(id='plot_10', style={'height': '40vh'})], width=4),
            ]
        ),
        ]
    )
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
def createPlot(y_axis_name, y_axis_col_name, date_value):
    #Mysql Connection with database
    connection = mysql.connector.connect(host='localhost',
                                    database='dashboard',
                                    user='root',
                                    password='hfy5676%%TY6h%$#gU7')
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
            )
            data.append(trace)
    layout = go.Layout(
    xaxis={"title": "Time",
            'type': 'date',
            'range': [str(date_value) + ' 04:00:00', str(date_value) + ' 20:00:00'],
            "autorange": False,
            'dtick': 3600000.0 * 1,  #1 hour in milliseconds
            'tickformat':"%X",
            'showgrid': False,
            },
    yaxis={"title": y_axis_name,
            'type': 'linear',
            "autorange": True,
            'showgrid': False},
    margin={"l": 5, "b": 50, "t": 50, "r": 5},
    uirevision= 'data',
    hovermode="closest",
    title= y_axis_name + ' Vs. Time',
    font= dict(
        size=11,
        color="#000000"
        )
    )
    figure = go.Figure(data=data, layout=layout)
    figure.add_vline(
        x=str(date_value) + ' 09:30:00', line_width=3, line_dash="dash", 
        line_color="gray"
    )
    figure.add_vline(
        x=str(date_value) + ' 16:00:00', line_width=3, line_dash="dash", 
        line_color="gray"
    )
    if str(date_value) != str(timeNow.date()):
        max_intervals = 0
    else:
        max_intervals = -1
    cursor.close()
    connection.close()
    return figure, max_intervals


# Callback function for figure 1
@app.callback(
    [Output('plot_1', 'figure'),
    Output('interval-component_1', 'max_intervals')],
    [Input('interval-component_1', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_1(n_intervals, date_value):
    y_axis_name = 'PL Last Equity' # set plot's Y axis name
    y_axis_col_name = 'pl_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 2
@app.callback(
    [Output('plot_2', 'figure'),
    Output('interval-component_2', 'max_intervals')],
    [Input('interval-component_2', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_2(n_intervals, date_value):
    y_axis_name = 'Cash Last Equity' # set plot's Y axis name
    y_axis_col_name = 'cash_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 3
@app.callback(
    [Output('plot_3', 'figure'),
    Output('interval-component_3', 'max_intervals')],
    [Input('interval-component_3', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_3(n_intervals, date_value):
    y_axis_name = 'Daytrading Buying Power Last Equity' # set plot's Y axis name
    y_axis_col_name = 'daytrading_buying_power_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 4
@app.callback(
    [Output('plot_4', 'figure'),
    Output('interval-component_4', 'max_intervals')],
    [Input('interval-component_4', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_4(n_intervals, date_value):
    y_axis_name = 'Initial Margin Last Equity' # set plot's Y axis name
    y_axis_col_name = 'initial_margin_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 5
@app.callback(
    [Output('plot_5', 'figure'),
    Output('interval-component_5', 'max_intervals')],
    [Input('interval-component_5', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_5(n_intervals, date_value):
    y_axis_name = 'Last Maintenance Margin Last Equity' # set plot's Y axis name
    y_axis_col_name = 'last_maintenance_margin_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 6
@app.callback(
    [Output('plot_6', 'figure'),
    Output('interval-component_6', 'max_intervals')],
    [Input('interval-component_6', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_6(n_intervals, date_value):
    y_axis_name = 'Long Market Value Last Equity' # set plot's Y axis name
    y_axis_col_name = 'long_market_value_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 7
@app.callback(
    [Output('plot_7', 'figure'),
    Output('interval-component_7', 'max_intervals')],
    [Input('interval-component_7', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_7(n_intervals, date_value):
    y_axis_name = 'Maintenance Margin Last Equity' # set plot's Y axis name
    y_axis_col_name = 'maintenance_margin_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 8
@app.callback(
    [Output('plot_8', 'figure'),
    Output('interval-component_8', 'max_intervals')],
    [Input('interval-component_8', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_8(n_intervals, date_value):
    y_axis_name = 'Portfolio Value Last Equity' # set plot's Y axis name
    y_axis_col_name = 'portfolio_value_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 9
@app.callback(
    [Output('plot_9', 'figure'),
    Output('interval-component_9', 'max_intervals')],
    [Input('interval-component_9', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_9(n_intervals, date_value):
    y_axis_name = 'Regt Buying Power Last Equity' # set plot's Y axis name
    y_axis_col_name = 'regt_buying_power_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

# Callback function for figure 10
@app.callback(
    [Output('plot_10', 'figure'),
    Output('interval-component_10', 'max_intervals')],
    [Input('interval-component_10', "n_intervals"),
    Input('date-picker', 'date')]
)
def fig_10(n_intervals, date_value):
    y_axis_name = 'Short Market Value Last Equity' # set plot's Y axis name
    y_axis_col_name = 'short_market_value_last_equity' # set the name of the column in database
    figure, max_intervals  = createPlot(y_axis_name, y_axis_col_name, date_value)
    return figure, max_intervals

if __name__ == "__main__":
    app.run_server()