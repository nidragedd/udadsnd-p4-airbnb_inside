"""
Created on 05 august 2019

Constants file

@author: nidragedd
"""

DATA_DIR_PATH = "../data"
CLEAN_DATA_DIR_PATH = DATA_DIR_PATH + "/clean"
RESULTS_DIR_PATH = DATA_DIR_PATH + "/results"

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

LST_X_TRAIN_FILE = 'full_listings_x_train.csv'
LST_Y_TRAIN_FILE = 'full_listings_y_train.csv'
LST_X_VAL_FILE = 'full_listings_x_val.csv'
LST_Y_VAL_FILE = 'full_listings_y_val.csv'
LST_X_TEST_FILE = 'full_listings_x_test.csv'
LST_Y_TEST_FILE = 'full_listings_y_test.csv'

LST_RESULTS_FILE = 'listings_price_prediction.csv'
