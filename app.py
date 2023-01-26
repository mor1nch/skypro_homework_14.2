from flask import Flask
from utils import *

app = Flask(__name__)


@app.route("/")
def main_page():
    result = """
                <h1>Возможности:</h1><br>
                <div>
                1. Поиск по названию фильма (/movie/***)............................................| *** - title of film or serial<br>
                2. Поиск по диапазону лет выпуска (/movie/**/to/***)..........................| ** - since year, *** - to year<br>
                3. Поиск по возрастному рейтингу (/rating/***).....................................| *** - children or family or adult<br>
                4. 10 последних выпущенных фильмов по жанру (/genre/***)..............| *** - genre of film
                </div>
                """
    return result


@app.route("/movie/<title>")
def movies_by_title_page(title):
    content_dict = search_film_by_title(title)
    return content_dict


@app.route("/movie/<int:first_year>/to/<int:second_year>")
def movies_by_years_page(first_year, second_year):
    content_list = sort_by_years_interval(first_year, second_year)
    return content_list


@app.route("/rating/<category>")
def movies_by_rating_page(category):
    content_list = search_by_rating(category)
    return content_list


@app.route("/genre/<genre>")
def search_by_genre_page(genre):
    content_list = search_by_genre(genre)
    return content_list


if __name__ == '__main__':
    app.run()
