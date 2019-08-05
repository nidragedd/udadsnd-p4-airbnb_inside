"""
Created on 05 august 2019

Utility package used by notebooks to collect data

@author: nidragedd
"""
import os
import shutil
import requests

from src.utils import constants as cst


def _build_data_dir():
    """
    Inner method that builds the data directory if does not exist or empty it otherwise
    """
    if os.path.exists(cst.DATA_DIR_PATH):
        # Remove everything within this folder
        shutil.rmtree(cst.DATA_DIR_PATH)
    os.makedirs(cst.DATA_DIR_PATH, exist_ok=True)


def _download_file_from_url(url, local_filename):
    """
    Download a file from the given url and save it in DATA folder under the given local filename
    :param url: (string) url of the file to retrieve
    :param local_filename: (string) name of the file in local DATA folder
    """
    print("Download started for file {}".format(url))
    target_file = os.path.join(cst.DATA_DIR_PATH, local_filename)
    with requests.get(url, stream=True) as r:
        with open(target_file, 'wb') as f:
            shutil.copyfileobj(r.raw, f)
    print("Download finished for file {}".format(url))


def collect_data():
    """
    Method to call to gather all files for this project
    """
    _build_data_dir()

    _download_file_from_url(cst.DATA_LISTING_FULL, cst.LISTING_FULL_FILE)
    _download_file_from_url(cst.DATA_LISTING_LIGHT, cst.LISTING_LIGHT_FILE)
    _download_file_from_url(cst.DATA_CALENDAR, cst.CALENDAR_FILE)
    _download_file_from_url(cst.DATA_REVIEWS, cst.REVIEWS_FILE)
    _download_file_from_url(cst.DATA_NEIGHBOURHOODS, cst.NEIGHBOURHOODS_FILE)

