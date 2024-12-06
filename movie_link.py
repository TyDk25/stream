from typing import  Union, Any
import requests
import imdb

ia = imdb.IMDb()


def search_movie(movie_name) -> list[dict[str, Union[Union[int, str], Any]]]:
    result = ia.search_movie(movie_name)
    movies = []
    for count, value in enumerate(result, start=1):
        title = value['title']
        year = value.get('year')
        streaming_link = f'https://vidsrc.to/embed/movie/tt{value.movieID}'
        url = f"https://www.imdb.com/title/tt{value.movieID}/"
        response = requests.get(streaming_link)

        if response.status_code == 200:
            if movie_name.lower() == title.lower():
                movie_info = {
                    "count": count,
                    "title": title,
                    "year": year,
                    "url": url,
                    "streaming_link": streaming_link
                }

                movies.append(movie_info)

                print(f""" {count}. Title: {title} ({year})
                            IMDB Link: {url}
                            Streaming Link: {streaming_link}
                            
                            """)
    return movies


def search_series(series_name, season, episode) -> list[dict[str, Union[Union[int, str], Any]]]:
    result = ia.search_movie(series_name)
    series = []
    for count, value in enumerate(result, start=1):
        title = value['title']
        year = value.get('year')

        streaming_link = f'https://vidsrc.to/embed/tv/tt{value.movieID}/{season}/{episode}'
        imdb_link = f'https://www.imdb.com/title/tt{value.movieID}/'

        response = requests.get(streaming_link)

        if response.status_code == 200:
            if series_name.lower() == title.lower():
                series_info = {
                    "count": count,
                    "title": title,
                    "year": year,
                    "url": imdb_link,
                    "streaming_link": streaming_link
                }
                print(f""" {count}. Title: {title} ({year})
                    IMDB Link: {imdb_link}
                    Streaming Link: {streaming_link}
                    """)

                series.append(series_info)
    return series


if __name__ == '__main__':
    ...
