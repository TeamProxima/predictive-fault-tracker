import numpy as np

from analysis_manager import AnalysisManager


def main():
    analysis_manager = AnalysisManager()
    # Generate train data
    X = 0.9 * np.random.randn(10, 1)
    # X_train = np.r_[X + 2, X - 2]
    X_train = X + 25
    # Generate some regular novel observations
    X = 0.3 * np.random.randn(20, 1)
    # X_test = np.r_[X + 2, X - 2]
    X_test = X + 20
    # Generate some abnormal novel observations
    X_outliers = np.random.uniform(low=16, high=20, size=(20, 1))

    # X_train = np.array([25 for _ in range(10)]).reshape(-1, 1)
    model = analysis_manager.get_trained_model_from_data(X_train)
    analysis_manager.save_model(model)

    # model = load_model()
    X_outliers = np.array([25]).reshape(-1, 1)
    print(X_outliers)
    print(analysis_manager.predict(model, X_outliers))


if __name__ == "__main__":
    main()
