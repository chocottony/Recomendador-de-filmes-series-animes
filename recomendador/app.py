import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from google import genai

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_API_KEY')
TMBD_API_KEY = os.getenv('TMBD_API_KEY')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get('/items', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_items(search_input: str = ''):

    if not search_input:
        return """
        <html>
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Saira:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=search" />
                <link rel="stylesheet" href="/static/style.css">
                <title>Recomendador</title>
            </head>
            <body>
                <h1 style="color: var(--cor-destaque); font-family: 'Saira', sans-serif;">PlotPilot</h1>
                <form action = '/items' method = 'get'>
                    <label for = 'search_input' style="color: var(--cor-texto); font-family: 'Saira', sans-serif; font-size: 1.2rem;">Enter a name:</label>
                    <input type = 'text' id = 'search_input' name = 'search_input'>
                    <button type="submit"><span class="material-symbols-outlined">search</span></button>
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
            if item.get('media_type') not in ['movie', 'tv']:
                continue
            item_name = item.get('name', item.get('title', 'Unknown'))
            item_overview = item.get('overview', 'No overview available')
            item_image = item.get('poster_path', None)

            if item_image:
                html_content += f'''
                <div class = "card">
                    <img src="https://image.tmdb.org/t/p/w500{item_image}" alt="{item_name}">
                    <div class = "card-content">
                        <p class = "card-title">{item_name}</p>
                        <p class = "card-overview">{item_overview}</p>
                    </div>
                </div>'''
            else:
                html_content += f'''
                <div class = "card">
                <img src="https://placehold.co/400x600?text=No+Image+Available" alt="{item_name}">
                    <div class = "card-content">
                        <p class = "card-title">{item_name}</p>
                        <p class = "card-overview">{item_overview}</p>
                    </div>
                </div>'''

        return f"""
        <html>
            <head>
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Saira:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
                <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=search" />
                <link rel="stylesheet" href="/static/style.css">
                <title>Recomendador</title>
            </head>
            <body>
                <h1 style="color: var(--cor-destaque); font-family: 'Saira', sans-serif;">PlotPilot</h1>
                <form action = '/items' method = 'get'>
                    <label for = 'search_input' style="color: var(--cor-texto); font-family: 'Saira', sans-serif; font-size: 1.2rem;">Enter a name:</label>
                    <input type = 'text' id = 'search_input' name = 'search_input'>
                    <button type="submit"><span class="material-symbols-outlined">search</span></button>
                </form>
                <div class="container">
                    {html_content}
                </div>
            </body>
        </html>
        """
