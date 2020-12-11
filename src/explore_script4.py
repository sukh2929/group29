# author: Rachel Wong, Sukhdeep Kaur, Zhiyong Wang
# date: 2020-11-28


"""performs some statistical or machine learning analysis and summarizes the results as a figure(s) and a table(s)
Usage:
  explore_script4.py --input=<raw_path> --output=<process_path>
  explore_script4.py (-h | --help)
  explore_script4.py
  
Options:
  -h --help     Shows the arguments needed to run script.
  --input=<raw_path>   Path of the raw data.
  --output=<process_path>      local path to save the process data.
"""
from docopt import docopt
import numpy as np
import pandas as pd
import altair as alt
import random

from hashlib import sha1

import matplotlib.pyplot as plt
from IPython.display import HTML

from sklearn.compose import ColumnTransformer
from sklearn.dummy import DummyClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import cross_val_score, cross_validate, train_test_split
from sklearn.preprocessing import (
    FunctionTransformer,
    Normalizer,
    OneHotEncoder,
    OrdinalEncoder,
    StandardScaler,
    normalize,
    scale,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    make_scorer,
    precision_score,
    recall_score,
)

from sklearn.model_selection import (
    RandomizedSearchCV,
    cross_validate,
    train_test_split,
)
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.svm import SVC


# Packages necessary for importing data (from a zip file containing 2 dataset CSVs)
import requests, zipfile
from urllib.request import urlopen
from io import BytesIO

opt = docopt(__doc__)
print(opt)

read_path = "data/processed/diabetes_clean.csv"
if len(opt['--input']) > 0:
    read_path = opt['--input']

output_path = opt['--output']

print(read_path)
print(output_path)

diabetes_clean = pd.read_csv(read_path)

# Take a random and representative sample of our diabetes dataset to apply data analysis to
print("subsetting data")

# set the seed 
random.seed(2020)

diabetes_subset = diabetes_clean.sample(n = 1_000)
diabetes_subset


# Change positive and negative labels of readmitted target column to 0 (not readmitted) and 1 (readmitted)
print("split trainning data set")
from sklearn.preprocessing import label_binarize
encoded_column_vector = label_binarize(diabetes_subset['readmitted'], classes=['NO','YES'])
encoded_labels = np.ravel(encoded_column_vector)

diabetes_subset["readmitted"] = encoded_labels

# Split the data into training (0.8) and testing (0.2)
train_df, test_df = train_test_split(diabetes_subset, test_size=0.2, random_state=123)

# Split the data into X and Y
X_train, y_train = train_df.drop(columns=["readmitted"]), train_df["readmitted"] 
X_test, y_test = test_df.drop(columns=["readmitted"]), test_df["readmitted"]

# categorical features - OneHotEncoding
# numeric features - StandardScaler
# ordinal features - OrdinalEncoding
categorical_features = ["age", "diag_1", "diag_2", "diag_3", "max_glu_serum", "A1Cresult", "metformin", "repaglinide", "nateglinide", "chlorpropamide", "glimepiride", "acetohexamide", "glipizide", "glyburide", "tolbutamide", "pioglitazone", "rosiglitazone", "acarbose", "miglitol", "troglitazone", "tolazamide", "glyburide-metformin", "glipizide-metformin", "glimepiride-pioglitazone", "metformin-rosiglitazone", "metformin-pioglitazone"]
numeric_features = ["admission_type_id", "discharge_disposition_id", "admission_source_id", "time_in_hospital", "num_lab_procedures", "num_procedures", "num_medications", "number_outpatient", "number_emergency", "number_inpatient", "number_diagnoses" ]
ordinal_features = ["gender", "change", "diabetesMed"]
target_feature = "readmitted"

# build our transformers
print("build transformers")

categorical_transformer = Pipeline(
    steps=[
        ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
        ("onehot", OneHotEncoder(handle_unknown="ignore")),
    ]
)

numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")), 
            ("scaler", StandardScaler()),
    ]
)

ordinal_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="constant", fill_value="missing")),
            ("ordinal", OrdinalEncoder()),
    ]
)

preprocessor = ColumnTransformer(
    transformers=[
        ("num", numeric_transformer, numeric_features),
        ("cat", categorical_transformer, categorical_features),
        ("ord", ordinal_transformer, ordinal_features)
    ],
    #remainder = "passthrough"
)

preprocessor.fit(X_train, y_train)

new_columns = numeric_features+ordinal_features+list(preprocessor.named_transformers_['cat'].named_steps['onehot'].get_feature_names())


# Create an empty dictionary to store results
results_dict = {}
# Code adapted from MDS 571 - Lab 4
def store_results(classifier_name, scores, results_dict):
    """
    Stores mean scores from cross_validate in results_dict for
    the given model model_name.

    Parameters
    ----------
    model_name :
        scikit-learn classification model
    scores : dict
        object return by `cross_validate`
    results_dict: dict
        dictionary to store results

    Returns
    ----------
        None

    """
    # test cases for store_results function
    assert type(classifier_name) == str # test that the classifier_name is a string
    assert type(scores) == dict # test that the scores is a dictionary
    
    results_dict[classifier_name] = {
        "fit_time": "{:0.4f}".format(np.mean(scores["fit_time"])),
        "score_time": "{:0.4f}".format(np.mean(scores["score_time"])),
        "test_accuracy": "{:0.4f}".format(np.mean(scores["test_accuracy"])),
        "train_accuracy": "{:0.4f}".format(np.mean(scores["train_accuracy"])),
        "test_f1": "{:0.4f}".format(np.mean(scores["test_f1"])),
        "train_f1": "{:0.4f}".format(np.mean(scores["train_f1"])),

    }
    
# Test 3 models against baseline DummyClassifier
print("validating various models")
classifiers = {
    "Dummy Classifier" : DummyClassifier(strategy = "stratified"),
    "RBF SVM": SVC(),
    "Logistic Regression": LogisticRegression(max_iter = 10000),
    "Logistic Regression (balanced)": LogisticRegression(class_weight="balanced", max_iter = 10000),
}

# ignore warnings, DummyClassifier will output many 0s for scores but this is correct
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

scoring = ["accuracy", "f1", "recall", "precision", "average_precision", "roc_auc"]

for classifier_name, classifier in classifiers.items():
    pipe = Pipeline(steps=[("preprocessor", preprocessor), ("classifier", classifier)])
    scores = cross_validate(pipe, X_train, y_train, return_train_score=True, scoring = scoring)
    store_results(classifier_name, scores, results_dict)

# save results from testing models into results_dict
results_dict = pd.DataFrame(results_dict)
results_dict = results_dict.T.rename(columns = {"fit_time" : "Fit Time",  "score_time" : "Score Time", "test_accuracy" : "Test Accuracy", "train_accuracy" : "Train Accuracy", "test_f1" : "Test F1-score", "train_f1" : "Train F1-score"})

# save results_dict as a csv
results_dict.to_csv("./reports/figures/script4_classifier_scores.csv")
print("output various model scores to csv")

# continue our analysis with logistic regression balanced
lr_bal_pipe = Pipeline(steps=[("preprocessor", preprocessor), ("lr", LogisticRegression(class_weight="balanced"))])
scoring=["accuracy", "precision", "f1", "recall", 'roc_auc', 'average_precision']

# create the preprocessor and logistic regression pipeline
pipe = make_pipeline(preprocessor, LogisticRegression(class_weight="balanced", max_iter = 10000))

# do hyperparameter optimization on logistic regression for the hyperparameter C
param_grid = {
             "logisticregression__C": [10,100,500],
              }

# user randomizedsearch to do hyperparameter optimization
random_search = RandomizedSearchCV(pipe, param_distributions=param_grid, n_jobs=-1, n_iter=2, cv=5, scoring= "f1")

# fit our data using the best hyperparameters
random_search.fit(X_train, y_train)
random_search.best_params_

# plot the confusion matrix
print("plotting confusion matrix")
from sklearn.metrics import plot_confusion_matrix

cm = plot_confusion_matrix(random_search.best_estimator_, X_test, y_test, display_labels=["not admitted", "readmitted"], values_format="d", cmap=plt.cm.Blues)
plt.savefig("./reports/figures/script4_confusion_matrix.png", dpi=300)

# plot the precision recall curve
from sklearn.metrics import plot_precision_recall_curve
plot_precision_recall_curve(random_search, X_test, y_test, name='LogisticRegressionClassifier');
plt.plot(recall_score(y_test, random_search.predict(X_test)), precision_score(y_test, random_search.predict(X_test)), 'or', markersize=8)

plt.savefig("./reports/figures/script4_recall_precision.png", dpi=300)

# print the classification report
print(classification_report(y_test, random_search.predict(X_test),
        target_names=["not admitted", "readmitted"]))

# plot the ROC curve
from sklearn.metrics import plot_roc_curve

cm = confusion_matrix(y_test, random_search.predict(X_test))

rc = plot_roc_curve(random_search, X_test, y_test, name='Logistic Regression')
plt.plot(cm[0,1]/(cm[0].sum()), cm[1,1]/(cm[1].sum()), 'or', markersize=8)
plt.savefig("./reports/figures/script4_ROC_AUC.png", dpi=300)

# score our test data
random_search.best_estimator_.fit(X_train, y_train)
random_search.best_estimator_.score(X_test,y_test)

best_pipe = make_pipeline(preprocessor, LogisticRegression(class_weight="balanced", C=10, max_iter = 10000))
best_pipe

# find the most informative coefficients from our training data using our best pipeline
print("find the best coefficients")
best_pipe.fit(X_train, y_train)

coef_df = pd.DataFrame(data=best_pipe.named_steps['logisticregression'].coef_.T, index=new_columns, columns=["Coefficients"]).apply(abs)
coef_df.sort_values(by='Coefficients', ascending=False).head(20)
print(coef_df.head(10))

coef_df.head(10).to_csv("./reports/figures/script4_coefficients.csv")




