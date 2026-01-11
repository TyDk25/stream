from typing import Any
from omdbapi.movie_search import GetMovie
from dotenv import load_dotenv
import os

load_dotenv()
movie_key = GetMovie(os.getenv("MOVIE_KEY"))

""""
Retrieves movie or series information including streaming links.
"""


def get_title(movie_name, season=None, episode=None) -> dict[str, str | Any]:
    result = movie_key.get_movie(movie_name)
    title = result['title']
    imdb_id = result['imdbid']
    type = result['type']

    if type == "series":
        if season is None or episode is None:
            raise ValueError("Season and Episode must be provided for series.")
        return {
            "title": title,
            "year": result.get("year", "N/A"),
            "type": result.get("type", "series"),
            "imdb": f"https://www.imdb.com/title/{imdb_id}",
            "stream": f"https://vidsrc.me/embed/tv/{imdb_id}/{season}/{episode}"
        }

    else:
        if type == "movie":
            return {

                "title": title,
                "year": result.get("year", "N/A"),
                "type": result.get("type", "movie"),
                "imdb": f"https://www.imdb.com/title/{imdb_id}",
                "stream": f"https://vidsrc.me/embed/movie/{imdb_id}"

            }


print(get_title('inception'))
