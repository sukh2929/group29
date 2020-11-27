# authors: Javairia Raza and Sukhdeep Kaur 
# date: 2020-11-26

"""
Usage:
  eda.py --input=<raw_path> --output=<process_path>
  eda.py (-h | --help)
  
Options:
  -h --help     Shows the arguments needed to run script.
  --input=<local_path>   Raw file to do Pandas profiling
  --output=<figures_path>      Path of where to save the figures from EDA.
"""

from docopt import docopt
import os
import pandas as pd
import numpy as np
import altair as alt
from altair_saver import save
import feather





opt = docopt(__doc__)


def main(opt):
    #profile = ProfileReport(diabetes_csv, title='Diabetic Patient Readmission')
#profile.to_notebook_iframe() # create pandas profiling report in notebook
    #profile.to_file("pandas_profiling.html")

# make a table 

    #make the race plot
    diabetes_with_race = pd.read_csv(opt["--input"])
    
    print(diabetes_with_race.shape)
    
    sort_list = ["Caucasian", "AfricanAmerican", "Hispanic", "Asian", "Other", "null"]
    race_plot = alt.Chart(diabetes_with_race).mark_rect().encode(
      y = alt.Y("race:N", title = None, sort = sort_list),
      x = alt.X("readmitted", title = "Readmitted Status"),
      color = "count()",
    ).properties(width = 100, height = 300)

    file_path = os.path.join(opt["--output"], "figure1_racedist_eda.svg")
    race_plot.save(file_path)
    
    #histogram for numerical variables
    
    diabetes_clean = pd.read_csv(opt["--input"])
    
    num_var_dict = {"num_medications": "Number of Medications",
                "num_lab_procedures": "Number of Lab Procedures",
                "num_procedures": "Number of Procedures other than lab", 
                "diag_1" : "Primary Diagnosis",
                "time_in_hospital" : "Time spent in hospital (days)",
                }
    chart1 = [] #Reference (5)
    for key, value in num_var_dict.items():
        chart1.append(alt.Chart(diabetes_clean).mark_area(
          opacity=0.3,
          interpolate='step'
          ).encode(
        alt.X(key, type = "quantitative", bin=alt.Bin(maxbins=10), title = value),
        alt.Y('count()', stack=None),
        alt.Color('readmitted:N', title = "Readmitted Status")
        ).properties(width = 100, height = 100))
        
        alt.hconcat(*chart1)
        
    #histogram for categorical variables
    cat_var_dict = {"A1Cresult": "Hemoglobin A1C Levels",
                "metformin": "Prescribed Metformin or Changed Dosage",
                "insulin": "Prescribed Insulin or Changed Dosage", 
               }
    chart2 = [] #Reference (5)
    
    for key, value in cat_var_dict.items():
        chart2.append(alt.Chart(diabetes_clean).mark_rect().encode(
          alt.Y("readmitted", type = "nominal", title = "Readmitted Status"),
          alt.X(key, type = "nominal", stack=None,  title = value),
          alt.Color('count()')
          ).properties(width = 100, height = 120))
          
          alt.hconcat(*chart2)
    
    return print("Done! Check the folder!")

if __name__ == "__main__":
      main(opt)
