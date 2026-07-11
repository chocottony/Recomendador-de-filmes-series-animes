import os
from http import HTTPStatus

import requests
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv('TMDB_API_KEY')
api_url = 'https://api.themoviedb.org/3/search/multi'


def search_tmdb(query: str = '') -> str:
    query_params = {'query': query, 'api_key': TMDB_API_KEY}
    response = requests.get(api_url, params=query_params)
    response_data = response.json()

    if response.status_code == HTTPStatus.OK:
        for result in response_data['results']:
            if result.get('media_type') in {'movie', 'tv'}:
                item = result
                break
        if item.get('media_type') in {'movie', 'tv'}:
            item_name = item.get('name', item.get('title', 'Unknown'))
            item_overview = item.get('overview', 'No overview available')
            item_image = item.get('poster_path', None)

            return item_name, item_overview, item_image

    return 'Unknown', 'No overview available', None
