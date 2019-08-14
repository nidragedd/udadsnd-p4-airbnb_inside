"""
Created on 08 august 2019

Utility package used by notebooks to clean data

@author: nidragedd
"""
import pandas as pd


def drop_cols(df, cols_to_drop):
    """
    Drop given columns from given pandas DataFrame + coherence control for the operation
    :param df: (pandas DataFrame) the dataset to transform
    :param cols_to_drop: (list) columns that will be removed
    :return: a new dataset without the columns
    """
    df_lst_reduced = df.drop(cols_to_drop, axis=1)
    # Coherence control
    assert df_lst_reduced.shape[1] == df.shape[1] - len(cols_to_drop)
    print("After column dropping, new shape is now {}".format(df_lst_reduced.shape))

    return df_lst_reduced


def clean_currency_columns(df, columns):
    """
    Clean 2 columns related to price in the calendar dataset
    :param df: (pandas DataFrame) the dataset to transform
    :param columns: (list) columns with currency to clean
    :return: transformed dataset, NaN are still there but for others the currency has been removed and the numeric format
    has been handled (',' separator for thousands)
    """
    for column in columns:
        df[column] = df[column].apply(lambda x: str.replace(x, '$', '') if not pd.isnull(x) else x)
        df[column] = df[column].apply(lambda x: str.replace(x, ',', '') if not pd.isnull(x) else x)
        df[column] = df[column].astype("float64")
    return df


def transform_t_f(df, columns):
    """
    Transform the given dataset: the given column which is categorical nominal ('t'/'f' which stands for True/False) is
    transformed to binary 0/1
    :param df: (pandas DataFrame) the dataset to transform
    :param columns: (string) columns to transform
    :return: transformed dataset
    """
    df[columns] = df[columns].map({'t': 1, 'f': 0})
    return df


def encode_categorical(df, one_hot_encode_col_list):
    """
    Transform the given dataset by creating dummy variables for each column in the given list
    :parameter df: (pandas Dataframe) the dataframe to transform
    :parameter one_hot_encode_col_list: (list) all columns to one-hot encode
    :return: (pandas Dataframe) the given dataframe transformed
    """
    # Will be used for coherence control check
    nb_new_cols = 0
    new_df = df.copy()

    for col in one_hot_encode_col_list:
        nb_new_cols += new_df[col].nunique()
        dummies = pd.get_dummies(new_df[col], prefix=col)
        new_df = pd.concat([new_df, dummies], axis=1)

    # Do not forget to remove the original columns as they are not needed anymore
    new_df = new_df.drop(one_hot_encode_col_list, axis=1)

    # Coherence control
    assert new_df.shape[1] == df.shape[1] - len(one_hot_encode_col_list) + nb_new_cols
    print("After one-hot encoding, new shape is now {}".format(new_df.shape))
    return new_df
