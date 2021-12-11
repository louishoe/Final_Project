import json
from google.cloud import storage
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

gs = 'gs://project-1050-data/'
df = pd.read_csv(gs+'data_file.csv')
print(df.head())

