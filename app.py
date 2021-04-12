import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    ]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.title = "Wine Class"

app.layout = html.Div([
    html.Div([

        # Left area of dash
        html.Div([
            # Input for description
            dcc.Textarea(
                id='wine-description-textarea',
                value="Enter your description here",
                style={'width': '100%', 'height': 300},
            ),

            # Submit button
            html.Button("Show me Da Powaa!", id='wine-description-submit', n_clicks=0)
        ], id='wine-description-container', className='three columns'),

        # Right area of dash
        html.Div([
            html.P("Placeholder for all charts")
        ], id='wine-plots-container', className='nine columns'),
    ], className='row')     
])



# Description on submit callback
@app.callback(
    Output('wine-plots-container', 'children'),
    [Input('wine-description-submit', 'n_clicks')],
    [State('wine-description-textarea', 'value')])
def update_output(n_clicks, input_string):
    return "Input: %s"%input_string


if __name__ == '__main__':
    app.run_server(debug=True)