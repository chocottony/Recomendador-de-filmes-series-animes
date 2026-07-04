import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from google import genai

load_dotenv()

GEMINI_KEY = os.getenv('GEMINI_API_KEY')
 # Initialize the client (automatically reads GEMINI_API_KEY from environment)
client = genai.Client()
    
description = input("Digite a descrição do que você quer assistir: ")

# Generate a response using a free-tier model
response = client.models.generate_content(
    model='gemini-2.5-flash',
    contents= f'O usuário quer assistir algo assim: {description}. '
    'Sugira 5 títulos de filmes ou animes com base nisso.'
    'Retorne apenas os títulos, um por linha, sem explicações adicionais.',
)

paragraph = response.text
print (paragraph.splitlines())