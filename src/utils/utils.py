"""
Created on 09 august 2019

Utility package used all over the program

@author: nidragedd
"""
import pandas as pd


def get_school_holidays():
    """
    :return: dict with key as the school holiday name and value is a tuple of 2 dates: when it begins, when it ends
    """
    # Information retrieved from http://icalendrier.fr/vacances/zone-c
    return {
        "autumn": ['2019-10-19', '2019-11-03'],
        "christmas": ['2019-12-21', '2020-01-05'],
        "winter": ['2020-02-08', '2020-02-23'],
        "spring": ['2020-04-04', '2020-04-19']
    }


def get_months_ends(df):
    """
    Retrieve all months ends over a year starting from the minimum date found in the given dataset
    :param df: (pandas DataFrame) the dataset that contains data
    :return: (list) list of last day of months for 1 year
    """
    return pd.date_range(start=df.date.min(), periods=12, freq='M').strftime("%Y-%m-%d").tolist()
