import cPickle as pickle
import random

import numpy as np
from sklearn import svm

from constants import *


class AnalysisManager(object):
    def get_trained_model_from_data(self, train_data):
        model = svm.OneClassSVM(nu=0.1, kernel="rbf", gamma=0.1)
        model.fit(train_data)
        return model

    def get_trained_model_from_file(self, data_file, data_type):
        data = np.load(data_file)
        if data_type == TYPE_TEMP:
            # Variance to eliminate disadvantage of fast train
            data = np.array([i + random.uniform(-1.0, 1.0) for i in data.reshape(-1, 1)])
        return self.get_trained_model_from_data(data)

    def predict(self, model, data):
        prediction = model.predict(data)
        return prediction

    def save_model(self, model, loc=DEFAULT_MODEL_FILE_LOCATION):
        pickle.dump(model, open(loc, "w"))

    def load_model(self, location=DEFAULT_MODEL_FILE_LOCATION):
        model = pickle.load(open(location))
        return model

    def test_sound_from_file(self, data_file):
        data = np.load(data_file)
        model = self.load_model(SOUND_MODEL_FILE_LOCATION)
        predictions = model.predict(data)
        return predictions

    def get_problem_count(self, result, search_range=PROBLEM_SEARCH_RANGE,
                          tolerance=OUTLIER_TOLERANCE):
        # TODO: Don't re-walk on the same items
        problem_count = 0
        i = search_range
        while i < len(result):
            outlier_count = 0
            for j in range(search_range):
                if result[i - search_range + j] == -1:
                    outlier_count += 1
            if outlier_count > tolerance:
                problem_count += 1
                i += search_range
            i += 1
        return problem_count

    def check_for_problem_from_file(self, data_file):
        predictions = self.test_sound_from_file(data_file)
        problem_count = self.get_problem_count(predictions)
        return problem_count > PROBLEM_TOLERANCE
