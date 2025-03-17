import sys
import os
import kagglehub
path = kagglehub.dataset_download("kaggle/us-baby-names")
print ()
print("Path to dataset files:", path)
functions_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'STRV_TEST_PROJECT'))
sys.path.append(functions_path)
import functions

path_to_results = r"C:\Users\matej\VSCode_projects\STRV_test_project\STRV_test_project\Results"
path_to_NationalNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv"
path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv"
print ()
print (' -----------------------------------------------------')
print ('Exploring the fundamentals of the datasets')
functions.check_year_span(file_path = path_to_NationalNames_dataset, 
                          dataset_name = 'NationalNames'
                          )
functions.check_year_span(file_path = path_to_StateNames_dataset, 
                          dataset_name = 'StateNames'
                          )
print ()
print (' -----------------------------------------------------')
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
print ()
print (' -----------------------------------------------------')
print ('Explore the dataset, task 2. How did the name Ida change period-over-period in California?')
functions.plot_name_occurance_change_over_time(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                               path_to_StateNames_dataset = path_to_StateNames_dataset, 
                                               name = 'Ida', 
                                               dataset = 'State', 
                                               state = 'CA', 
                                               path_to_results = path_to_results, 
                                               plotname_to_save = 'Ida_change_over_time_state_CA'
                                               )
print ()
print (' -----------------------------------------------------')
print ('Explore the dataset, task 3. What name is the most unisex?')
functions.random_most_unisex_name(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                  path_to_StateNames_dataset = path_to_StateNames_dataset,
                                  dataset = 'National', 
                                  minimum_unisex_score = 0.8,  
                                  minimum_name_count = 10000, 
                                  printing_the_names = True
                                  )
print ()
print (' -----------------------------------------------------')
print ('Explore the dataset, task 4. Which names are common nationally but rare at the state level?')
functions.find_common_national_rare_state(path_to_NationalNames_dataset = path_to_NationalNames_dataset, 
                                          path_to_StateNames_dataset = path_to_StateNames_dataset,
                                          threshold_national=0.75, 
                                          threshold_state=0.65, 
                                          sort_by='State', 
                                          keep_only_the_lowest_state_per_name=True
                                          )
print ()
print (' -----------------------------------------------------')
print ('Presentation task 1. Find the TOP 10 trending names')

functions.find_trending_names_by_slope(path_to_NationalNames_dataset = path_to_NationalNames_dataset,
                                       years_to_analyze=3, 
                                       plot_top_n = 10,
                                       path_to_results = path_to_results,
                                       plotname_to_save = 'trending_analysis'
                                       )
print ()
print (' -----------------------------------------------------')
print ('Presentation task 2. Find the TOP 10 states with the most newborns')
functions.top_10_states_most_newborns(path_to_StateNames_dataset = path_to_StateNames_dataset, 
                                      top_N_states = 10
                                      )
print ()
print (' -----------------------------------------------------')
print ('Presentation task 3. Make a map of the USA showing the top names by state')
functions.plot_top_names_by_state(path_to_StateNames_dataset)