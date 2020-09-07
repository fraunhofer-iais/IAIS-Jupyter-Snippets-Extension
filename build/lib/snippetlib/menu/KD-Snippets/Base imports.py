# Data related libraries
import numpy as np
import pandas as pd

# Plotting
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed
from IPython.display import display, HTML

# Convenient helpers
from copy import copy
from time import time
from collections import defaultdict, Counter
from sklearn.preprocessing import minmax_scale

# Printing libraries and settings
# import warnings; warnings.filterwarnings('ignore')
pd.set_option('display.max_columns', 500)
pd.set_option('display.float_format','{0:.2f}'.format)

try:
    # nicer error output
    import stackprinter
    stackprinter.set_excepthook(style='color')
except:
    pass

%matplotlib inline