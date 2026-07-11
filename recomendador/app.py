from http import HTTPStatus

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from services import gemini, tmdb

load_dotenv()

app = FastAPI()
app.mount('/static', StaticFiles(directory='static'), name='static')


@app.get('/items', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_items(search_input: str = ''):

    if not search_input:
        return render_home_page()

    paragraph = gemini.generate_recommendations(search_input)

    html_content = ''
    for rubrica in paragraph.splitlines():
        item_name, item_overview, item_image = tmdb.search_tmdb(rubrica)

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

    return render_page(html_content)


def render_page(html_content: str = '') -> str:
    return f"""
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Saira:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=search" />
            <link rel="stylesheet" href="/static/style.css">
            <title>PlotPilot</title>
        </head>
        <body>
            <h1 style="color: var(--cor-destaque); font-family: 'Saira', sans-serif;">PlotPilot</h1>
            <form action = '/items' method = 'get'>
                <label for = 'search_input' style="color: var(--cor-texto); font-family: 'Saira', sans-serif; font-size: 1.2rem;">Enter a description:</label>
                <input type = 'text' id = 'search_input' name = 'search_input'>
                <button type="submit"><span class="material-symbols-outlined">search</span></button>
            </form>
            <div class="container">
                {html_content}
            </div>
        </body>
    </html>
    """


def render_home_page() -> str:
    return """
    <html>
        <head>
            <link rel="preconnect" href="https://fonts.googleapis.com">
            <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
            <link href="https://fonts.googleapis.com/css2?family=Saira:ital,wght@0,100..900;1,100..900&display=swap" rel="stylesheet">
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200&icon_names=search" />
            <link rel="stylesheet" href="/static/style.css">
            <title>PlotPilot</title>
        </head>
        <body>
            <section class="hero-section">
                <div class="hero-container">
                    <div class="hero-content">
                    <span class="hero-tagline">AI-Powered</span>
                    <h1 class="hero-title">PlotPilot</h1>
                    <p class="hero-description">
                        Describe what you want to watch and our AI will find the perfect recommendations for you
                    </p>
                    <form action = '/items' method = 'get'>
                        <label for = 'search_input' style="color: var(--cor-texto); font-family: 'Saira', sans-serif; font-size: 1.2rem;">Enter a description:</label>
                        <input type = 'text' id = 'search_input' name = 'search_input'>
                        <button type="submit"><span class="material-symbols-outlined">search</span></button>
                    </form>
                    </div>
                </div>
            </section>
        </body>
    </html>
    """
