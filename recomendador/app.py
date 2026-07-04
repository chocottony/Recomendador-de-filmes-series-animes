import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TMBD_API_KEY = os.getenv('TMBD_API_KEY')
app = FastAPI()

@app.get('/items', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_items(search_input: str = ''):

    if not search_input:
        return """
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                <form action = '/items' method = 'get'>
                    <label for = 'search_input'>Enter a name:</label>
                    <input type = 'text' id = 'search_input' name = 'search_input'>
                    <input type = 'submit' value = 'Search'>
                </form>
            </body>
        </html>
        """
    
    html_content = ''
    api_url = 'https://api.themoviedb.org/3/search/multi'
    query_params = {'query': search_input, 'api_key': TMBD_API_KEY}
    response = requests.get(api_url, params=query_params)
    response_data = response.json()

    if response.status_code == HTTPStatus.OK:
        for item in response_data['results']:
            item_name = item.get('name', item.get('title', 'Unknown'))
            item_overview = item.get('overview', 'No overview available')
            item_image = item.get('poster_path', None)

            html_content += f'<p>{item_name} - {item_overview}</p>'

        return f"""
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                <form action = '/items' method = 'get'>
                    <label for = 'search_input'>Enter a name:</label>
                    <input type = 'text' id = 'search_input' name = 'search_input'>
                    <input type = 'submit' value = 'Search'>
                </form>
                {html_content}
            </body>
        </html>
        """
