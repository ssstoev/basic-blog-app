from dash import Dash, dcc, html, Input, Output, State, callback
import requests
import dash_bootstrap_components as dbc

# callback to post blog and upload in db
@callback(
    Output('post-alert', 'is_open'),
    Output('post-alert', 'children'),
    Output('post-alert', 'color'),
    Input('submit-blog', 'n_clicks'),
    State('input-title', 'value'),
    State('sub-title-input', 'value'),
    State('input-content', 'value')
)

def submit_blog(n_clicks, title, sub_title, content):
    if n_clicks:
        print('button pressed')
        if not title or not content:
            return True, 'Title and content fileds must be both filled!', 'red'
        
        blog_data = {
            'title': title,
            'sub_title': sub_title,
            'content': content
        }

        try:
            response = requests.post('http://127.0.0.1:8000/new/blog', json=blog_data)

            # Check if the request was successful
            if response.status_code == 200:
                return True, "Blog posted successfully!", "green"
            else:
                return True, f"Failed to post blog. Status code: {response.status_code}, Error: {response.text}", "red"

        except Exception as e:
            return True, f"An error occurred: {str(e)}", 'red'
        
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


@callback(
    Output("blog-feed", "children"),
    [Input("search-blogs-button", "n_clicks")]
)
def update_blog_feed(n_clicks):
    if n_clicks:
        try:
            response = requests.get("http://127.0.0.1:8000/all/blogs")
            response.raise_for_status()
            blogs = response.json().get('data', [])
        except requests.RequestException as e:
            return [html.P(f"Error: {str(e)}")]
        
        # Create HTML content for blog feed
        if not blogs:
            return [html.P("No blogs found.")]
        
        feed = []
        for blog in blogs:
            feed.append(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5(blog.get('title', 'No title'), className="card-title"),
                            html.P(blog.get('sub_title', 'No subtitle'), className="card-text"),
                            html.P(blog.get('content', 'No content'), className="card-text"),
                            html.P(f"By {blog.get('author', 'Unknown author')}", className="card-subtitle"),
                        ]
                    ),
                    className="mb-3"
                )
            )
        return feed
    return []


# # Callback to search blogs and update the feed
# @callback(
#     Output("blog-feed", "children"),
#     Input("search-blogs-button", "n_clicks"), 
#     State("search-field", "value")
# )

# def update_blog_feed(n_clicks, search_query):
#     if search_query:
#         # Call the FastAPI search route
#         response = requests.get(f"http://127.0.0.1:8050/search/blogs?query={search_query}")
#         blogs = response.json().get('blogs', [])
#     else:
#         # If no search, show latest blogs
#         response = requests.get("http://127.0.0.1:8050/all/blogs")
#         blogs = response.json().get('blogs', [])

#     # Create HTML content for blog feed
#     if not blogs:
#         return [html.P("No blogs found.")]
    
#     feed = []
#     for blog in blogs:
#         feed.append(
#             dbc.Card(
#                 dbc.CardBody(
#                     [
#                         html.H5(blog['title'], className="card-title"),
#                         html.P(blog['content'], className="card-text"),
#                         html.P(f"By {blog['author']}", className="card-subtitle"),
#                     ]
#                 ),
#                 className="mb-3"
#             )
#         )
#     return feed