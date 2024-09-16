from dash import Dash, dcc, html, Input, Output, State, callback
import requests

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
        
