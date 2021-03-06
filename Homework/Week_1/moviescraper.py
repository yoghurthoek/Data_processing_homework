#!/usr/bin/env python
# Name: Jochem van den Hoek
# Student number: 11066288
"""
This script scrapes IMDB and outputs a CSV file with highest rated movies.
"""

import csv
from re import findall, compile
from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup

TARGET_URL = "https://www.imdb.com/search/title?title_type=feature&release_date=2008-01-01,2018-01-01&num_votes=5000,&sort=user_rating,desc"
BACKUP_HTML = 'movies.html'
OUTPUT_CSV = 'movies.csv'


def extract_movies(dom):
    """
    Extract a list of highest rated movies from DOM (of IMDB page).
    Each movie entry should contain the following fields:
    - Title
    - Rating
    - Year of release (only a number!)
    - Actors/actresses (comma separated if more than one)
    - Runtime (only a number!)
    """
    # Make empty array
    moviedata = []

    for index, element in enumerate(
            dom.find_all(class_="lister-item-content")):

        # Add space to add moviedata
        moviedata.append([])

        # Adds Title
        moviedata[index].append(
            element.find(class_="lister-item-header").a.string)

        # Adds Rating
        moviedata[index].append(
            element.find(class_="ratings-imdb-rating").strong.string)

        # Adds Release year
        moviedata[index].append(
            findall(r'\d+', element.find(class_="lister-item-year").string)[0])

        # Add Actors
        temparray = []
        actors = element.find(string=compile("Stars:"))
        if actors is not None:
            for actor in actors.find_next_siblings("a"):
                temparray.append(actor.string)
            moviedata[index].append(", ".join(temparray))
        else:
            moviedata[index].append("-")

        # Add Runtime
        moviedata[index].append(
            element.find(class_="runtime").string.strip(' min'))

    return moviedata


def save_csv(outfile, movies):
    """
    Output a CSV file containing highest rated movies.
    """
    with open("movies.csv", 'w', encoding='utf-8-sig', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Title', 'Rating', 'Year', 'Actors', 'Runtime'])
        for element in movies:
            writer.writerow(element)
    # ADD SOME CODE OF YOURSELF HERE TO WRITE THE MOVIES TO DISK


def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None
    except RequestException as e:
        print('The following error occurred during HTTP GET request to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns true if the response seems to be HTML, false otherwise
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


if __name__ == "__main__":

    # get HTML content at target URL
    html = simple_get(TARGET_URL)

    # save a copy to disk in the current directory, this serves as an backup
    # of the original HTML, will be used in grading.
    with open(BACKUP_HTML, 'wb') as f:
        f.write(html)

    # parse the HTML file into a DOM representation
    dom = BeautifulSoup(html, 'html.parser')

    # extract the movies (using the function you implemented)
    movies = extract_movies(dom)

    # write the CSV file to disk (including a header)
    with open(OUTPUT_CSV, 'w', newline='') as output_file:
        save_csv(output_file, movies)
