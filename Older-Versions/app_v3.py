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
import numpy as np


# specify Time zone
tz = timezone('US/Eastern')

styles = [dbc.themes.GRID]

app = Dash(name = __name__, external_stylesheets=styles)

timeNow = datetime.now(tz)


# just a function to print empty graph by default
def blank_fig():
    fig = go.Figure(go.Scatter(x=[], y = []))
    fig.update_layout(template = None)
    fig.update_xaxes(showgrid = False, showticklabels = False, zeroline=False)
    fig.update_yaxes(showgrid = False, showticklabels = False, zeroline=False)
    return fig

dropDown_values = ['Account_a', 'Account_b', 'Account_c', 'Account_d']


# ------------------ Layout Settings Start --------------------
app.layout = html.Div([
    html.H1("Live Dashboard", style={'textAlign': 'center'}),
    dbc.Row([
        dbc.Col([
            html.H3("Time Series Graphs", style={'textAlign': 'center'}),
            html.Div(
                [
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
                ]
            )
        ], width=8),
        dbc.Col([
        html.Div(
            [
                html.H3("Tree Maps", style={'textAlign': 'center'}),
                dcc.Interval(
                id='treemap-interval-component',
                interval=30*1000, # in milliseconds
                n_intervals=0,
                max_intervals=-1
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.RadioItems(id="radioBtn",
                                options= ['Live', 'Still'],
                                value = 'Live', inline=True)
                                ,width=4, align='start'),
                        dbc.Col(dcc.Dropdown(id="dropdown",
                            options=dropDown_values,
                            value = dropDown_values[0],
                            clearable=False,
                            searchable=False,
                            placeholder="Select an Account",
                            ), width=4, align='center'),
                        dbc.Col(dcc.DatePickerSingle(
                                id='treemap_date-picker',
                                display_format='YYYY-MM-DD',
                                date= timeNow.date()
                                ), width=4, align= 'end'),
                    ],
                ),
                dbc.Row(
                    [
                        dbc.Col(dcc.Slider(4, 20, 1,
                            value=timeNow.hour,
                            id='hour-slider',
                            marks=None,
                            tooltip={"placement": "bottom", "always_visible": True}
                            ), width=4),
                        dbc.Col(dcc.Slider(0, 59, 1,
                                value= timeNow.minute,
                                id='minute-slider',
                                marks=None,
                                tooltip={"placement": "bottom", "always_visible": True}
                                ), width=8),
                    ],
                ),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="tree_map_1",figure = blank_fig()), width=12),
                ]
                ),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="tree_map_2",figure = blank_fig()), width=12),
                ]
                ),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="tree_map_3",figure = blank_fig()), width=12),
                ]
                ),
                dbc.Row(
                [
                    dbc.Col(dcc.Graph(id="tree_map_4",figure = blank_fig()), width=12),
                ]
                ),
            ]
        )
        ], width=4),
    ]),
    ])
# ------------------ Layout Settings End --------------------

# Line colors on each line graph
COLORS = [
    "#1e88e5",
    "#7cb342",
    "#fbc02d",
    "#ab47bc",
]

account_tables = ['yyyy_mm_dd_a', 'yyyy_mm_dd_b', 'yyyy_mm_dd_c', 'yyyy_mm_dd_d']
account_names = ['Account_a', 'Account_b', 'Account_c', 'Account_d']

position_tables = ['stocks_account_a', 'stocks_account_b', 'stocks_account_c', 'stocks_account_d']
    
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
    # set y margin of title from each subplot 
    for annotation in all_figures['layout']['annotations']: 
        annotation['yshift']=15

    all_figures.update_layout(height=1400,  uirevision= 'data', hovermode="closest",
    font= dict(
    size=10,
    color="#000000"
    ),
    margin={"l": 0, "b": 45, "t": 80, "r": 0},
    )
    all_figures.update_annotations(font_size=13)
    return all_figures, max_intervals


# Callback function for tree map
@app.callback(
    [Output('tree_map_1', 'figure'),
    Output('tree_map_2', 'figure'),
    Output('tree_map_3', 'figure'),
    Output('tree_map_4', 'figure'),
    Output('treemap-interval-component', 'max_intervals'),
    Output('hour-slider', 'value'),
    Output('minute-slider', 'value'),
    Output('treemap_date-picker', 'date')],
    [Input('treemap-interval-component', "n_intervals"),
    Input('treemap_date-picker', 'date'),
    Input('dropdown', 'value'),
    Input('hour-slider', 'value'),
    Input('minute-slider', 'value'),
    Input('radioBtn', 'value')]
)
def plotTreeMap(n_intervals, date_value, dropdown_value, hour_value, minute_value, mode):
    #Mysql Connection with database
    connection = mysql.connector.connect(host='localhost',
                                    database='dashboard',
                                    user='root',
                                    password='')
    connection.autocommit = True
    cursor = connection.cursor()

    # determine the table name in the database from the Accounts from dropdown
    current_position_table = ''
    counter = 0
    for account_name in account_names:
        if dropdown_value == account_name:
            current_position_table =  position_tables[counter]
            break
        counter+=1
    map_trace = []
    try:
        query =  '''Select entry_id From {0} Where DATE(ts) = '{1}' AND HOUR(ts) = '{2}' AND MINUTE(ts) = '{3}'
                    ORDER BY entry_id DESC LIMIT 1;
                    '''.format(current_position_table , str(date_value), str(hour_value), str(minute_value))
        cursor.execute(query)
        stocks_id = cursor.fetchone()
        # getThat id and now use this id in next query
        cursor.execute('''Select entry_id, symbol, open_pl, position_percentage, open_pl_percentage, parent 
                        From {0} Where entry_id = '{1}';'''.format(current_position_table, stocks_id[0]))

        latest_entries = cursor.fetchall()
        ret = pd.DataFrame(latest_entries, columns= ['entry_id', 'symbol', 'open_pl', 'position_percentage', 'open_pl_percentage'
        , 'parent'])
        red_gradient_scale = [
            [0.0, 'rgb(186, 37, 37)'],

            [0.1, 'rgb(186, 37, 37)'],
            [0.2, 'rgb(213, 62, 62)'],

            [0.3, 'rgb(213, 62, 62)'],
            [0.4, 'rgb(213, 62, 62)'],

            [0.5, 'rgb(238, 91, 91)'],
            [0.6, 'rgb(238, 91, 91)'],

            [0.7, 'rgb(238, 91, 91)'],
            [0.8, 'rgb(255, 121, 121)'],

            [0.9, 'rgb(255, 121, 121)'],
            [1.0, 'rgb(255, 121, 121)']
        ]
        green_gradient_scale = [
            [0.0, 'rgb(49, 158, 28)'],

            [0.1, 'rgb(49, 158, 28)'],
            [0.2, 'rgb(63, 181, 39)'],

            [0.3, 'rgb(63, 181, 39)'],
            [0.4, 'rgb(63, 181, 39)'],

            [0.5, 'rgb(85, 211, 60)'],
            [0.6, 'rgb(85, 211, 60)'],

            [0.7, 'rgb(85, 211, 60)'],
            [0.8, 'rgb(104, 247, 75)'],

            [0.9, 'rgb(104, 247, 75)'],
            [1.0, 'rgb(104, 247, 75)']
        ]

        # get the data for all categories
        categ_1_df = ret.loc[(ret['open_pl'] >= 0.0) & (ret['position_percentage'] >= 0.0)]
        categ_2_df = ret.loc[(ret['open_pl'] < 0.0) & (ret['position_percentage'] >= 0.0)]
        categ_3_df = ret.loc[(ret['open_pl'] >= 0.0) & (ret['position_percentage'] < 0.0)]
        categ_4_df = ret.loc[(ret['open_pl'] < 0.0) & (ret['position_percentage'] < 0.0)]

        maps_data = [categ_1_df, categ_2_df, categ_3_df, categ_4_df]
        maps_counter = 1
        for map_data in maps_data:
            if maps_counter == 1:
                 color = ['#58e658', '#58e658']
            elif maps_counter == 2:
                color = ['#58e658', '#fd2f2f']
            elif maps_counter == 3:
                color = ['#fd2f2f', '#58e658']
            else:
                color = ['#fd2f2f', '#fd2f2f']

            map_data.loc[: , 'parent'] = str('Position=<b style="color:{0}">{1:.0f}%</b>, Open PL= <b style="color:{2}">${3:.0f}</b>').format(color[0], 
            map_data['position_percentage'].apply(abs).sum()*100, color[1], map_data['open_pl'].sum())
            # select color scale for different maps
            if maps_counter == 1 or  maps_counter == 3:
                color_scale = green_gradient_scale
            elif maps_counter == 2 or maps_counter == 4:
                color_scale = red_gradient_scale

            trace = go.Treemap(
                branchvalues = 'total',
                labels = map_data['symbol'],
                parents = map_data['parent'],
                values =  map_data['position_percentage'].apply(abs),
                root_color="lightgrey",
                marker=dict(
                colors=map_data['open_pl_percentage'].apply(abs),
                colorscale=color_scale,
                ),
                customdata = np.column_stack([map_data['position_percentage'] * 100, map_data['open_pl']]),
                hovertemplate='<b>%{label} </b> <br>%{customdata[0]:.4f}%<br>$%{customdata[1]}',
                texttemplate = "<b>%{label}</b><br>%{customdata[0]:.4f}%<br>$%{customdata[1]}"
            )
            fig = go.Figure(data=trace)
            postion_sum = map_data['position_percentage'].apply(abs).sum()
            postion_sum*=100*5
            fig.update_layout(height = 27 + int(postion_sum), uirevision= 'data', hovermode="closest",
            font= dict(
            size=12,
            color="#000000"
            ),
            margin={"l": 0, "b": 0, "t": 0, "r": 0},
            )
            fig.data[0]['textfont']['color'] = "white"
            map_trace.append(fig)
            maps_counter+=1

    except Exception as e:
        print('Failed to Draw Tree Plot: {}'.format(e))
        trace = go.Treemap(
        labels = [dropdown_value],
        parents = [''],
        values =  [0],
        root_color="lightgrey",
        )
        fig = go.Figure(trace)
        fig.update_layout(height = 250, uirevision= 'data', hovermode="closest",
            margin={"l": 0, "b": 0, "t": 35, "r": 0},
            )
        for n in range(0, 4):
            map_trace.append(fig)
    cursor.close()
    connection.close()
    # settings for Live and Still maps
    hour_at = 0
    minute_at = 0
    live_status = -1 # true
    day_at = ''
    if mode == 'Live':
        timeNow = datetime.now(tz)
        hour_at = timeNow.hour
        minute_at = timeNow.minute
        day_at = timeNow.strftime('%Y-%m-%d')
    else:
        hour_at = hour_value
        minute_at = minute_value
        live_status = 0
        day_at = date_value

    return map_trace[0], map_trace[1], map_trace[2], map_trace[3], live_status, hour_at, minute_at, day_at



if __name__ == "__main__":
        app.run_server(debug=True, port=8050)
    