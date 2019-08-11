"""
Created on 08 august 2019

Utility package used by notebooks to clean data

@author: nidragedd
"""


def _clean_price_column(df, column):
    """
    Inner function to clean one specific 'price' column in the given dataset
    :param df: (pandas DataFrame) the dataset to transform
    :param column: (string) price related column
    :return: transformed dataset, NaN are still there but for others the currency has been removed and the numeric format
    has been handled (',' separator for thousands)
    """
    df[column] = df[column].apply(lambda x: str.replace(x, '$', '') if str(x) != 'nan' else x)
    df[column] = df[column].apply(lambda x: str.replace(x, ',', '') if str(x) != 'nan' else x)
    df[column] = df[column].astype("float64")
    return df


def calendar_clean_price(df):
    """
    Clean 2 columns related to price in the calendar dataset
    :param df: (pandas DataFrame) the calendar dataset to transform
    :return: transformed dataset, NaN are still there but for others the currency has been removed and the numeric format
    has been handled (',' separator for thousands)
    """
    columns = ['price', 'adjusted_price']
    for col in columns:
        df = _clean_price_column(df, col)
    return df


def listing_clean_price(df):
    """
    Clean columns related to price in the listings dataset
    :param df: (pandas DataFrame) the listings dataset to transform
    :return: transformed dataset, NaN are still there but for others the currency has been removed and the numeric format
    has been handled (',' separator for thousands)
    """
    columns = ['price']
    for col in columns:
        df = _clean_price_column(df, col)
    return df


def transform_t_f(df, column):
    """
    Transform the given dataset: the given column which is categorical nominal ('t'/'f' which stands for True/False) is
    transformed to binary 0/1
    :param df: (pandas DataFrame) the dataset to transform
    :param column: (string) column to transform
    :return: transformed dataset
    """
    df[column] = df[column] .map({'t': 1, 'f': 0})
    return df
