import sys
import os

import kagglehub
path = kagglehub.dataset_download("kaggle/us-baby-names")
print("Path to dataset files:", path)

functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'STRV_TEST_PROJECT'))
sys.path.append(functions_path)
import functions

functions.plot_name_occurance_change_over_time(name = 'Ida', dataset = 'National', state = None)

