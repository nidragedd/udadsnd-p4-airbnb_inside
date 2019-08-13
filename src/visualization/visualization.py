"""
Created on 08 august 2019

Utility package used by notebooks to visualize data.
All functions that plots graphs with matplotlib/seaborn should be within this package

@author: nidragedd
"""
import matplotlib.pyplot as plt
import seaborn as sns

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


def plot_listings_summary_neighbourhood(data):
    """
    Display several plots about neighbourhood
    :param data: (pandas DataFrame) data used for plots
    """
    figure, axis = plt.subplots(3, 2, figsize=(20, 25))

    axis[0][0].set_title("Number of listings per neighbourhood")
    sns.barplot(y="index", x="neighbourhood", ax=axis[0][0],
                data=data.neighbourhood.value_counts().reset_index().sort_values(by='index'))

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


def barplot_something_per_neighbourhood_sorted(df, column):
    """
    Barplot a the distribution of given feature per neighbourhood
    :param df: (pandas groupby DataFrame) the data used for the plot
    :param column: (string) column of the DataFrame to filter on
    """
    figure, axis = plt.subplots(1, 1, figsize=(8, 5))
    sns.barplot(y="neighbourhood", x=column,
                data=df.groupby('neighbourhood')[column].mean().reset_index().sort_values(by=column), ax=axis)
    axis.set_title("Mean {} per neighbourhood".format(column))
    axis.set_xlabel("Mean {}".format(column))
    axis.set_ylabel("Neighbourhood")
    plt.show()


def _inner_split_location(row):
    """
    Inner method called through 'apply' on the whole dataset
    :param row: each row is given as argument of the function
    :return: row
    """
    elements = row['host_location'].split(', ')
    if len(elements) == 3:
        row['city'] = elements[0]
        row['region'] = elements[1]
        row['country'] = elements[2]
    elif len(elements) == 2:
        row['region'] = elements[0]
        row['country'] = elements[1]
    elif len(elements) == 1:
        row['country'] = elements[0]
    return row


def barplot_hostlocation(df):
    """
    Barplot the host location
    :param df: (pandas DataFrame) dataset to explore
    """
    df_host_loc = df[df['host_location'].notnull()][['id', 'host_location']]
    df_host_loc = df_host_loc.apply(_inner_split_location, axis=1)

    # Update country codes with country name
    df_host_loc.country.replace('FR', 'France', inplace=True)
    df_host_loc.country.replace('US', 'United States', inplace=True)
    df_host_loc.country.replace('GB', 'United Kingdom', inplace=True)
    df_host_loc.country.replace('IT', 'Italy', inplace=True)
    df_host_loc.country.replace('CN', 'China', inplace=True)
    df_host_loc.country.replace('London', 'United Kingdom', inplace=True)
    df_host_loc.country.replace('LONDON', 'United Kingdom', inplace=True)

    # Plot countries and cities
    figure, axis = plt.subplots(2, 1, figsize=(15, 12))
    axis[0].set_title("Most represented countries except France")
    axis[1].set_title("Most represented cities except Paris")
    sns.barplot(y='index', x='country', data=df_host_loc.country.value_counts().reset_index()[1:20], ax=axis[0])
    sns.barplot(y='index', x='city', data=df_host_loc.city.value_counts().reset_index()[1:20], ax=axis[1])
    axis[0].set_ylabel("Country")
    axis[1].set_ylabel("City")
    axis[0].set_xlabel("Count")
    axis[1].set_xlabel("Count")
    plt.show()


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


def scatterplot_xy_top_n_elements_vs_all(df, column, title, nb_elements):
    """
    Scatter plot to show where are the nb_elements most available and the 1000 less expensive rooms to rent
    :param df: (pandas DataFrame) dataset that contains all listings
    :param column: (string) feature to plot in a different color for the top nb_elements
    :param title: (string) title for the plot
    :param nb_elements: (int) the number of elements to keep for display
    """
    figure, axis = plt.subplots(1, 1, figsize=(9, 6))
    axis.set_title(title)
    sns.scatterplot(x="longitude", y="latitude", data=df, alpha=0.1, palette="RdBu", ax=axis)
    subset = df.loc[df[column].sort_values(ascending=False)[:nb_elements].index.tolist()]
    sns.scatterplot(x="longitude", y="latitude", data=subset, alpha=0.9, palette="muted", ax=axis)
    plt.show()


def scatterplot_xy_all_places(df, hue, title, palette=None):
    """
    Scatter plot to show where are rooms to rent based on latitude/longitude values in given dataset
    :param df: (pandas DataFrame) dataset that contains all listings
    :param hue: (string) the feature for color change
    :param title: (string) title for the plot
    :param palette: (string) seaborn palette parameter name if needed
    """
    figure, axis = plt.subplots(1, 1, figsize=(15, 10))
    axis.set_title(title)
    sns.scatterplot(x="longitude", y="latitude", hue=hue, data=df, alpha=0.9, palette=palette, ax=axis)
    plt.show()


def scatterplot_xy_top_flop_expensive_places(df, nb_elements):
    """
    Scatter plot to show where are the nb_elements most and less expensive rooms to rent
    :param df: (pandas DataFrame) dataset that contains all listings
    :param nb_elements: (int) the number of elements to keep for display
    """
    df_lst_sum_no_shared = df[df['room_type'] != 'Shared room']
    top1000 = df_lst_sum_no_shared.price.sort_values(ascending=False)[:nb_elements].index.tolist()
    flop1000 = df_lst_sum_no_shared.price.sort_values()[:nb_elements].index.tolist()

    figure, axis = plt.subplots(1, 1, figsize=(15, 10))
    axis.set_title("{} most and less expensive places (most expensive in blue)".format(nb_elements))
    sns.scatterplot(x="longitude", y="latitude", data=df_lst_sum_no_shared.loc[top1000], palette='RdBu', alpha=0.9,
                    ax=axis)
    sns.scatterplot(x="longitude", y="latitude", data=df_lst_sum_no_shared.loc[flop1000], palette='muted', alpha=0.9,
                    ax=axis)
    plt.show()


def lineplot_feature_over_time(df, column, group, hue=None, col_title=None):
    """
    Plot variation over time of a mean value for a given column
    :param df: (pandas DataFrame) the dataset that contains data
    :param column: (string) the column to use for plotting
    :param group: (string or list) features for the groupby
    :param hue: (string) the feature for color change (if multiple groupby)
    :param col_title: (string) if column has not a readable version you can specify another one with this parameter
    """
    av_time = df.groupby(group)[column].mean().reset_index()
    figure, axis = plt.subplots(1, 1, figsize=(15, 8))
    axis.set_title("Mean {} over time".format(column if col_title is None else col_title))
    if hue is None:
        sns.lineplot(x="date", y=column, data=av_time, ax=axis)
    else:
        sns.lineplot(x="date", y=column, hue=hue, data=av_time, ax=axis)
    axis.set(xticks='')
    for i in utils.get_months_ends(df):
        axis.axvline(i, color='b', linestyle="--", linewidth=0.5)
    for school_holiday in utils.get_school_holidays().values():
        axis.axvline(school_holiday[0], color='r', linestyle=":", linewidth=1)
        axis.axvline(school_holiday[1], color='r', linestyle=":", linewidth=1)
    plt.show()


def lineplot_feature_distinct_neighbourhood_over_time(df, column, group, col_title=None):
    """
    Plot variation over time per neighbourhood for a specific feature/column of the given dataset
    :param df: (pandas DataFrame) the dataset that contains data
    :param column: (string) the column to use for plotting
    :param group: (string or list) features for the groupby
    :param col_title: (string) if column has not a readable version you can specify another one with this parameter
    """
    figure, axis = plt.subplots(5, 4, figsize=(16, 12))
    neighs = df['neighbourhood'].unique().tolist()
    counter = 0
    for i in range(0, 5):
        for j in range(0, 4):
            av_time = df[df['neighbourhood'] == neighs[counter]].groupby(group)[column].mean().reset_index()
            axis[i][j].set_title("Mean {} for {}".format(column if col_title is None else col_title, neighs[counter]))
            sns.lineplot(x="date", y=column, data=av_time, ax=axis[i][j])
            axis[i][j].set(xticks='')
            counter += 1
    plt.show()
