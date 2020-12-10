# authors: Javairia Raza 
# date: 2020-11-27

"""Creates a Pandas Profiling report and visuals for exploratory data anaylsis using two datasets
Usage:
  eda2.py --input=<local_path> --output=<figures_path>
  eda2.py (-h | --help)
  
Options:
  -h --help     Shows the arguments needed to run script.
  --input=<local_path>   All the paths needed for EDA including file name. EDA needed two different datasets needed in order of raw data 
                         followed by processed data separated by a semicolon ;.
                         example: "data/raw/dataset_diabetes/diabetic_data.csv;data/processed/diabetes_with_race.csv".
  --output=<figures_path>      Local path to where to save the figures into.
"""

from docopt import docopt
import os
import random
import pandas as pd
import numpy as np
import altair as alt
from altair_saver import save
from pandas_profiling import ProfileReport
from sklearn.model_selection import train_test_split


opt = docopt(__doc__)

string = opt["--input"]
datafile = string.split(";")



def main(opt):
    # Pandas Profiling 
    # 
    diabetes_csv = pd.read_csv(datafile[0])
    profile = ProfileReport(diabetes_csv)
    file_path1 = os.path.join(opt["--output"], "pandas_profiling.html")
    profile.to_file(output_file=file_path1)
    
    #Subset the data for visualization optimization
    random.seed(123)
    diabetes_with_race = pd.read_csv(datafile[1])
    train_df, test_df = train_test_split(diabetes_with_race, test_size=0.2, random_state=123)

    diabetes_subset = train_df.sample(n = 1000)

    # Heatmap for Race
    
    sort_list = ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other", "null"]
    race_plot = alt.Chart(diabetes_subset).mark_rect().encode(
      y = alt.Y("race:N", title = None, sort = sort_list),
      x = alt.X("readmitted", title = "Readmitted Status"),
      color = "count()",
    ).properties(width = 100, height = 300)

    file_path2 = os.path.join(opt["--output"], "figure1_racedist_eda.svg")
    race_plot.save(file_path2)
    
    
    # Histogram for numerical variables

    num_var_dict = {"num_medications": "Number of Medications",
                    "num_lab_procedures": "Number of Lab Procedures",
                    "num_procedures": "Number of Procedures other than lab",
                    "diag_1" : "Primary Diagnosis",
                     "time_in_hospital" : "Time spent in hospital (days)"}
    chart1 = []
    for key, value in num_var_dict.items():
        chart1.append(alt.Chart(diabetes_subset).mark_area(
          opacity=0.3,
          interpolate='step'
          ).encode(
        alt.X(key, type = "quantitative", bin=alt.Bin(maxbins=10), title=value),
        alt.Y('count()', stack=None),
        alt.Color('readmitted:N', title = "Readmitted Status")
        ).properties(width = 100, height = 100))

    num_hists = alt.hconcat(*chart1)
    file_path3 = os.path.join(opt["--output"], "figure2_numhisttarget_eda.svg")
    num_hists.save(file_path3)
        
    # Histogram for categorical variables

    cat_var_dict = {"A1Cresult": "Hemoglobin A1C Levels",
                    "metformin": "Prescribed Metformin or Changed Dosage",
                     "insulin": "Prescribed Insulin or Changed Dosage"}

    chart2 = []
    for key, value in cat_var_dict.items():
          chart2.append(alt.Chart(diabetes_subset).mark_rect().encode(
          alt.Y("readmitted", type = "nominal", title = "Readmitted Status"),
          alt.X(key, type = "nominal", stack=None,  title=value),
          alt.Color('count()')
          ).properties(width = 100, height = 120))

    cat_hists = alt.hconcat(*chart2)
    file_path4 = os.path.join(opt["--output"], "figure3_numcattarget_eda.svg")
    cat_hists.save(file_path4)

    # Scatterplot for Numerical Variables

    numeric_cols = ['num_procedures','time_in_hospital', 'num_lab_procedures',
                    'num_medications', 'number_diagnoses',
                     'number_inpatient', 'number_emergency']

    numeric_scatter = alt.Chart(diabetes_subset).mark_point(size = 4).encode(
                        alt.X(alt.repeat('column'), type = 'quantitative', scale = alt.Scale(zero = False)),
                        alt.Y(alt.repeat('row'), type = 'quantitative', scale = alt.Scale(zero = False))
                        ).properties(height = 100, width = 100
                        ).repeat(
                        row = numeric_cols,
                        column = numeric_cols
                        ).configure_axis(labels = False)

    file_path5 = os.path.join(opt["--output"], "figure4_numscatter_eda.svg")
    numeric_scatter.save(file_path5)

    return print("Done! Check the folder!")

if __name__ == "__main__":
      main(opt)
