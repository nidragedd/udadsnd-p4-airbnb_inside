"""
Created on 09 august 2019

Utility package used all over the program

@author: nidragedd
"""


def get_school_holidays():
    """
    TODO
    :return:
    """
    # Information retrieved from http://icalendrier.fr/vacances/zone-c
    return {
        "autumn": ['2019-10-19', '2019-11-03'],
        "christmas": ['2019-12-21', '2020-01-05'],
        "winter": ['2020-02-08', '2020-02-23'],
        "spring": ['2020-04-04', '2020-04-19']
    }