import itertools


import pandas as pd
import numpy as np
df = pd.DataFrame({'a': ['1', '2', '1', '1', '2'], 'b': ['4', np.NaN, '6', '9', '3'], 'c': ['z', 'x', 'y', 'w', 'q']})
df

df.groupby('a')

