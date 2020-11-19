# author: Zhiyong Wang
# date: 2020-11-18

"""Download data from URL address to local path.

Usage:
  download.py --local_path=<local_path> --url=<url>
  download.py (-h | --help)
  download.py

Options:
  -h --help     Show this screen.
  --url=<url>   URL address of the data.
  --local_path=<local_path>      local path to save the downloaded file.

"""
from docopt import docopt
import urllib.request
from collections import ChainMap
import os
import tarfile
import zipfile

defaults = {
    '--url': 'https://archive.ics.uci.edu/ml/machine-learning-databases/00296/dataset_diabetes.zip',
    '--local_path': './data/raw'
}

def fetch_data(url, local_path):
  if not os.path.isdir(local_path):
    os.makedirs(local_path)
  zip_path = os.path.join(local_path, "dataset_diabetes.zip")
  urllib.request.urlretrieve(url, zip_path)
  
  with zipfile.ZipFile(zip_path, 'r') as zip: 
    # printing all the contents of the zip file 
    zip.printdir() 
  
    # extracting all the files 
    print('Extracting all the files now...') 
    zip.extractall(local_path) 
    print('Done!')


if __name__ == '__main__':
    arguments = docopt(__doc__)
    print(arguments)

    command_line_args = { k: v for k, v in arguments.items() if v }

    combined = ChainMap(command_line_args, os.environ, defaults)

    fetch_data(combined['--url'], combined['--local_path'])


