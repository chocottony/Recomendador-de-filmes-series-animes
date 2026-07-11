import os

from dotenv import load_dotenv
from google import genai

load_dotenv()
GEMINI_KEY = os.getenv('GEMINI_API_KEY')


def generate_recommendations(search_input: str = '') -> str:
    client = genai.Client(api_key=GEMINI_KEY)
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=f'O usuário quer assistir algo assim: {search_input}. '
        'Sugira 5 títulos de filmes ou animes com base nisso.'
        'Retorne apenas os títulos originais em inglês, '
        'um por linha, sem explicações adicionais.',
    )

    paragraph = response.text
    return paragraph
