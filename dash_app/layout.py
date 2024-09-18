import dash
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    return dbc.Container(
                [
                    #------------  
                    dbc.Row(dbc.Navbar(
                        dbc.Container(
                            [
                                dbc.NavbarBrand(html.B("FastAPI Blog App", style={"fontSize": "2rem"}), className="ms-2"),  # Blog App title
                                dbc.Nav(
                                    dbc.NavItem(dbc.Button("Create Post", id='create-post-button', color="primary", className="ms-2")),  # Create Post button
                                    className="ms-auto",  # Push the button to the right
                                ),
                            ]
                        ),
                        color="primary",  # Set the navbar color
                        dark=True,  # Make the text light to contrast the dark background
                        className="mb-4",  # Margin below the navbar
                        fixed="top"
                        )
                    ),

                    # Search field
                    dbc.Row([
                        dbc.Col(width=4),
                        dbc.Col(
                            dbc.Input(placeholder='Search...', id='search-field'), width=4
                        ),
                        dbc.Col(dbc.Button('Search', id='search-blogs-button'), width=1)
                    ], style={"padding-top": "100px"}),

                    dcc.Interval(id='page-load-trigger', n_intervals=0, max_intervals=1),
                    dbc.Row([
                        # the news feed col
                        dbc.Col(
                            dbc.Card([
                                dbc.CardHeader(html.P(
                                    html.B('Latest Blogs'),
                                    style={'fontSize': '2rem'},
                                    className='text-center')),

                                dbc.CardBody(
                                # Blog feed to display the latest blogs or search results
                                html.Div(id="blog-feed", children=[]),
                                )
                    ]), width=6
                        ),

                        # the AI assistance col
                        dbc.Col(dbc.Card([
                            dbc.CardHeader(
                                html.P(
                                    html.B('AI Q&A'),
                                    className='text-center',
                                    style={'fontSize': '2rem'}
                                )
                            ),
                            dbc.CardBody()
                            ]
                        ), width=6)
                        ],
                        style={'padding-top': '40px'}
                    ),


                    #------------
                    # The Create Blog Modal
                    html.Div(
                        [
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(dbc.ModalTitle("Create a Blog Post"), close_button=False),
                                    dbc.ModalBody([
                                            dbc.Row(dbc.Col(html.Div(id='blog-content'))),
                                            dbc.Row(
                                                dbc.Col(
                                                    dbc.Input(id='input-title', type='text', placeholder='Blog title'),
                                                    width=4
                                                ), style={'padding-top': '10px'}
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    dbc.Input(id='sub-title-input', type='text', placeholder='Blog sub-title'), width=4
                                                ), style={'padding-top': '20px'}
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    dbc.Textarea(id='input-content', placeholder='Write your blog content here...', style={'width': '100%', 'height': 100}),
                                                    width=8
                                                ), style={'padding-top': '20px'}
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    dbc.Input(id='hashtags-input', type='text', placeholder='#hasthags'), width=4
                                                ), style={'padding-top': '20px'}
                                            ),

                                            dbc.Row(
                                                dbc.Col(
                                                    dbc.Button('Submit', id='submit-blog', color='primary', className='mt-3'),
                                                    width=2
                                                )
                                            ),

                                            dbc.Row(dbc.Col(dbc.Alert(id = 'post-alert', duration=10000, is_open=False), width=4),
                                                    style={"padding-top": "20px"}),
                                            html.Div(id='output')
                                ]),
                                    dbc.ModalFooter(
                                        dbc.Button(
                                            "Close", id="close-create-blog-button", className="ms-auto", n_clicks=0, color='danger'
                                        )
                                    ),
                                ],
                                id="create-blog-modal",
                                is_open=False,
                                size='lg',
                                backdrop='static'
                                
                            ),
                        ]
                    )],
                    fluid=True,
                )
    
    
