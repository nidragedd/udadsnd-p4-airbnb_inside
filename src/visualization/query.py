"""
Created on 11 august 2019

Utility package used by notebooks to query data and print values, pandas DataFrame, etc

@author: nidragedd
"""


def print_basic_info_for_feature(data, column):
    """
    Print basic informations for a given feature in a given dataset
    :param data: (pandas DataFrame) dataset
    :param column: (string) column/feature name
    """
    total = data.shape[0]
    missing = data[column].isna().sum()
    print("There are {} different values for the '{}' feature.".format(data[column].nunique(), column))
    print("There are {} missing values ({:.2f}%).".format(missing, 100*(missing/total)))
    print("Here is a sample:")
    print(data[column].unique()[:8])


def get_hp_infos_for_listing(df, query_name):
    """
    Get airbnb homepage informations from a dataset and given a listing name
    :param df: (pandas DataFrame) dataset that contains all listings
    :param query_name: (string) will be used to query the 'name' feature in the dataset
    :return: (pandas DataFrame) found information or None
    """
    info_cols = ['id', 'name', 'room_type', 'beds', 'price', 'number_of_reviews', 'review_scores_rating',
                 'host_is_superhost']
    lst_id = df[df['name'].str.find(query_name) > -1].id.tolist()
    if len(lst_id) > 0:
        return df[df['id'] == lst_id[0]][info_cols]
    else:
        print("No listing found with this query '{}'".format(query_name))
        return None
