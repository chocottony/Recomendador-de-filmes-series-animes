from http import HTTPStatus

import requests
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()
TMBD_API_KEY = 'a9b8d6d94ef62653e6760d2b7e14b2f8'


@app.get('/items', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_items(name: str):
    content = ''
    url = 'https://api.themoviedb.org/3/search/multi'
    params = {'query': name, 'api_key': TMBD_API_KEY}
    response = requests.get(url, params=params)
    info = response.json()

    if response.status_code == HTTPStatus.OK:
        for item in info['results']:
            name = item.get('name', item.get('title', 'Unknown'))
            overview = item.get('overview', 'No overview available')

            content += f'<p>{name} - {overview}</p>'

        return f"""
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                {content}
            </body>
        </html>
        """
    return f"""
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                {'Not Working!'}
            </body>
        </html>
        """
