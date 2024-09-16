import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    layout = dbc.Container(
                [
                    dbc.Row(dbc.Col(html.H1("Blog Dashboard"), className="mb-4")),
                    dbc.Row(dbc.Col(html.Div(id='blog-content'))),
                    dbc.Row(
                        dbc.Col(
                            dcc.Input(id='input-title', type='text', placeholder='Blog title'),
                            width=4
                        )
                    ),

                    dbc.Row(
                        dbc.Col(
                            dbc.Input(id='sub-title-input', type='text', placeholder='Blog sub-title')
                        )
                    ),

                    dbc.Row(
                        dbc.Col(
                            dcc.Textarea(id='input-content', placeholder='Write your blog content here...', style={'width': '100%', 'height': 100}),
                            width=8
                        )
                    ),
                    dbc.Row(
                        dbc.Col(
                            dbc.Button('Submit', id='submit-blog', color='primary', className='mt-3'),
                            width=2
                        )
                    ),

                    dbc.Row(dbc.Col(dbc.Alert(id = 'post-alert', duration=10000, is_open=False), width=4)),
                    html.Div(id='output')
                ],
                fluid=True,
            )

    return layout