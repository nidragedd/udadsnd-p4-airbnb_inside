"""
Created on 05 august 2019

Utility package used by notebooks to collect data

@author: nidragedd
"""
import os
import shutil
import requests

from src.utils import constants as cst


def _build_data_dir(data_dir):
    """
    Inner method that builds a specific data directory if does not exist or empty it otherwise
    :param data_dir: (string) path to data directory to build
    """
    if os.path.exists(data_dir):
        # Remove everything within this folder
        shutil.rmtree(data_dir)
    os.makedirs(data_dir, exist_ok=True)


def get_data_file(filename, from_clean_dir=False):
    """
    Get the full path to the data file with given file name
    :param filename: (string) data file name to load
    :param from_clean_dir: (boolean) not required, default is False. If True, file is loaded from data clean directory
    :return: (string) full path to the data file with given file name
    """
    data_dir = cst.CLEAN_DATA_DIR_PATH if from_clean_dir else cst.DATA_DIR_PATH
    return os.path.join(data_dir, filename)


def get_files_list():
    """
    Utility class - Build a list of data file names to iterate over
    :return: (list) list of data file names
    """
    return [cst.LISTING_FULL_FILE, cst.LISTING_LIGHT_FILE, cst.CALENDAR_FILE, cst.REVIEWS_FILE, cst.NEIGHBOURHOODS_FILE]


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
    _build_data_dir(cst.DATA_DIR_PATH)

    _download_file_from_url(cst.DATA_LISTING_FULL, cst.LISTING_FULL_FILE)
    _download_file_from_url(cst.DATA_LISTING_LIGHT, cst.LISTING_LIGHT_FILE)
    _download_file_from_url(cst.DATA_CALENDAR, cst.CALENDAR_FILE)
    _download_file_from_url(cst.DATA_REVIEWS, cst.REVIEWS_FILE)
    _download_file_from_url(cst.DATA_NEIGHBOURHOODS, cst.NEIGHBOURHOODS_FILE)


def save_listing_splits(splits):
    """
    Save splits files corresponding to listings.csv.gz dataset
    :param splits: (list) list of splits dataset. Must be ordered x+y train, x+y val, x+y test
    """
    _build_data_dir(cst.CLEAN_DATA_DIR_PATH)

    filenames = [cst.LST_X_TRAIN_FILE, cst.LST_Y_TRAIN_FILE, cst.LST_X_VAL_FILE, cst.LST_Y_VAL_FILE,
                 cst.LST_X_TEST_FILE, cst.LST_Y_TEST_FILE]

    for split, filename in zip(splits, filenames):
        split.to_csv(os.path.join(cst.CLEAN_DATA_DIR_PATH, filename), index=False)
    print("All files saved to {} folder".format(cst.CLEAN_DATA_DIR_PATH))


def save_price_predictions_results(results):
    """
    Save the predictions of our different models locally
    :param results: (pandas DataFrame) different models predictions compared to ground truth
    """
    _build_data_dir(cst.RESULTS_DIR_PATH)
    results.to_csv(os.path.join(cst.RESULTS_DIR_PATH, cst.LST_RESULTS_FILE), index=False)
