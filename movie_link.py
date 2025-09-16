from typing import  Union, Any
import requests
from imdb import Cinemagoer

ia = Cinemagoer()



def search_movie(movie_name) -> list[dict[str, Union[Union[int, str], Any]]]:
    result = ia.search_movie(movie_name)
    print(result)
    movies = []
    for count, value in enumerate(result, start=1):
        title = value['title']

        streaming_link = f'https://vidsrc.to/embed/movie/tt{value.movieID}'
        url = f"https://www.imdb.com/title/tt{value.movieID}/"
        response = requests.get(streaming_link, timeout=10)

        try:
            if response.status_code == 200:
                if movie_name.lower().strip() == title.lower().strip():
                    movie_info = {

                        "title": title,
                        "url": url,
                        "streaming_link": streaming_link
                    }

                    movies.append(movie_info)

                    print(f""" {count} - Title: {title}
                                IMDB Link: {url}
                                Streaming Link: {streaming_link}
                                
                                """)
        except requests.RequestException as e:
            print(f"Error fetching streaming link for {title}: {e}")
    return movies


def search_series(series_name, season, episode) -> list[dict[str, Union[Union[int, str], Any]]]:
    result = ia.search_movie(series_name)
    series = []
    for count, value in enumerate(result, start=1):
        title = value['title']
        streaming_link = f'https://vidsrc.to/embed/tv/tt{value.movieID}/{season}/{episode}'
        imdb_link = f'https://www.imdb.com/title/tt{value.movieID}/'

        response = requests.get(streaming_link)

        if response.status_code == 200:
            if series_name.lower() == title.lower():
                series_info = {
                    "count": count,
                    "title": title,
                    "url": imdb_link,
                    "streaming_link": streaming_link
                }
                print(f""" {count} - Title: {title})
                    IMDB Link: {imdb_link}
                    Streaming Link: {streaming_link}
                    """)

                series.append(series_info)
    return series


if __name__ == '__main__':
    search_movie("Inception")
  

