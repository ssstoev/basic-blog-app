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

#update the blog feed when you click search
@callback(
    Output("blog-feed", "children"),
    [Input("search-blogs-button", "n_clicks"), Input("page-load-trigger", "n_intervals")],
    State('search-field', 'value')
)

def update_blog_feed(n_clicks, n_intervals, search_query):

    if n_intervals == 0:
        try:
            response = requests.get("http://127.0.0.1:8000/all/blogs")
            # check the status code
            response.raise_for_status()
            blogs = response.json().get('data', [])

        except requests.RequestException as e:
                return [html.P(f"Error: {str(e)}")]
        
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
        
    elif n_clicks > 0:

        if search_query:
            try:
                response = requests.get(f"http://127.0.0.1:8000/blog/{search_query}")

                # put the result in a list even though it is a single dict
                blogs = [response.json().get('data', [])]
                # print(len(blogs))
            
            except requests.RequestException as e:
                return [html.P("No blogs match your search criteria")]
            
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
