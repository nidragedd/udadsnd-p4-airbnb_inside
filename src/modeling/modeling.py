"""
Created on 02 september 2019

Package to hold functions needed in the modeling phase

@author: nidragedd
"""
import numpy as np

from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer

from sklearn.metrics import mean_squared_error

import xgboost as xgb
from xgboost import XGBRegressor

# Model tuning
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import KFold


def fit_and_run_pipeline(pipeline, model_name, X_train, y_train, X_test, y_test):
    """
    Fit using a pipeline/model on train dataset then predict on test dataset
    :param pipeline: (object) sklearn Pipeline or model. It should have a .fit method
    :param model_name: (string) name of the model (for display purpose)
    :param X_train: (pandas DataFrame) data used for training
    :param y_train: (pandas DataFrame) the real target for training
    :param X_test: (pandas DataFrame) data used for prediction
    :param y_test: (pandas DataFrame) the real target for test
    :return: predicted target
    """
    pipeline.fit(X_train, y_train)
    # Make predictions using the train and test set
    y_pred_train = pipeline.predict(X_train)
    y_pred_test = pipeline.predict(X_test)
    # Print RMSE values
    print("RMSE for {} model on train: {:.2f}".format(model_name, np.sqrt(mean_squared_error(y_train, y_pred_train))))
    print("RMSE for {} model on test: {:.2f}".format(model_name, np.sqrt(mean_squared_error(y_test, y_pred_test))))
    return y_pred_test


def get_column_transformer():
    """
    Build and return a ColumnTransformer from sklearn API. This will impute different columns with a different strategy:
    either the mode, either the mean. Other columns will remain without any change.
    :return: the built ColumnTransformer object
    """
    mode_feat = ['host_is_superhost', 'host_identity_verified', 'bathrooms', 'bedrooms', 'beds', 'security_deposit',
                 'review_scores_accuracy', 'review_scores_cleanliness', 'review_scores_checkin',
                 'review_scores_communication', 'review_scores_location', 'review_scores_value', 'review_scores_rating']
    mean_feat = ['cleaning_fee', 'reviews_per_month']

    mean_imputation_transformer = Pipeline(steps=[('mean_imputer', SimpleImputer(strategy='mean'))])
    mode_imputation_transformer = Pipeline(steps=[('mode_imputer', SimpleImputer(strategy='most_frequent'))])
    ct_imput = ColumnTransformer(transformers=[
        ('mean_t', mean_imputation_transformer, mean_feat),
        ('mode_t', mode_imputation_transformer, mode_feat)],
        remainder='passthrough')
    # By default, only the specified columns in transformers are transformed and combined in the output,
    # and the non-specified columns are dropped. (default of 'drop'). By specifying remainder='passthrough',
    # all remaining columns that were not specified in transformers will be automatically passed through

    return ct_imput


def build_xgb_random_search(param_grid, num_iters):
    """
    Build a sklearn RandomizedSearchCV object with XGBoost regressor
    :param param_grid: (dict) the parameters to explore
    :param num_iters: (int) how many parameters will be taken among all possible combinations
    :return: the built sklearn RandomizedSearchCV object
    """
    # K-fold cross validator
    kf = KFold(n_splits=5, shuffle=True, random_state=42)
    rs = RandomizedSearchCV(estimator=XGBRegressor(objective="reg:squarederror", seed=42, eval_metric='rmse',
                                                   verbose=False),
                            param_distributions=param_grid, n_iter=num_iters, iid=False, n_jobs=-1, cv=kf,
                            scoring='neg_mean_squared_error', refit=True, verbose=1)
    return rs


def find_best_parameters(dtrain, params, gridsearch_params, param_names, early_stopping_rounds):
    """
    When using XGBoost python API (so not through sklearn) and its internal cross validation function we need to keep
    track of the best parameters found. This is done here. Some given parameters vary and we keep the best combination
    for the RMSE metric (here it is hardcoded but if needed we could externalize this as well)
    :param dtrain: (DMatrix) training data
    :param params: (dict) the parameters to use for training. Some of them will vary, other will remain
    :param gridsearch_params: (list) list of tuples corresponding to parameters values
    :param param_names: (list) the list of parameters that will vary
    :param early_stopping_rounds: (int) stop after this number of iterations without significant improvement
    """
    # Define initial best params and RMSE
    min_rmse = float("Inf")
    best_params = None

    for param_tuple in gridsearch_params:
        print("CV run for parameters:")
        if len(param_names) > 1:
            for i in range(len(param_names)):
                print("\t{}: {}".format(param_names[i], param_tuple[i]), end="")
                # Update our parameters
                params[param_names[i]] = param_tuple[i]
        else:
            print("\t{}: {}".format(param_names[0], param_tuple), end="")
            # Update our parameters
            params[param_names[0]] = param_tuple

        # Run CV
        cv_results = xgb.cv(params, dtrain, num_boost_round=999, seed=42, nfold=5, metrics='rmse',
                            early_stopping_rounds=early_stopping_rounds)

        # Check if best and update best RMSE score
        min_mean_rmse = cv_results['test-rmse-mean'].min()
        boost_rounds = np.argmin(np.array(cv_results['test-rmse-mean']))
        print("\n\tRMSE value: {:.2f} for {} rounds".format(min_mean_rmse, boost_rounds))

        if min_mean_rmse < min_rmse:
            min_rmse = min_mean_rmse
            best_params = []
            if len(param_names) > 1:
                for i in range(len(param_names)):
                    best_params.append(param_tuple[i])
            else:
                best_params.append(param_tuple)

    print("Best params{}: {}, RMSE value: {:.2f}".format(param_names, best_params, min_rmse))
    for i in range(len(param_names)):
        params[param_names[i]] = best_params[i]


def classify_results(results_df, column):
    """
    Given a DataFrame containing results and a column name, compute absolute difference between prediction and truth,
    its difference percentage and based on this value, classify it among 1 of the 6 classes
    :param results_df: (pandas DataFrame) results data
    :param column: (string) the column name corresponding to one model predictions to evaluate
    :return: the same DataFrame updated with 2 new columns (absolute difference percentage) + class
    """
    diff_col = '{}_perc_diff'.format(column)
    diff_col_class = '{}_perc_diff_class'.format(column)
    results_df[diff_col] = np.round(100 * (np.abs(results_df['y_true'] - results_df[column])) / results_df['y_true'], 2)
    results_df[diff_col_class] = results_df[diff_col].apply(
        lambda x: '6-awful (> 40%)' if x > 40
        else '5-bad (20% < x < 40%)' if x > 20
        else '4-acceptable (10% < x < 20%)' if x > 10
        else '3-good (5% < x < 10%)' if x > 5
        else '2-pretty good (2% < x < 5%)' if x > 2
        else '1-very accurate (< 2%)')
    return results_df
