import os
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, Input, State
from plotly import plot
from helpers import PlotHelper, PredHelper, DEFAULT_DESCRIPTION

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
            html.H4("Description"),
            # Input for description
            dcc.Textarea(
                id='wine-description-textarea',
                value=DEFAULT_DESCRIPTION,
                style={'width': '90%'}
            ),
            # Submit button
            html.Button("Show me Da Powaa!", id='wine-description-submit', n_clicks=0),
            html.Div([
                html.Span(html.B("Variety"), style={"text-decoration": "underline", "font-size":"large"}),
                html.Br(),
                html.Span("Predicted", id="wine-plots-variety-text"),
            ], className="darker-res-container")
        ], id='wine-description-container', className='three columns darker-container'),

        # Right area of dash
        html.Div([
            # Right Top div with map and prediction
            html.Div([
                html.Div([
                    dcc.Graph(id="wine-plots-map")
                ], className="seven columns"),   
                html.Div([
                    dcc.Graph(id='wine-plots-best-sunburst')
                ], className="five columns left-border")
            ]),
            html.Br(),
            # Right Bottom div with price distrib and one placeholder
            html.Div([
                html.Div([
                    dcc.Graph(id="wine-plots-price-distribution")
                ],className="six columns top-border"),
                html.Div([
                    dcc.Graph(id='wine-plots-points-bar')
                ],className="six columns top-border left-border")
            ])
        ], id='wine-plots-container', className='nine columns dark-container'),
    ], className='row')     
], style={'height':'100vh'})



# Description on submit callback
@app.callback(
    [Output('wine-plots-variety-text', 'children'),
    Output('wine-plots-map', 'figure'),
    Output('wine-plots-price-distribution', 'figure'),
    Output('wine-plots-points-bar', 'figure'),
    Output('wine-plots-best-sunburst', 'figure')
    ],
    [Input('wine-description-submit', 'n_clicks')],
    [State('wine-description-textarea', 'value')])
def update_output(n_clicks, input_string):
    wine_predicted_variety = pred_helper.get_variety(input_string)

    plot_helper.update_filter(wine_predicted_variety)
    wine_points_map = plot_helper.get_map()

    wine_price_distrib = plot_helper.get_price_point_distribution()

    wine_points_bar = plot_helper.get_price_point_bar()

    wine_best_sunburst = plot_helper.get_best_sunburst()
    
    return wine_predicted_variety, wine_points_map, wine_price_distrib, wine_points_bar, wine_best_sunburst


if __name__ == '__main__':
    app.run_server(debug=True)
