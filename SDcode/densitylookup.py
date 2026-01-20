import pandas as pd
import numpy as np
import os


libary_path = os.path.expanduser('~/SD/SDcode/Project_Prop.csv')
#Chart lookups
df = pd.read_csv(libary_path) ### This changes per computer
headers = df.columns.tolist()
##^^ makes a header list

data = df.to_numpy() # puts df into numpy for easier use

# create a lookup for column header
col_idx = {name: i for i, name in enumerate(headers)}

def pl(inputvar, inputvalue, outputvar):  ## Property lookup function

    # gets the column positions
    l = col_idx[inputvar]
    c = col_idx[outputvar]


    x = data[:, l]
    y = data[:, c]

    # check that inputvalue is within bounds of the entire sheet
    if inputvalue < x[0] or inputvalue > x[-1]:
        raise ValueError(f"{inputvar}={inputvalue} is out of range [{x[0]}, {x[-1]}]")
    i_high = np.searchsorted(x, inputvalue) ## position above
    i_low = i_high - 1  ## position below

    # exact match
    if x[i_high] == inputvalue:
        return y[i_high]
    
    ## for interpolation
    x1, x2 = x[i_low], x[i_high]
    y1, y2 = y[i_low], y[i_high]

    # interpolation formula
    propvalue = y1 + (y2 - y1) * (inputvalue - x1) / (x2 - x1)
    return propvalue

print(1/pl('T',305,'vol_f'))