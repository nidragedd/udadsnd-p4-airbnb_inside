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


def clean_listings(df):
    """
    Clean the given dataset:
        * drop unnecessary columns
        * encode categorical to dummies 0/1
        * transform binary nominal to binary numeric 0/1*
        * handle currency symbols
        * extract amenities and dummies
    :param df: (pandas Dataframe) the dataframe to transform
    :return: (pandas Dataframe) a new dataframe transformed
    """
    cols_to_drop = ['id', 'listing_url', 'scrape_id', 'last_scraped', 'experiences_offered', 'notes', 'transit',
                    'interaction', 'house_rules', 'thumbnail_url', 'medium_url', 'picture_url', 'xl_picture_url',
                    'host_id', 'host_name', 'host_about', 'host_response_time', 'host_response_rate',
                    'host_acceptance_rate', 'host_since', 'host_location', 'host_neighbourhood', 'host_listings_count',
                    'host_total_listings_count', 'host_verifications', 'host_url', 'host_thumbnail_url',
                    'host_picture_url', 'host_has_profile_pic', 'calculated_host_listings_count',
                    'calculated_host_listings_count_entire_homes', 'calculated_host_listings_count_private_rooms',
                    'calculated_host_listings_count_shared_rooms', 'street', 'neighbourhood',
                    'neighbourhood_group_cleansed', 'city', 'state', 'zipcode', 'market', 'smart_location',
                    'country_code', 'country', 'latitude', 'longitude', 'property_type', 'square_feet',
                    'has_availability', 'calendar_updated', 'calendar_last_scraped', 'first_review', 'last_review',
                    'requires_license', 'is_business_travel_ready', 'require_guest_profile_picture',
                    'require_guest_phone_verification', 'name', 'summary', 'space', 'description',
                    'neighborhood_overview', 'access', 'weekly_price', 'monthly_price', 'jurisdiction_names']
    df_reduced = drop_cols(df, cols_to_drop)

    # From 't'/'f' to 0/1
    tf_cols = ['host_is_superhost', 'host_identity_verified', 'is_location_exact', 'instant_bookable']
    for feat in tf_cols:
        df_reduced = transform_t_f(df_reduced, feat)

    df_reduced['license_missing'] = df_reduced['license'].apply(lambda x: 1 if pd.isnull(x) else 0)

    currency_cols = ['price', 'security_deposit', 'cleaning_fee', 'extra_people']
    df_reduced = clean_currency_columns(df_reduced, currency_cols)

    one_hot_cols = ['neighbourhood_cleansed', 'room_type', 'bed_type', 'cancellation_policy']
    df_reduced = encode_categorical(df_reduced, one_hot_cols)

    # Amenities
    df_reduced.amenities = df_reduced.amenities.str.strip('{}')
    df_reduced.amenities = df_reduced.amenities.str.replace('"', '')
    df_only_amenities = df_reduced.amenities
    df_only_amenities = df_only_amenities.str.get_dummies(sep=',')
    # Build a dataframe that contains amenities as index and sum of listing containing this amenity as value
    amen_dict = {}
    for amenity in df_only_amenities.columns.tolist():
        amen_dict[amenity] = df_only_amenities[amenity].sum()
    df_amen_sum = pd.DataFrame.from_dict(amen_dict, orient='index', columns=['amen_sum'])
    df_only_amenities_reduced = drop_cols(df_only_amenities, df_amen_sum[df_amen_sum['amen_sum'] < 642].index.tolist())
    # We're almost there, just concat and drop the original 'amenities' column
    df_clean = pd.concat([df_reduced, df_only_amenities_reduced], axis=1)
    df_clean = drop_cols(df_clean, ['license', 'amenities'])

    return df_clean
