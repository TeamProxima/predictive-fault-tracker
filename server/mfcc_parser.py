import sys

import numpy as np

if len(sys.argv) != 2:
    print('Give filename as argument')
    sys.exit(1)

features = np.loadtxt(sys.argv[1])[..., 1:]
np.save(sys.argv[1][:-3] + 'npy', features)
