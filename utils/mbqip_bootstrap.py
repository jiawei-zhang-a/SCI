from sklearn.base import clone
import os
from mbqip_read_run import run_mbqip
import numpy as np
import copy

def bootstrap(est, PATH, type, task_id):
    estimator_copy = copy.deepcopy(est)
    if os.path.exists("Result") == False:
        os.mkdir("Result")
    if os.path.exists("Result/" + type) == False:
        os.mkdir("Result/" + type)
    result = run_mbqip(estimator_copy, PATH)
    result = np.array(result)
    np.save('Result/%s/risk_%d.npy' % (type, task_id), result)



