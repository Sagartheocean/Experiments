import os
from typing import List

import requests
import xmltodict

from .settings import load_env

SHELF = "currently-reading"
VERSION = 2
API_URL = "https://www.goodreads.com/review/list"


def get_currently_reading() -> List[str]:
    try:
        response = _make_goodreads_request()
        wrapped = xmltodict.parse(response.text)

        reviews = wrapped["GoodreadsResponse"]["reviews"]["review"]
        books = [r["book"] for r in reviews]
        book_titles = [b["title"] for b in books]
    except (requests.exceptions.RequestException, KeyError) as e:
        print(e)
        book_titles = []

    return book_titles


def _make_goodreads_request():
    load_env()

    api_key = os.environ["GOODREADS_API_KEY"]
    user_id = os.environ["GOODREADS_USER_ID"]

    params = {"v": VERSION, "shelf": SHELF, "id": user_id, "key": api_key}

    response = requests.get(API_URL, params)
    return response
