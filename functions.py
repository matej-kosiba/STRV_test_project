import pandas as pd
import matplotlib.pyplot as plt
import random
import os

def check_year_span(file_path, dataset_name):
    """
    This function loads a text file of the chosen dataset and prints the range of recorded years.
    Parameters:
    file_path - path to the dataset
    dataset_name - just for the printing purposes, the name of the dataset
    """
    df = pd.read_csv(file_path)
    min_year = df["Year"].min()
    max_year = df["Year"].max()
    print ()
    #print(f"Dataset: {file_path}")
    print(f"Year span of dataset {dataset_name}: {min_year} - {max_year}\n")

def average_occurrence_in_time_period_national(path_to_NationalNames_dataset, name, start_year, end_year):
    """
    This function calculates the average number of newborns (average occurance) and the maximum number of newborns in one year 
    for a given period of years defined by the start_year and the end_year in the national dataset

    It has 4 arameters:
    file_path - path to the dataset
    name - the newborn name of interest
    start_year - the year from which we want to start monitoring the period of interest
    end_year - the last year for which we want to monitor the period of interest
    """
    df = pd.read_csv(path_to_NationalNames_dataset)
    df_filtered = df[(df["Name"] == name) & (df["Year"] >= start_year) & (df["Year"] <= end_year)] # filters only the data of the input name between the start_year and end_year
    total_occurrences = df_filtered["Count"].sum() # calculates the total number of babies born with the input name in the period between start_year and end_year
    num_years = end_year - start_year + 1 # calculates the number of years in the period specified by start_year and end_year
    average_occurance = total_occurrences / num_years if num_years > 0 else 0 # calculates the average occurance of newborns per year in the desired time period

    if not df_filtered.empty:
        max_row = df_filtered.loc[df_filtered["Count"].idxmax()] # id of the row with the year of the highest count of newborns in the given time period
        max_yearly_occurrence = max_row["Count"] # the largest number of newborns with the given name in the given time period in a year
        max_year = max_row["Year"] # the year in which the peak occurance was recorded
    else:
        max_yearly_occurrence = 0
        max_year = None  # if there is no maximum year recorded

    print(f"Average yearly occurrence of '{name}' from {start_year} to {end_year} is {average_occurance:.2f}")
    print(f"Maximum yearly occurrence of '{name}' in this period is {max_yearly_occurrence} (occurred in {max_year})")

def plot_name_occurance_change_over_time(path_to_NationalNames_dataset, path_to_StateNames_dataset, name, dataset, state, path_to_results, plotname_to_save):
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
    if dataset == 'National':
        file_path_NationalNames = path_to_NationalNames_dataset
        df_NationalNames = pd.read_csv(file_path_NationalNames)

    if dataset == 'State':
        file_path_StateNames = path_to_StateNames_dataset
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
    # it starts either at the first year of the national dataset, 1880 or the first year of the state dataset, which is 1910
    plt.tight_layout()
    save_path = os.path.join(path_to_results, f"{plotname_to_save}.png")
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    print ('The plot has been saved in the folder Results \n')
    plt.close() 
    

def random_most_unisex_name(path_to_NationalNames_dataset, path_to_StateNames_dataset, dataset, minimum_unisex_score, minimum_name_count, printing_the_names):
    """
    This function calculates the unisexness of names, the unisex_score, U = min(F, M) / max(F, M), 
    where F is the count of females born with the name and M is the count of males born with the name.
    U is a float number between 1 (most unisex name, F = M) and 0.

    This function has following 4 parameters:
    dataset - chooosing which dataset we work with, either 'National' or 'State'
    minimum_unisex_score - parameter defining the minimum unisex_score, to screen out names of low unisex_score
    minimum_name_count - parameter defining the minimum number of TOTAL names assigned for the baby. It is used to filter out low occuring names
    printing_the_names - if set to True, it prints the resulted filtered unisex names based on our input parameters

    The function prints the list of names with U > minimum_unisex_score and count of newborn > minimum_name_count if the parameter printing_the_names == True.
    --> this is used for the project's task to find the most unisex name
    --> it also prints directly the most unisex name from this list
    In any case of the printing_the_names selection, the function always returns a random name from the list of most unisex names selected based on the input parameters.
    --> this would be used for the startup's needs to help clients generate a random name with a high unisex score.
    """
    
    if dataset == 'National':
        df_Names = pd.read_csv(path_to_NationalNames_dataset)

    if dataset == 'State':
        df_Names = pd.read_csv(path_to_StateNames_dataset)

    name_gender_counts = df_Names.groupby(["Name", "Gender"])["Count"].sum().unstack(fill_value=0) # makes a 2 column table, name of the baby, female count, male count
    name_gender_counts["Total"] = name_gender_counts["M"] + name_gender_counts["F"] # computes the total number of names, of each gender and adds as a new column to the 2 column table created above
    name_gender_counts["Unisex_score"] = name_gender_counts[["M", "F"]].min(axis=1) / name_gender_counts[["M", "F"]].max(axis=1) # finds for each pair of female and male occurances per name their minimum and maximum value and calculates their ratio.
    
    unisex_names = name_gender_counts[
        (name_gender_counts["M"] > 0) & 
        (name_gender_counts["F"] > 0) & 
        (name_gender_counts["Unisex_score"] >= minimum_unisex_score) & 
        (name_gender_counts["Total"] >= minimum_name_count)
    ] # filters only names within defined tresholds

    unisex_names_sorted = unisex_names.sort_values(by=["Total", "Unisex_score"], ascending=[False, False]) # sorts the selected list by the total number of names (count) and for the names with the same count by the Unisex_score
    if printing_the_names == True:
        print(unisex_names_sorted)
    print ('The most Unisex name is', unisex_names_sorted.index[0])
    random_name = random.choice(unisex_names_sorted.index.tolist())
    return (random_name)

def find_common_national_rare_state(path_to_NationalNames_dataset, path_to_StateNames_dataset, threshold_national=0.7, threshold_state=0.4, sort_by='national', keep_only_the_lowest_state_per_name=False):
    
    df_national = pd.read_csv(path_to_NationalNames_dataset)
    df_national_summary = df_national.groupby("Name")[["Count"]].sum().reset_index() # groups dataset by name and sums all counts of each name, converts back to a pandas dataframe
    max_count = df_national_summary["Count"].max() # finds the largest value in the count column --> corresponding to the most common name on national level
    df_national_summary["Relative_Commonness_National"] = (df_national_summary["Count"] / max_count) # for each name, calculates the ratio of its total count on national level over all years with the largest count of the most occuring name
    
    df_state = pd.read_csv(path_to_StateNames_dataset)
    df_state_summary = df_state.groupby(["State", "Name"])["Count"].sum().reset_index() # groups dataset by state and name, sums all counts over years for the same name in a particular state, reset_index converts back to pd.df
    df_state_summary["Max_Count_State"] = df_state_summary.groupby("State")["Count"].transform("max") # groups dataset by state, finds the largest value in the count column for each state and stores it as a new column --> the most common name per state
    df_state_summary["Relative_Commonness_State"] = df_state_summary["Count"] / df_state_summary["Max_Count_State"] # creates a new column "Relative_Commonness_State" which is the ratio of a name's count to the most common name's count in that particular state

    df_final = df_state_summary.merge(df_national_summary, on="Name", how="left", suffixes=("_State", "_National")) # putting the national and state data together so the statistics can be compared

    common_national_rare_state = df_final[(df_final["Relative_Commonness_National"] >= threshold_national) & # filters only names ABOVE the treshold_national
                                          (df_final["Relative_Commonness_State"] <= threshold_state)] # filters only names BELOW the treshold_state

    if keep_only_the_lowest_state_per_name == True: # If we want to monitor each name uniquely, so they do not repeat if low in multiple states and instead keeping only their lowest state
        common_national_rare_state = common_national_rare_state.loc[common_national_rare_state.groupby("Name")["Relative_Commonness_State"].idxmin()]

    if sort_by == 'national': # if we want to sort the output by the "Relative_Commonness_National"
        common_national_rare_state_sorted = common_national_rare_state.sort_values(by='Relative_Commonness_National', ascending=False)
    elif sort_by == 'state': # if we want to sort the output by the "Relative_Commonness_State"
        common_national_rare_state_sorted = common_national_rare_state.sort_values(by='Relative_Commonness_State', ascending=False)
    else:
        raise ValueError("Invalid value. The 'sort_by' expects input to be 'national' or 'state'.")
    
    print(common_national_rare_state_sorted[['Name', 'Relative_Commonness_National', 'Relative_Commonness_State', 'State']])
