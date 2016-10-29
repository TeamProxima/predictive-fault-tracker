import sys

import numpy as np

from server.analysis_manager import AnalysisManager

if len(sys.argv) != 2:
    print('Need 1 argument as file name')
    sys.exit(1)

analysis_manager = AnalysisManager()
X_train = np.load(sys.argv[1])
model = analysis_manager.get_trained_model_from_data(X_train)
analysis_manager.save_model(model)
