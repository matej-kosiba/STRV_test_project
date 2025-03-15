import sys
import os

import kagglehub
path = kagglehub.dataset_download("kaggle/us-baby-names")
print("Path to dataset files:", path)

functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'STRV_TEST_PROJECT'))
sys.path.append(functions_path)
import functions

path_to_results = r"C:\Users\matej\VSCode_projects\STRV_test_project\STRV_test_project\Results"
path_to_NationalNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv"
path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv"

print ('Exploring the fundamentals of the datasets')
functions.check_year_span(path_to_NationalNames_dataset, 'NationalNames')
functions.check_year_span(path_to_StateNames_dataset, 'StateNames')

print ('Explore the dataset, task 1. How did the name Ida change period-over-period nationally?')
functions.plot_name_occurance_change_over_time(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                               path_to_StateNames_dataset = path_to_StateNames_dataset, 
                                               name = 'Ida', 
                                               dataset = 'National', 
                                               state = None, 
                                               path_to_results = path_to_results, 
                                               plotname_to_save = 'Ida_change_over_time_national'
                                               ) 

functions.average_occurrence_in_time_period_national(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                                     name = "Ida", 
                                                     start_year = 1910, 
                                                     end_year = 1930
                                                     ) # just to get some statistics for the documentation

print ('Explore the dataset, task 2. How did the name Ida change period-over-period in California?')
functions.plot_name_occurance_change_over_time(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                               path_to_StateNames_dataset = path_to_StateNames_dataset, 
                                               name = 'Ida', 
                                               dataset = 'State', 
                                               state = 'CA', 
                                               path_to_results = path_to_results, 
                                               plotname_to_save = 'Ida_change_over_time_state_CA'
                                               )

print ('Explore the dataset, task 3. What name is the most unisex?')
functions.random_most_unisex_name(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                  path_to_StateNames_dataset = path_to_StateNames_dataset,
                                  dataset = 'National', 
                                  minimum_unisex_score = 0.8,  
                                  minimum_name_count = 10000, 
                                  printing_the_names = False
                                  )

print ('Explore the dataset, task 4. Which names are common nationally but rare at the state level?')
functions.find_common_national_rare_state(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                          path_to_StateNames_dataset = path_to_StateNames_dataset,
                                          threshold_national=0.75, 
                                          threshold_state=0.65, 
                                          sort_by='state', 
                                          keep_only_the_lowest_state_per_name=True
                                          )

