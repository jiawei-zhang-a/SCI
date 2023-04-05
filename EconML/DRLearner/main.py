from econml.orf import DROrthoForest
from sklearn.linear_model import Lasso, LassoCV, LogisticRegression, LogisticRegressionCV
from econml.sklearn_extensions.linear_model import WeightedLassoCV
from sklearn.model_selection import train_test_split
from econml.dr import ForestDRLearner
from sklearn.dummy import DummyRegressor, DummyClassifier
import numpy as np
import scipy.special
import glob
import matplotlib.pyplot as plt
from sklearn.tree import plot_tree
import os

f = open('new.txt', 'w')

def load_and_format_covariates_mbqip(file_path):

    data = np.loadtxt(file_path, delimiter=',')

    contfeats = [1]
    binfeats = [i for i in range(2,49) if i not in contfeats]

    perm = contfeats + binfeats
    x = data[:, perm]
    return x


def load_all_other_crap(file_path):
    data = np.loadtxt(file_path, delimiter=',')
    perm = 49
    t, y = data[:, 50], data[:,perm]
    
    return t.reshape(-1, 1), y


def run_mbqip(data_base_dir='/'):

    simulation_files = sorted(glob.glob("{}/*.csv".format(data_base_dir)))
    ans = []
    for idx, simulation_file in enumerate(simulation_files):

        x = load_and_format_covariates_mbqip(simulation_file)
        t, y = load_all_other_crap(simulation_file)
        print(x[0])
        print(t[0])
        print(y[0])
        est = ForestDRLearner(
                            cv=3,
                            n_estimators=4000,
                            min_samples_leaf=10,
                            verbose=0,
                            min_weight_fraction_leaf=.005)
        est.fit(y,t,X = x,W=None)

        print(est.ate_interval(x))
        f.write(str(est.ate_interval(x)))
        f.close()
        return ans
    return ans

def main():
    run_mbqip("/Users/jiaweizhang/med/dragonnet/dat/mbqip/csv/BMI")

if __name__ == '__main__':
    main()