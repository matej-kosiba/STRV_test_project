import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random
import os
from sklearn.linear_model import LinearRegression
import plotly.express as px

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
    

def random_most_unisex_name(path_to_NationalNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv", 
                            path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv", 
                            dataset = 'National', 
                            minimum_unisex_score = 0.9, 
                            minimum_name_count = 3000, 
                            printing_the_names = True):
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

def find_common_national_rare_state(path_to_NationalNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv", 
                                    path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv", 
                                    threshold_national = 0.7, 
                                    threshold_state = 0.4, 
                                    sort_by = 'National', 
                                    keep_only_the_lowest_state_per_name = False
                                    ):
    """
    This function finds the most common national names that are also rare at the state level.
    This is done with thresholding, it is looking for names that are higher in their relative occurance (with respect to the most occuring name) on the national level thaan the 'threshold_national'
    and at the same time lower in their relative occurance on the state level than the 'threshold_state'.

    Parameters of the function:
    path_to_NationalNames_dataset - path to the NationalNames dataset
    path_to_StateNames_dataset - path to the StateNames dataset
    threshold_national - threshold for filtering names which have relative commonness (*) higher than this value on the national level 
    threshold_state - threshold to filter names which have relative commonnes on the state level smaller than this value
    sort_by - either 'National' or 'State', defines by which relative comonness should the output list of names be sorted
    keep_only_the_lowest_state_per_name - a True or False parameter, if True, it will keep each name in the list only once, with its lowest record in the relative comonness on the state level
                                                                     if False, it will keep all state entries where the name scored relative comonness on the state level lower than the threshold_state

    (*) relative comonness is defined as a ratio of all name counts with respect to the most occuring name, its value is thus between 1 and 0, where 1 is the most occuring name. 
    This is calculated for national dataset and stored in the column 'Relative_Commonness_National' and separately also for state dataset per state stored in 'Relative_Commonness_State'
    """
    
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

    if sort_by == 'National': # if we want to sort the output by the "Relative_Commonness_National"
        common_national_rare_state_sorted = common_national_rare_state.sort_values(by='Relative_Commonness_National', ascending=False)
    elif sort_by == 'State': # if we want to sort the output by the "Relative_Commonness_State"
        common_national_rare_state_sorted = common_national_rare_state.sort_values(by='Relative_Commonness_State', ascending=False)
    else:
        raise ValueError("Invalid value. The 'sort_by' expects input to be 'National' or 'State'.")
    
    print(common_national_rare_state_sorted[['Name', 'Relative_Commonness_National', 'Relative_Commonness_State', 'State']])

def find_trending_names_by_slope(path_to_NationalNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\NationalNames.csv", 
                                 years_to_analyze=20, 
                                 plot_top_n = 10, 
                                 path_to_results = r"C:\Users\matej\VSCode_projects\STRV_test_project\STRV_test_project\Results", 
                                 plotname_to_save = 'trending_analysis'
                                 ):
    """
    This function fits a linear regression model to measure the slope of change of number of newborns with a certain name over the last 'years_to_analyze' years.
    It is designed to find and print the top 10 trending names in this time period.

    Parameters:
    path_to_NationalNames_dataset - path to the NationalNames dataset
    years_to_analyze - number of years for which we calculate the slope of the trend. It starts from the most recent year.
    plot_top_n - the number off top trending names to plot, default for the task is 10
    path_to_results - path for the directory to which the function saves the plots of the 'plot_top_n' names with lin.reg. fit. X axis are the analyzed years, Y axis is the total count of the newborns with the baby name in a year
    plotname_to_save - starting part of the name of plots for saving, some results of the analysis are added after this starting string 
    """
    df_national = pd.read_csv(path_to_NationalNames_dataset)
    max_year = df_national["Year"].max() # the last year in the dataset
    min_year = max_year - years_to_analyze + 1  # earliest year to include in analysis
    recent_years = list(range(min_year, max_year + 1))  # the list of the years to analyze

    df_filtered = df_national[df_national["Year"] >= min_year] # selecting only the last 'years_to_analyze' years
    df_national = df_filtered.groupby(["Name", "Year"])["Count"].sum().reset_index() # total count of each name in each year across genders
    recent_counts = df_national[df_national["Year"].isin(recent_years)].groupby("Name")["Count"].sum().reset_index() # calculating total occurance of each name in the entire analyzed period --> good for business needs of startup 
    recent_counts.rename(columns={"Count": "Recent_Counts"}, inplace=True)

    name_trends = [] # array for storing the steepness of slope after lin.reg. fitting

    for name, group in df_national.groupby("Name"): # iterating through names
        X = group["Year"].values.reshape(-1, 1)  # X values are  years, reshapen for sklearn
        y = group["Count"].values # y values are counts

        if len(y) < 2:
            continue  # lin.reg. needs at least 2 data points for fitting

        model = LinearRegression() 
        model.fit(X, y) # lin.reg. fitting

        slope = model.coef_.flatten()[0]

        if slope > 0:  # filtering only the positive values of slope, getting rid of highly decreasing names over the insepcted period
            name_trends.append({"Name": name, "Trend_Slope": slope})

    df_trends = pd.DataFrame(name_trends)
    df_trends = df_trends.merge(recent_counts, on="Name", how="left")
    df_trends_sorted = df_trends.sort_values(by="Trend_Slope", ascending=False) # sorting by the steepness 
    top_trending_names = df_trends_sorted.head(plot_top_n).reset_index(drop=True)

    for i, name in enumerate(top_trending_names["Name"]):
        name_data = df_national[(df_national["Name"] == name) & (df_national["Year"] >= min_year)] # selecting only the 'years_to_analyze' years for fitting the lin.reg
        trend_slope = top_trending_names.loc[top_trending_names["Name"] == name, "Trend_Slope"].values[0] # retrieving the slope for a specific name

        X = name_data["Year"].values.reshape(-1, 1)
        y = name_data["Count"].values

        model = LinearRegression() 
        model.fit(X, y) # fitting lin.reg.

        X_pred = np.arange(min(X), max(X) + 1).reshape(-1, 1)
        y_pred = model.predict(X_pred) # predicting the lin.reg. trend

        plt.figure(figsize=(8, 5))
        plt.scatter(X, y, color="blue", label="Count", alpha=0.6)
        plt.plot(X_pred, y_pred, color="red", linestyle="-", label="Linear regression", linewidth=1)
        plt.xticks(np.arange(min(X), max(X) + 1, 1))  # plotting only int. years, not floats
        plt.xlabel("Year")
        plt.ylabel("Count")
        plt.title(f"Trend for {name} over the last {years_to_analyze} years")
        plt.legend()
        save_path = os.path.join(path_to_results, f"{plotname_to_save}_for_past_{years_to_analyze}_years_slope_{trend_slope:.0f}_{name}.png")
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print ('The plot has been saved in the folder Results \n')
        plt.close() 

    print (top_trending_names)

def top_10_states_most_newborns(path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv", 
                                top_N_states = 10
                                ):
    """
    This function loads the StateNames datasets, counts all newborns in each state, sorts states by the number of newborns and prints the top 'top_N_states' states by the number of newborns and the count of newborns.

    Parameters:
    path_to_StateNames_dataset - path to the StateNames dataset
    top_N_states - the number of top states we want to print
    """
    df = pd.read_csv(path_to_StateNames_dataset)
    total_per_state = df.groupby("State")["Count"].sum().reset_index() # number of all newborns per state
    top_states = total_per_state.sort_values(by="Count", ascending=False).head(top_N_states).reset_index(drop=True) # sorts states by the number of all newborns, keeps the top 'top_N_states' and resets the original indexes by the new order
    
    print(top_states)

def plot_top_names_by_state(path_to_StateNames_dataset = r"C:\Users\matej\.cache\kagglehub\datasets\kaggle\us-baby-names\versions\2\StateNames.csv"):
    """
    This function craetes a choropleth map of the USA where each state is colored by the most popular baby name in that state.

    Parameters:
    file_path - path to the StateNames dataset
    """
    df = pd.read_csv(path_to_StateNames_dataset)
    top_names = df.groupby(["State", "Name"])["Count"].sum().reset_index() #sums all occurances of the same baby name in the same state across all years,  .groupby converts the data frame to a grouped object, .reset_index converts it back
    top_names = top_names.loc[top_names.groupby("State")["Count"].idxmax()]  # creates a grouped object - grouping states together, .idmax finds the index of the maximum count (done for each state), finally .loc makes a subsample of rows corresponding to the most occuring baby names per state
    
    # Create map visualization
    fig = px.choropleth(
        top_names,
        locations="State",
        locationmode="USA-states",
        color="Name", # coloring states by the most popular name
        hover_name="Name", # displays the most popular baby name of the state when hovering over it with a coursor
        hover_data={"State": True, "Name": True, "Count": True}, # additional data shown when hovering over
        title="Most Popular Baby Names by State",
        scope="usa", # defines the map to be only USA
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    fig.show()