import sys

import numpy as np

from server.analysis_manager import AnalysisManager

TEST_RESULT_FILE_LOCATION = 'last_test.txt'
SOUND_MODEL_FILE_LOCATION = 'sound.model'

if len(sys.argv) != 2:
    print('Need 1 argument as file name')
    sys.exit(1)

analysis_manager = AnalysisManager()
model = analysis_manager.load_model(SOUND_MODEL_FILE_LOCATION)
preds = model.predict(np.load(sys.argv[1]))
print('{} outliers out of {} samples'.format(preds[preds == -1].size, preds.size))

problem_count = analysis_manager.get_problem_count(preds)

print('Filtered problems: {}'.format(problem_count))
np.savetxt(TEST_RESULT_FILE_LOCATION, preds, fmt='%i')
