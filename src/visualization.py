"""
Created on 08 august 2019

Utility package used by notebooks to visualize data

@author: nidragedd
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from src.utils import utils


def _subplot_neighbourhood(axis, title, column, data):
    """
    Inner method to barplot one column values per neighbourhood
    :param axis: matplotlib axis to update
    :param title: (string) plot title that will be displayed
    :param column: (string) column of the DataFrame to filter on
    :param data: (pandas groupby DataFrame) the data used for the plot
    """
    df_gb = data.groupby('neighbourhood')
    axis.set_title(title)
    sns.barplot(y="neighbourhood", x=column, data=df_gb[column].mean().reset_index(), ax=axis)
    axis.axvline(data[column].mean(), color='r')
    axis.axvline(data[column].median(), color='g')


def _get_months_ends(df):
    """
    Retrieve all months ends over a year starting from the minimum date found in the given dataset
    :param df: (pandas DataFrame) the dataset that contains data
    :return: (list) list of last day of months for 1 year
    """
    return pd.date_range(start=df.date.min(), periods=12, freq='M').strftime("%Y-%m-%d").tolist()


def plot_something_over_time(df, column):
    """
    Plot variation over time of a mean value for a given column
    :param df: (pandas DataFrame) the dataset that contains data
    :param column: (string) the column to use for plotting
    """
    av_time = df.groupby('date')[column].mean().reset_index()
    figure, axis = plt.subplots(1, 1, figsize=(15, 8))
    axis.set_title("Mean {} over time".format(column))
    sns.lineplot(x="date", y=column, data=av_time, ax=axis)
    axis.set(xticks='')
    for i in _get_months_ends(df):
        axis.axvline(i, color='b', linestyle="--", linewidth=0.5)
    for school_holiday in utils.get_school_holidays().values():
        axis.axvline(school_holiday[0], color='r', linestyle=":", linewidth=1)
        axis.axvline(school_holiday[1], color='r', linestyle=":", linewidth=1)
    plt.show()


def plot_listings_summary_neighbourhood(data):
    """
    Display several plots about neighbourhood
    :param data: (pandas DataFrame) data used for plots
    """
    figure, axis = plt.subplots(3, 2, figsize=(20, 25))

    axis[0][0].set_title("Number of listings per neighbourhood")
    sns.barplot(y="index", x="neighbourhood", data=data.neighbourhood.value_counts().reset_index(), ax=axis[0][0])

    _subplot_neighbourhood(axis[0][1], "Mean availability over year per neighbourhood", "availability_365", data)
    _subplot_neighbourhood(axis[1][0], "Mean listing price per neighbourhood", "price", data)
    _subplot_neighbourhood(axis[1][1], "Mean min. nb of nights per neighbourhood", "minimum_nights", data)
    _subplot_neighbourhood(axis[2][0], "Mean nb of reviews/month neighbourhood", "reviews_per_month", data)
    _subplot_neighbourhood(axis[2][1], "Mean nb of listings/host per neighbourhood", "calculated_host_listings_count", data)

    # Handle labels display
    axis[0][0].set_xlabel("Listings count")
    axis[0][1].set_xlabel("Mean availability (nb of days)")
    axis[1][0].set_xlabel("Mean price")
    axis[1][1].set_xlabel("Mean min. nb of nights")
    axis[2][0].set_xlabel("Mean nb of reviews/month")
    axis[2][1].set_xlabel("Mean nb of listings/host")
    for i in range(0, 3):
        for j in range(0, 2):
            axis[i][j].set_ylabel("")
            axis[i][j].set_yticklabels(axis[i][j].get_yticklabels(), rotation=20)

    plt.show()


def print_basic_info_for_feature(data, column):
    """
    Print basic informations for a given feature in a given dataset
    :param data: (pandas DataFrame) dataset
    :param column: (string) column/feature name
    """
    print("There are {} different values for the '{}' feature.".format(data[column].nunique(), column))
    print("There are {} missing values.".format(data[column].isna().sum()))
    print("Here is a sample:")
    print(data[column].unique())


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


def plot_room_type_share(df):
    """
    Plot a pie chart and a countplot for the room types
    :param df: (pandas DataFrame) dataset that contains all listings
    """
    figure, axis = plt.subplots(1, 2, figsize=(15, 5))
    axis[0].set_title("Share of room types")
    axis[1].set_title('Count room types')
    axis[0].pie(df.room_type.value_counts(), labels=list(df.room_type.value_counts().index),
                autopct='%1.1f%%', shadow=True)
    axis[1] = sns.countplot(x='room_type', data=df)

    # Trick to display value on countplot graph
    for p in axis[1].patches:
        _x = p.get_x() + p.get_width() / 2
        _y = p.get_y() + p.get_height() + 1
        value = '{}'.format(p.get_height())
        axis[1].text(_x, _y, value, ha="center")
    plt.show()


def plot_room_type_places(df):
    """
    Plot places (scatter plot) with different color for each room type (3)
    :param df: (pandas DataFrame) dataset that contains all listings
    """
    figure, axis = plt.subplots(1, 1, figsize=(15, 10))
    axis.set_title("Room type emplacements")
    sns.scatterplot(x="longitude", y="latitude", hue="room_type", data=df, alpha=0.9, ax=axis)
    plt.show()


def plot_room_type_mean_price(df):
    """
    Bar plot of the mean price value for each different room type (3)
    :param df: (pandas DataFrame) dataset that contains all listings
    """
    figure, axis = plt.subplots(1, 1, figsize=(8, 5))
    sns.barplot(x="room_type", y='price',
                data=df.groupby('room_type')['price'].mean().reset_index().sort_values(by='price'), ax=axis)
    axis.set_title("Mean price per room type")
    axis.set_xlabel("Room type")
    axis.set_ylabel("Mean price")
    plt.show()


def plot_top_flop_expensive_places(df):
    """
    Scatter plot to show where are the 1000 most expensive and the 1000 less expensive rooms to rent
    :param df: (pandas DataFrame) dataset that contains all listings
    """
    df_lst_sum_no_shared = df[df['room_type'] != 'Shared room']
    top1000 = df_lst_sum_no_shared.price.sort_values(ascending=False)[:1000].index.tolist()
    flop1000 = df_lst_sum_no_shared.price.sort_values()[:1000].index.tolist()

    figure, axis = plt.subplots(1, 1, figsize=(15, 10))
    axis.set_title("1000 most and less expensive places (most expensive in blue)")
    sns.scatterplot(x="longitude", y="latitude", data=df_lst_sum_no_shared.loc[top1000], palette='RdBu', alpha=0.9,
                    ax=axis)
    sns.scatterplot(x="longitude", y="latitude", data=df_lst_sum_no_shared.loc[flop1000], palette='muted', alpha=0.9,
                    ax=axis)
    plt.show()

