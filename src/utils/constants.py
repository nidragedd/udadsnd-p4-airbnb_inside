"""
Created on 05 august 2019

Constants file

@author: nidragedd
"""

DATA_DIR_PATH = "../data2"

DATA_BASE_URL = "http://data.insideairbnb.com/france/ile-de-france/paris/2019-07-09/"
LISTING_FULL_FILE = "listings.csv.gz"
LISTING_LIGHT_FILE = "listings.csv"
CALENDAR_FILE = "calendar.csv.gz"
REVIEWS_FILE = "reviews.csv.gz"
NEIGHBOURHOODS_FILE = "neighbourhoods.csv"

DATA_LISTING_FULL = DATA_BASE_URL + "data/" + LISTING_FULL_FILE
DATA_CALENDAR = DATA_BASE_URL + "data/" + CALENDAR_FILE
DATA_REVIEWS = DATA_BASE_URL + "data/" + REVIEWS_FILE
DATA_LISTING_LIGHT = DATA_BASE_URL + "visualisations/" + LISTING_LIGHT_FILE
DATA_NEIGHBOURHOODS = DATA_BASE_URL + "visualisations/" + NEIGHBOURHOODS_FILE
