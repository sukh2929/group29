# author : Javairia Raza 
# date : 2020-11-26

"""
Usage:
  process.py --input=<raw_path> --output=<process_path>
  process.py (-h | --help)
  process.py
  
Options:
  -h --help     Shows the arguments needed to run script.
  --input=<raw_path>   Path of the raw data including file name.
  --output=<process_path>      local path to save the process data.
"""

from docopt import docopt
import os
import pandas as pd
import numpy as np



opt = docopt(__doc__)


def main(opt):
    diabetes_csv = pd.read_csv(opt["--input"])
    
    # Change `readmitted` target column to binary "YES" or "NO" values if admitted or not.
    diabetes_csv["readmitted"] = diabetes_csv["readmitted"].str.replace(r'[<>]30',"YES",regex = True)
  
    # Convert any ? to na
    diabetes_nan = diabetes_csv.replace("?", np.NaN)
    
    # Drop duplicates
    diabetes_interim = diabetes_nan.drop_duplicates(subset= ['patient_nbr'], keep = 'first')

    # Drop unnecessary columns 
    diabetes_interim2 = diabetes_interim.drop(columns = ["encounter_id", "patient_nbr", "race", "weight", 
                                              "payer_code", "medical_specialty", "examide", "citoglipton"])
    # Drop unnecessary columns except race
    diabetes_race_interim2 = diabetes_interim.drop(columns = ["encounter_id", "patient_nbr","weight", 
                                             "payer_code", "medical_specialty", "examide", "citoglipton"])
    
    # Drop any rows with nas and duplicates
    diabetes_clean = diabetes_interim2.dropna()
    diabetes_with_race = diabetes_race_interim2.dropna()

    
    out_path = os.path.join(opt["--output"], "diabetes_clean.csv")
    file = diabetes_clean.to_csv(out_path, index = False)
    
    out_path2 = os.path.join(opt["--output"], "diabetes_with_race.csv")
    file = diabetes_with_race.to_csv(out_path2, index = False)

    
    return print("Done! Check the processed file")



    
if __name__ == "__main__":
      main(opt)

