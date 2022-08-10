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
    df['Transaction Date'] = [i.date() for i in df['transaction_date'].to_list()]
    df['post_date'] = pd.to_datetime(df['post_date'])
    
    # REMOVING RETURNS AND CONVERTING NEGATIVE AMOUNTS TO POSITIVE TO REPRESENT TRANSACTIONS
    df = df[df['amount'] <= 0]
    df['amount'] = df['amount'] * (-1)
    
    df['transaction_year'] = df['transaction_date'].dt.year
    df['transaction_month'] = df['transaction_date'].dt.month
    df['month_name'] = df['transaction_date'].dt.month_name()
    df = df.sort_values('transaction_date').drop(columns = {'post_date'})
    
    table_df = df.rename(columns = {'description' : 'Description',
                             'category' : 'Category',
                             'type' : 'Type',
                             'amount' : 'Amount ($)'})
    relevant_cols = ['Transaction Date', 'Description', 'Category', 'Type', 'Amount ($)']
    table_df = table_df.sort_values('transaction_date')[relevant_cols]
    # Output -> final cleaned df that we pass into our dash application
    return df, table_df


# GETTING DATA 
flex_df = clean_data('flex.csv')
unlimited_df =  clean_data('unlimited.csv')
transactions_df = pd.concat([flex_df[0], unlimited_df[0]], ignore_index = True)
output_df = pd.concat([flex_df[1], unlimited_df[1]], ignore_index = True)

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
years = sorted(pd.unique(transactions_df['transaction_year']).tolist())
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
                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black'}
                )
            ]
        ),
        
        
        html.Div(
            id = 'piegraph',
            children = [
                html.H4('Spending by Category Breakdown', 
                        style = {'fontSize' : 32, 'font-family' : 'monospace', 'font-weight' : 'bold', 'textAlign' : 'center', 'marginTop' : 45, 'marginBottom' : 5}),
  
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a year',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.Dropdown(
                                    id = 'pie-year',
                                    options = years,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace', 'fontSize' : 16}
                                )
                            ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '50px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a month',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.Dropdown(
                                    id = 'pie-month',
                                    options = months,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace', 'fontSize' : 16}
                                )
                            ], style={'display': 'inline-block', 'width': '50%', 'margin-left': '15px', 'margin-right' : '50px'}
                        )
                    ], style=dict(display='flex'), className = 'nine columns'
                ),
                
                dcc.Graph(id = 'pie-chart')
                
            ]
        ),
        
        
        html.Div(
            id = 'transactions',
            children = [
                html.H4('Transactions History', 
                        style = {'fontSize' : 32, 'font-family' : 'monospace', 'font-weight' : 'bold', 'textAlign' : 'center', 'marginTop' : 45, 'marginBottom' : 5}),
  
                html.Div(
                    children = [
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a start date and end date:',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'left', 'color' : 'black', 'marginBottom' : 5}
                                ),
                                dcc.DatePickerRange(
                                    id = 'date_range_line',
                                    min_date_allowed=date(2020, 12, 1),
                                    start_date_placeholder_text="Start Period",
                                    end_date_placeholder_text="End Period",
                                    calendar_orientation='horizontal',
                                    clearable = True,
                                    with_portal = True,
                                    style = {'font-family' : 'monospace', 'textAlign' : 'center', 'fontSize' : 16, 'marginBottom': '15'}
                                ),
                            ], style={'display': 'inline-block', 'width': '20%', 'margin-left': '50px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a year',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 10}
                                ),
                                dcc.Dropdown(
                                    id = 'transaction-year',
                                    options = years,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace', 'fontSize' : 16}
                                )
                            ], style={'display': 'inline-block', 'width': '27%', 'margin-left': '10px', 'margin-right' : '10px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a month',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 10}
                                ),
                                dcc.Dropdown(
                                    id = 'transaction-month',
                                    options = months,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace', 'fontSize' : 16}
                                )
                            ], style={'display': 'inline-block', 'width': '27%', 'margin-left': '10px', 'margin-right' : '10px'}
                        ),
                        
                        html.Div(
                            children = [
                                html.P(
                                    children = 'Select a category',
                                    style = {'fontSize' : 16, 'font-family' : 'monospace', 'textAlign' : 'center', 'color' : 'black', 'marginBottom' : 10}
                                ),
                                dcc.Dropdown(
                                    id = 'category',
                                    options = categories,
                                    value = None,
                                    search_value = '',
                                    style = {'marginBottom' : 5, 'font-family' : 'monospace', 'fontSize' : 16}
                                )
                            ], style={'display': 'inline-block', 'width': '27%', 'margin-left': '10px', 'margin-right' : '50px'}
                        )
                    ], style = {'display' : 'flex', 'marginBottom' : 0}
                ),
                
                dash_table.DataTable(
                    id = 'datatable',
                    data = output_df.to_dict('records'), 
                    columns = [{"name": i, "id": i} for i in output_df.columns],
                    page_size = 10,
                    page_current= 0,
                    sort_action="native",
                    sort_mode="multi",
                    column_selectable = 'single',
                    selected_columns = [],
                    page_action = 'native',
                    fixed_rows = {'headers' : True},
                    style_cell = {
                        'textAlign': 'center', 
                        'overflow' : 'hidden', 
                        'fontSize' : 15,
                        'width' : '{}%'.format(len(output_df.columns))
                    },
                    style_table = {
                        'marginTop' : 10, 
                        'padding-right': '20px', 
                        'padding-left': '60px', 
                        'width': '93%'
                    }
                ),
                                                    
                dcc.Graph(id = 'line-chart', style={'margin-left': '30px', 'margin-right' : '5px'})
  
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
    if (month is None) and (year is not None):
        df = df[df['transaction_year'] == year]
        year_str = ' ' + str(year)
    if (year is None) and (month is not None):
        df = df[df['month_name'] == month]
        month_str = ' ' + str(month)
    if month and year:
        df = df[(df['transaction_year'] == year) & (df['month_name'] == month)]
        year_str = ' ' + str(year)
        month_str = ' ' + str(month)
    fig = px.pie(df, values = df['amount'], names = df['category'], hole = 0.2)
    fig.update_layout(title = 'Spending by Category during:' + month_str + year_str)
    return fig


@app.callback(
    Output('datatable', 'data'),
    [Input('date_range_line', 'start_date'),
     Input('date_range_line', 'end_date'),
     Input('category', 'value'),
     Input('transaction-year', 'value'),
     Input('transaction-month', 'value')
    ]
)
def datatable_update(start, end, category, year, month):
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
    if (year is not None) and (month is None):
        df = df[df['transaction_year'] == year]
    if (year is None) and (month is not None):
        df = df[df['month_name'] == month]
    if month and year:
        df = df[(df['transaction_year'] == year) & (df['month_name'] == month)]
    
    table_df = df.rename(columns = {'description' : 'Description',
                             'category' : 'Category',
                             'type' : 'Type',
                             'amount' : 'Amount ($)'})
    relevant_cols = ['Transaction Date', 'Description', 'Category', 'Type', 'Amount ($)']
    table_df = table_df.sort_values('transaction_date')[relevant_cols]
    
    return table_df.to_dict('records')
    

@app.callback(
    Output('line-chart', 'figure'),
    [Input('date_range_line', 'start_date'),
     Input('date_range_line', 'end_date'),
     Input('category', 'value'),
     Input('transaction-year', 'value'),
     Input('transaction-month', 'value')
    ]
)
def linechart_update(start, end, category, year, month):
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
    if (year is not None) and (month is None):
        df = df[df['transaction_year'] == year]
    if (year is None) and (month is not None):
        df = df[df['month_name'] == month]
    if month and year:
        df = df[(df['transaction_year'] == year) & (df['month_name'] == month)]
    if len(df) == 0:
        return px.line(title = 'Overall Spending')
    fig = px.line(title = 'Overall Spending', x = df['transaction_date'], y = df['amount'], markers = True)
    fig.update_layout(
        xaxis_title = "Date",
        yaxis_title = "Amount ($)")
    return fig


if __name__ == '__main__':
    app.run_server(debug = True, port = 4052)