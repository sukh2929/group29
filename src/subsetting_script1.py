# author: Zhiyong Wang
# date: 2020-11-26

"""
Usage:
  subsetting_script1.py --input=<raw_path> --output=<process_path>
  subsetting_script1.py (-h | --help)
  subsetting_script1.py
  
Options:
  -h --help     Shows the arguments needed to run script.
  --input=<raw_path>   Path of the raw data including file name.
  --output=<process_path>      local path to save the subsetted data including file name.
"""

from docopt import docopt
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


opt = docopt(__doc__)


def main(opt):
    print(opt)
    raw_csv = pd.read_csv(opt["--input"])
    discarded_csv, used_csv = train_test_split(raw_csv, test_size=0.2, random_state=123)
    
    used_csv.to_csv(opt["--output"], index = False)
    
    return print("Done! Check the processed file")
   
if __name__ == "__main__":
      main(opt)