"""
Created on 08 august 2019

Utility package used by notebooks to visualize data

@author: nidragedd
"""
import matplotlib.pyplot as plt
import seaborn as sns


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
    print("There are {} different values for the '{}' feature.".format(data[column].nunique(), column))
    print("There are {} missing values.".format(data[column].isna().sum()))
    print("Here is a sample:")
    print(data[column].unique())