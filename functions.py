import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

def plot_name_occurance_change_over_time(name, dataset, state):
    """
    This function plots a histogram of occurances of a selected name from a selected dataset over the years of monitoring.
    It has 3 parameters:
    name - defines the name of a baby to monitor, expects a string
    dataset - defines the dataset to scan through, expected input is a string either 'National' or 'State'
    state - relevant only if dataset = 'State' and only if we want to monitor name occurances restricted to a single state.
            It expects a string input of the state abbreviation. Here is the list of all possible inputs:
            AK, AL, AR, AZ, CA, CO, CT, DC, DE, FL, GA, HI, IA, ID, IL, IN, KS, KY, LA, MA, MD, ME, MI, MN, MO, MS, MT,
            NC, ND, NE, NH, NJ, NM, NV, NY, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VA, VT, WA, WI, WV, WY.
            Or a None input if we do not want to narrow the statistics for a single state.
    """
    file_path_NationalNames = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv"
    df_NationalNames = pd.read_csv(file_path_NationalNames)

    file_path_StateNames = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv"
    df_StateNames = pd.read_csv(file_path_StateNames)

    plt.figure(figsize=(10, 6))

    if dataset == 'National':
        name_occurances = df_NationalNames[df_NationalNames["Name"] == name] # selecting all occurances of the chosen name
        name_count_per_year = name_occurances.groupby("Year")["Count"].sum() # counting for each year how many times the chosen name was given to a baby
        plt.title('Occurrences of the name %s over the years' % (name), fontsize=14)


    if dataset == 'State':
        if state is None:
            name_occurances = df_StateNames[df_StateNames["Name"] == name] # selecting all occurances of the chosen name
            name_count_per_year = name_occurances.groupby("Year")["Count"].sum() # counting for each year how many times the chosen name was given to a baby
            plt.title('Occurrences of the name %s over the years' % (name), fontsize=14)

        if state != None:    
            name_occurances = df_StateNames[(df_StateNames["Name"] == name) & (df_StateNames["State"] == state)] # selecting all occurances of the chosen name in the chosen state
            name_count_per_year = name_occurances.groupby("Year")["Count"].sum() # counting for each year how many times the chosen name in the chosen state was given to a baby
            plt.title('Occurrences of the name %s over the years in the state %s' % (name, state), fontsize=14)

    
    plt.bar(name_count_per_year.index, name_count_per_year.values, color='lightblue', edgecolor='black')
    plt.xlabel('Year', fontsize=12)
    plt.ylabel('Number of Occurrences', fontsize=12)
    plt.xticks(ticks=range(min(name_count_per_year.index), max(name_count_per_year.index)+1, 10), rotation=45) # X-axis showing years per decade, rotated by 45 degrees
    # it starts either at the first year of the national dataset, 1880 or the first year of the state dataset, which is 1920
    plt.tight_layout()
    plt.show()

