import dash
from dash import Dash, dcc, html, Input, Output, State, callback
import requests
import dash_bootstrap_components as dbc
import datetime 

# callback to post blog and upload in db
@callback(
    Output('post-alert', 'is_open'),
    Output('post-alert', 'children'),
    Output('post-alert', 'color'),
    Input('submit-blog', 'n_clicks'),
    State('input-title', 'value'),
    State('sub-title-input', 'value'),
    State('input-content', 'value'),
    State('hashtags-input', 'value')
)

def submit_blog(n_clicks, title, sub_title, content, hasthags):
    if n_clicks:
        print('button pressed')
        if not title:
            return True, 'Title is a mandatory field!', 'danger'
        
        blog_data = {
            'title': title,
            'sub_title': sub_title,
            'content': content,
            'tags': [hasthags]
        }

        try:
            response = requests.post('http://127.0.0.1:8000/new/blog', json=blog_data)

            # Check if the request was successful
            if response.status_code == 200:
                return True, "Blog posted successfully!", "success"
            else:
                return True, f"Failed to post blog. Status code: {response.status_code}, Error: {response.text}", "danger"

        except Exception as e:
            return True, f"An error occurred: {str(e)}", 'danger'
        
    return False, "", ""
    
# open Create Blog modal
@callback(
    Output('create-blog-modal', 'is_open'),
    [Input('create-post-button', 'n_clicks'),
     Input("close-create-blog-button", 'n_clicks'),
    Input('create-blog-modal', 'is_open')]

)

def open_modal(n1, n2, is_open):
    if n1 or n2:
        return not is_open
    return is_open



# Function to safely convert date strings to datetime objects
def parse_date(date_str):
    try:
        return datetime.datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S.%f')
    except ValueError:
        # Handle cases where the date string is not in the expected format
        print(f"Date format error: {date_str}")
        return datetime.min  # Or handle the error as needed

#update the blog feed when you click search
@callback(
    Output("blog-feed", "children"),
    [Input("search-blogs-button", "n_clicks"), Input("page-load-trigger", "n_intervals")],
    State('search-field', 'value')
)

# def update_blog_feed(n_clicks, n_intervals, search_query):

#     if n_intervals == 0:
#         try:
#             response = requests.get("http://127.0.0.1:8000/all/blogs")
#             # check the status code
#             response.raise_for_status()
#             blogs = response.json().get('data', [])

#         except requests.RequestException as e:
#                 return [html.P(f"Error: {str(e)}")]
        
#         feed = []
#         # Sort the blogs by 'date' in descending order (latest first)
#         sorted_blogs = sorted(blogs, key=lambda x: parse_date(x['date']), reverse=True)
#         for blog in sorted_blogs:
#             feed.append(
#                 dbc.Card([
#                     dbc.CardHeader([
#                             html.H5(blog.get('title', 'No title'), className="card-title"),
#                             html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
#                     ]),
#                     dbc.CardBody(
#                         [
#                             html.P(blog.get('content', 'No content'), className="card-text"),
#                             html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle")
#                         ]
#                     ),

#                     dbc.CardFooter([
#                         html.P(f"{blog.get('tags', 'No tags')}", className="card-subtitle")
#                     ])

#                     ], className="mb-3"
#                 )
#             )
            
#         return feed
        
#     elif n_clicks > 0:

#         if search_query:
#             try:
#                 response = requests.get(f"http://127.0.0.1:8000/search/blogs/{search_query}")
#                 response.raise_for_status()  # Ensure the request was successful
#                 blogs = response.json().get('data', [])
                
#                 if not blogs:
#                     return [html.P(f"No blogs found for keyword: {search_query}")]
            
#             except requests.RequestException as e:
#                 return [html.P(f"Error searching blogs: {str(e)}")]
            
#         else:
#             try:
#                 response = requests.get("http://127.0.0.1:8000/all/blogs")
#                 # check the status code
#                 response.raise_for_status()
#                 blogs = response.json().get('data', [])

#             except requests.RequestException as e:
#                 return [html.P(f"Error: {str(e)}")]
            
#         feed = []
#         for blog in blogs:
#             feed.append(
#                 dbc.Card([
#                     dbc.CardHeader([
#                             html.H5(blog.get('title', 'No title'), className="card-title"),
#                             html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
#                     ]),
#                     dbc.CardBody(
#                         [
#                             html.P(blog.get('content', 'No content'), className="card-text"),
#                             html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle"),
#                         ]
#                     ),
#                     dbc.CardFooter([
#                         html.P(f"{blog.get('tags', 'No tags')}", className="card-subtitle")
#                     ])
#                     ], className="mb-3"
#                 )
#             )
            
#         return feed

def update_blog_feed(n_clicks, n_intervals, search_query):
# Only search when the button is clicked (n_clicks > 0) and there's a query
    if n_clicks > 0 and search_query:
        try:
            response = requests.get(f"http://127.0.0.1:8000/search/blogs/{search_query}")
            response.raise_for_status()
            blogs = response.json().get('data', [])

            if not blogs:
                return [html.P("No blogs found matching your search.")]

            # Create HTML content for blog feed
            feed = []
            # Sort the blogs by 'date' in descending order (latest first)   
            sorted_blogs = sorted(blogs, key=lambda x: parse_date(x['date']), reverse=True)
            for blog in sorted_blogs:
                feed.append(
                dbc.Card([
                    dbc.CardHeader([
                            html.H5(blog.get('title', 'No title'), className="card-title"),
                            html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
                    ]),
                    dbc.CardBody(
                        [
                            html.P(blog.get('content', 'No content'), className="card-text"),
                            html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle"),
                        ]
                    ),
                    dbc.CardFooter([
                        html.P(f"{blog.get('tags', 'No tags')}", className="card-subtitle")
                    ])
                    ], className="mb-3"
                )
            )
            return feed

        except requests.RequestException as e:
            return [html.P(f"Error: {str(e)}")]
        
    elif n_clicks and not search_query:
        try:
            response = requests.get(f"http://127.0.0.1:8000/all/blogs")
            response.raise_for_status()
            blogs = response.json().get('data', [])

            if not blogs:
                return [html.P("No blogs found matching your search.")]

            # Create HTML content for blog feed
            feed = []
            # Sort the blogs by 'date' in descending order (latest first)   
            sorted_blogs = sorted(blogs, key=lambda x: parse_date(x['date']), reverse=True)
            for blog in sorted_blogs:
                feed.append(
                dbc.Card([
                    dbc.CardHeader([
                            html.H5(blog.get('title', 'No title'), className="card-title"),
                            html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
                    ]),
                    dbc.CardBody(
                        [
                            html.P(blog.get('content', 'No content'), className="card-text"),
                            html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle"),
                        ]
                    ),
                    dbc.CardFooter([
                        html.P(f"{blog.get('tags', 'No tags')}", className="card-subtitle")
                    ])
                    ], className="mb-3"
                )
            )
            return feed

        except requests.RequestException as e:
            return [html.P(f"Error: {str(e)}")]   

    # If no search query, load all blogs (initial page load or no search query entered)
    elif n_intervals == 0:
        try:
            response = requests.get("http://127.0.0.1:8000/all/blogs")
            response.raise_for_status()
            blogs = response.json().get('data', [])

            if not blogs:
                return [html.P("No blogs found.")]

            # Create HTML content for blog feed
            # Sort the blogs by 'date' in descending order (latest first)
            sorted_blogs = sorted(blogs, key=lambda x: parse_date(x['date']), reverse=True)
            feed = []
            for blog in sorted_blogs:
                feed.append(
                    dbc.Card([
                        dbc.CardHeader([
                                html.H5(blog.get('title', 'No title'), className="card-title"),
                                html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
                        ]),
                        dbc.CardBody(
                            [
                                html.P(blog.get('content', 'No content'), className="card-text"),
                                html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle"),
                            ]
                        ),
                        dbc.CardFooter([
                            html.P(f"{blog.get('tags', 'No tags')}", className="card-subtitle")
                        ])
                        ], className="mb-3"
                    )
                )
            return feed

        except requests.RequestException as e:
            return [html.P(f"Error: {str(e)}")]

    # Default return to prevent overwriting content when not searching or loading
    raise dash.exceptions.PreventUpdate