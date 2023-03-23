#!/usr/bin/env python3.9
import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
import subprocess
import time


# Define the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Apple Stock Price'),
    html.Div(children=[
        html.H3(children='Current Price: '),
        html.H3(id='current-price')
    ]),
    dcc.Graph(
        id='stock-price-graph'
    ),
    dcc.Interval(
        id='interval-component',
        interval=5*60*1000, # Update every 5 minutes
        n_intervals=0
    )
])

# Define the callback function to update the current price
@app.callback(
    dash.dependencies.Output('current-price', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_current_price(n):
    # Run the bash script to scrape the current price
    #result = subprocess.run(["./apple_stock_price.sh"], stdout=subprocess.PIPE)
    #current_price = result.stdout.decode('utf-8').strip()

    # Format the current price with dollar sign and two decimal places

    #current_price = "${:,.2f}".format(float(current_price))
    #return current_price
    
    # Run the command and capture the output
    #subprocess.run(['/usr/bin/env', 'python3.9', './apple_stock_price.sh'],stdout=subprocess.PIPE)
    subprocess.check_output('bash apple_stock_price.sh', shell =True)
    # Read the output file and extract the current price
    with open('apple_stock.txt', 'r') as file:
         price_str = file.read().strip()
    # Extract the numeric part of the price string
    price_numeric_str = price_str.split(" USD ")[0]

    # Convert the current price to a float
    current_price = float(price_numeric_str)
    # Format the price as a string with a dollar sign and two decimal places
    current_price_formatted = "${:,.2f}".format(current_price)

    # Do something with the current price
    return current_price_formatted

# Define the callback function to update the graph
@app.callback(
    dash.dependencies.Output('stock-price-graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graph(n):
    # Get the time and price data for the past 24 hours
    x = []
    y = []
    for i in range(24):
        t = time.time() - (i * 3600)
        x.append(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(t)))
        subprocess.check_output('bash apple_stock_price.sh', shell =True)
        # Read the output file and extract the current price
        with open('apple_stock.txt', 'r') as file:
             price_str = file.read().strip()
        # Extract the numeric part of the price string
        price_numeric_str = price_str.split("USD")[0]

        # Convert the current price to a float
        current_price = float(price_numeric_str)
        y.append(current_price)

    # Create the graph
    fig = go.Figure(
        data=go.Scatter(
            x=x,
            y=y,
            mode='lines'
        ),
        layout=go.Layout(
            title='Apple Stock Price Time Series',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Price')
        )
    )

    return fig

if __name__ == '__main__':
    app.run_server(port=8070, debug=True)
