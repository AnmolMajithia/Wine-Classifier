import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from helpers import PlotHelper, PredHelper

external_stylesheets = [
    'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    ]
app = dash.Dash(__name__,
                external_stylesheets=external_stylesheets,
                suppress_callback_exceptions=True)

app.title = "Wine Class"

pred_helper = PredHelper()
plot_helper = PlotHelper()

app.layout = html.Div([
    html.Div([

        # Left area of dash
        html.Div([
            # Input for description
            dcc.Textarea(
                id='wine-description-textarea',
                value="Enter your description here",
                style={'width': '90%'}
            ),

            # Submit button
            html.Button("Show me Da Powaa!", id='wine-description-submit', n_clicks=0)
        ], id='wine-description-container', className='three columns darker-container'),

        # Right area of dash
        html.Div([
            html.P("Placeholder for all charts", id="wine-plots-variety-text"),
            dcc.Graph(id="wine-plots-map")
        ], id='wine-plots-container', className='nine columns dark-container'),
    ], className='row')     
], style={'height':'100vh'})



# Description on submit callback
@app.callback(
    [Output('wine-plots-variety-text', 'children'),
    Output('wine-plots-map', 'figure')
    ],
    [Input('wine-description-submit', 'n_clicks')],
    [State('wine-description-textarea', 'value')])
def update_output(n_clicks, input_string):
    print("Updating")
    wine_predicted_variety = pred_helper.get_variety(input_string)
    wine_text = "Predicted wine variety: %s"%wine_predicted_variety

    wine_points_map = plot_helper.get_map(wine_predicted_variety)
    
    return wine_text, wine_points_map


if __name__ == '__main__':
    app.run_server(debug=True)