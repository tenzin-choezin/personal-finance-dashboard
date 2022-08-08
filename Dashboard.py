import pandas as pd
import numpy as np 
import plotly.express as px
import plotly.graph_objects as go
import dash
from dash import Dash, dcc, html, Input, Output, dash_table, State
from datetime import date, datetime, timedelta

pd.options.mode.chained_assignment = None


# UTILITY FUNCTIONS BEGIN HERE
def clean_data(initial_csv):
    # Input -> string format of csv location
    df = pd.read_csv(initial_csv)
    df = df.drop(columns = ['Memo'], axis = 1)
    new_columns = ['transaction_date', 'post_date', 'description', 'category', 'type', 'amount']
    df.columns = new_columns
    
    df['transaction_date'] = pd.to_datetime(df['transaction_date'])
    df['post_date'] = pd.to_datetime(df['post_date'])
    
    # REMOVING RETURNS AND CONVERTING NEGATIVE AMOUNTS TO POSITIVE TO REPRESENT TRANSACTIONS
    df = df[df['amount'] <= 0]
    df['amount'] = df['amount'] * (-1)
    
    df['transaction_year'] = df['transaction_date'].dt.year
    df['transaction_month'] = df['transaction_date'].dt.month
    df['month_name'] = df['transaction_date'].dt.month_name()
    
    df = df.sort_values('transaction_date')
    # Output -> final cleaned df that we pass into our dash application
    return df


# GETTING DATA 
flex_df = clean_data('flex.csv')
unlimited_df =  clean_data('unlimited.csv')
transactions_df = pd.concat([flex_df, unlimited_df], ignore_index = True)
months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = pd.unique(transactions_df['transaction_year']).tolist()
categories = pd.unique(transactions_df['category'])


app = dash.Dash()
server = app.server
app.title = 'Personal Finance Dashboard'



app.layout = html.Div(
    id = 'root',
    children = [
        
        html.Div(
            id = 'Header',
            children = [
                html.H4('Personal Finances Dashboard',
                        style = {'fontSize' : 55, 'font-family' : 'monospace', 'font-weight' : 'bold', 'textAlign' : 'center', 'marginTop' : 15, 'marginBottom' : 15}
                       ),
                
                html.P(
                    children = 'This dashboard is presented by Tenzin Choezin. It is a general puprose tool built for tracking his spending habits.',
                    style = {'fontSize' : 15, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black'}
                )
            ]
        ),
        
        
        html.Div(
            id = 'piegraph',
            children = [
                html.H4('Spending by Category Breakdown', 
                        style = {'fontSize' : 30, 'font-family' : 'monospace', 'font-weight' : 'bold', 'textAlign' : 'center', 'marginTop' : 45, 'marginBottom' : 5}),
  
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a year',
                                    style = {'fontSize' : 15, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.Dropdown(
                                    id = 'pie-year',
                                    options = years,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace'}
                                )
                            ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '15px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a month',
                                    style = {'fontSize' : 15, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.Dropdown(
                                    id = 'pie-month',
                                    options = months,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace'}
                                )
                            ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '15px', 'margin-right' : '15px'}
                        )
                    ], style=dict(display='flex'), className = 'nine columns'
                ),
                
                dcc.Graph(id = 'pie-chart')
                
            ]
        ),
        
        
        html.Div(
            id = 'linegraph',
            children = [
                html.H4('Spending Patterns by Month', 
                        style = {'fontSize' : 30, 'font-family' : 'monospace', 'font-weight' : 'bold', 'textAlign' : 'center', 'marginTop' : 45, 'marginBottom' : 5}),
  
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a start date and end date',
                                    style = {'fontSize' : 15, 'font-family' : 'monospace', 'textAlign' : 'left', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.DatePickerRange(
                                    id = 'date_range',
                                    min_date_allowed=date(2020, 5, 1),
                                    start_date_placeholder_text="Start Period",
                                    end_date_placeholder_text="End Period",
                                    calendar_orientation='horizontal',
                                    clearable = True,
                                    style = {'font-family' : 'monospace', 'textAlign' : 'center'}
                                ),
                            ], style={'display': 'inline-block', 'width': '30%', 'margin-left': '350px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a category',
                                    style = {'fontSize' : 15, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 10}
                                ),
                                dcc.Dropdown(
                                    id = 'category',
                                    options = categories,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace'}
                                )
                            ], style={'display': 'inline-block', 'width': '70%', 'margin-left': '10px', 'margin-right' : '350px'}
                        )
                    ], style=dict(display='flex')
                ),
                
                dcc.Graph(id = 'line-chart')
  
            ]
        )  
    ]
)



# CALLBACKS BEGIN HERE
@app.callback(
    Output('pie-chart', 'figure'),
    [Input('pie-year', 'value'),
     Input('pie-month', 'value')
    ]
)
def piechart_update(year, month):
    df = transactions_df
    year_str = ''
    month_str = ''
    if (month is None) and (year is None):
        pass
    elif (month is None) and (year is not None):
        df = df[df['transaction_year'] == year]
        year_str = ' ' + str(year)
    elif (year is None) and (month is not None):
        df = df[df['month_name'] == month]
        month_str = ' ' + str(month)
    elif month and year:
        df = df[(df['transaction_year'] == year) & (df['month_name'] == month)]
        year_str = ' ' + str(year)
        month_str = ' ' + str(month)
    fig = px.pie(df, values = df['amount'], names = df['category'], hole = 0.2)
    fig.update_layout(title = 'Spending by Category during:' + month_str + year_str)
    return fig



@app.callback(
    Output('line-chart', 'figure'),
    [Input('date_range', 'start_date'),
     Input('date_range', 'end_date'),
     Input('category', 'value')
    ]
)
def linechart_update(start, end, category):
    df = transactions_df.sort_values('transaction_date')
    if category is not None:
        df = df[df['category'] == category]
    if start is not None:
        start_date = pd.to_datetime(start)
        df = df[(df['transaction_date'] >= start_date)]
    if end is not None:
        end_date = pd.to_datetime(end)
        df = df[(df['transaction_date'] <= end_date)]
    if start is not None and end is not None:
        start_date = pd.to_datetime(start)
        end_date = pd.to_datetime(end)
        df = df[(df['transaction_date'] >= start_date) & (df['transaction_date'] <= end_date)]
    if len(df) == 0:
        return px.line(title = 'Overall Spending')
    fig = px.line(title = 'Overall Spending', x = df['transaction_date'], y = df['amount'], markers = True)
    fig.update_layout(
        xaxis_title = "Date",
        yaxis_title = "Amount ($)")
    return fig



if __name__ == '__main__':
    app.run_server(debug = False, port = 4050)