import requests
from http import HTTPStatus
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root():
    if "https://api.themoviedb.org/3/search/multi?query=Naruto" == True:
        return """
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                <p>Working!</p>
            </body>
        </html>
        """
    else: 
        return """
        <html>
            <head>
                <title>Recomendador</title>
            </head>
            <body>
                <h1>Welcome to My App</h1>
                <p>Not working!</p>
            </body>
        </html>
        """