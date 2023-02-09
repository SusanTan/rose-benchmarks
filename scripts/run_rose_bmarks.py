from matplotlib.ticker import (MultipleLocator, FormatStrFormatter, AutoMinorLocator)
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import utils
import csv
from matplotlib import rcParams
import math
from fractions import Fraction
import pickle
from matplotlib import rc

import sys
import os
import subprocess
from joblib import Parallel, delayed, parallel
from threading import Timer
from termcolor import colored
from collections import ChainMap
import json

def clean_all_bmarks(root_path):

  os.chdir(root_path)
  make_process = subprocess.Popen(["./clean.sh"],
                  stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

  if make_process.wait() != 0:
    print(colored("Clean failed", 'red'))

  print("Finish cleaning")

  return 0

def run_one_bmark(path, bmark_name):
  dir_path = os.path.join(path, bmark_name)
  os.chdir(dir_path)

  print("Running %s" % (bmark_name))
  with open("result.log", "w") as fd:
    make_process = subprocess.Popen(['make', 'check_performance'],
       env=dict(os.environ, CC='clang'), stdout=fd, stderr=fd)
    if make_process.wait() != 0:
      print(colored("Failed", 'red'))
    else:
      print(colored("Succeeded", 'green'))

  return

def set_config():
  config = {}
  config['root_path'] = os.path.join(os.getcwd(), '../') 
  config['bmark_list'] = json.load(open('bmarks.json'))
  config['result_path'] = os.path.join(config['root_path'], '../results/figures')
  return config

if __name__ == "__main__":
  
  config = set_config()
  if not config:
    print("Bad configuration, please start over.")
    sys.exit(1)

  print("\n\n### Performance Experiment Start ####")

  #clean directories
  clean_all_bmarks(config['root_path'])
  
  #Run experiment
  for bmark in config['bmark_list']:
    run_one_bmark(config['root_path'], bmark)

