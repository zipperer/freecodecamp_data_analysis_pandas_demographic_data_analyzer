import pandas as pd

def ratio_to_percentage_rounded_to_one_tenth(ratio):
  percentage = ratio * 100
  percentage_rounded_to_one_tenth = round(percentage, 1)
  return percentage_rounded_to_one_tenth

def calculate_demographic_data(print_data=True):
    # Read data from file
    df = pd.read_csv('adult.data.csv')
  
    # remove duplicates?
    # clean data where 
    # - df['native-country'] == '?'
    # - df['workclass'] == '?'


    # pandas methods used below:
    # get boolean series from dataframe, e.g. df[column_name] == column_value
    # use boolean series to get count of occurrences where df[column_name] == column_value, e.g. boolean_series.sum()
    # use boolean series to filter dataframe, e.g. df[boolean_series]
    # - are (a) df[boolean_series] and (b) df.loc([boolean_series]) equivalent?

    # How many of each race are represented in this dataset? This should be a Pandas series with race names as the index labels.
    race_count = df['race'].value_counts()

    # What is the average age of men?
    # round(df[df['sex'] == 'Male']['age'].mean(), 1)
    sex_is_male_boolean_series = (df['sex'] == 'Male')
    average_age_men = df[sex_is_male_boolean_series]['age'].mean().round(1)

    # What is the percentage of people who have a Bachelor's degree?
    education_is_bachelors_boolean_series = (df['education'] == 'Bachelors')
    count_bachelors = education_is_bachelors_boolean_series.sum()
    count_all = len(df)
    ratio_bachelors = (count_bachelors / count_all)
  
    percentage_bachelors = ratio_to_percentage_rounded_to_one_tenth(ratio_bachelors)

    # What percentage of people with advanced education (`Bachelors`, `Masters`, or `Doctorate`) make more than 50K?
    # What percentage of people without advanced education make more than 50K?

    advanced_education_boolean_series = ((df['education'] == 'Bachelors') |
                                            (df['education'] == 'Masters') |
                                            (df['education'] == 'Doctorate'))
    advanced_education_count = advanced_education_boolean_series.sum()

    without_advanced_education_boolean_series = (~ advanced_education_boolean_series)
    without_advanced_education_count = without_advanced_education_boolean_series.sum()
  
    salary_greater_than_50K_boolean_series = (df['salary'] == '>50K')
  
    advanced_education_and_salary_greater_than_50k_boolean_series = (advanced_education_boolean_series & salary_greater_than_50K_boolean_series)
    advanced_education_and_salary_greater_than_50k_count = advanced_education_and_salary_greater_than_50k_boolean_series.sum()
    ratio_advanced_education_and_salary_greater_than_50K_to_advanced_education = advanced_education_and_salary_greater_than_50k_count / advanced_education_count

    without_advanced_education_and_salary_greater_than_50K_boolean_series = (without_advanced_education_boolean_series & salary_greater_than_50K_boolean_series)
    without_advanced_education_and_salary_greater_than_50K_count = without_advanced_education_and_salary_greater_than_50K_boolean_series.sum()
    ratio_without_advanced_education_and_salary_greater_than_50K_to_without_advanced_education = without_advanced_education_and_salary_greater_than_50K_count / without_advanced_education_count
  
    # with and without `Bachelors`, `Masters`, or `Doctorate`
    higher_education = advanced_education_boolean_series # does spec call for boolean series or dataframe with rows? i.e. df[advanced_education_boolean_series]
    lower_education = without_advanced_education_boolean_series

    # percentage with salary >50K
    higher_education_rich = ratio_to_percentage_rounded_to_one_tenth(ratio_advanced_education_and_salary_greater_than_50K_to_advanced_education)
    lower_education_rich = ratio_to_percentage_rounded_to_one_tenth(ratio_without_advanced_education_and_salary_greater_than_50K_to_without_advanced_education)

    # What is the minimum number of hours a person works per week (hours-per-week feature)?
    min_work_hours = df['hours-per-week'].min()

    # What percentage of the people who work the minimum number of hours per week have a salary of >50K?
    min_workers_boolean_series = (df['hours-per-week'] == min_work_hours)
    min_workers = df[min_workers_boolean_series]
    num_min_workers = len(min_workers)

    min_workers_with_salary_greater_than_50k = (min_workers_boolean_series & salary_greater_than_50K_boolean_series)
    min_workers_with_salary_greater_than_50k_count = min_workers_with_salary_greater_than_50k.sum()

    ratio_min_workers_with_salary_greater_than_50k_to_min_workers = min_workers_with_salary_greater_than_50k_count / num_min_workers
    rich_percentage = ratio_to_percentage_rounded_to_one_tenth(ratio_min_workers_with_salary_greater_than_50k_to_min_workers)

    # What country has the highest percentage of people that earn >50K?
    countries_that_occur_in_dataset_numpy_array = df['native-country'].unique()
    highest_earning_country_so_far = None
    highest_earning_country_percentage_so_far = None
    for country in countries_that_occur_in_dataset_numpy_array:
        people_in_country_boolean_series = (df['native-country'] == country)
        people_in_country_that_earn_greater_than_50K_boolean_series = (people_in_country_boolean_series & salary_greater_than_50K_boolean_series)
        people_in_country_that_earn_greater_than_50K_count = people_in_country_that_earn_greater_than_50K_boolean_series.sum()
        people_in_country_count = people_in_country_boolean_series.sum()
        ratio_people_in_country_that_earn_greater_than_50k_to_people_in_country = people_in_country_that_earn_greater_than_50K_count / people_in_country_count
        percentage_of_people_in_country_that_earn_greater_than_50K = ratio_to_percentage_rounded_to_one_tenth(ratio_people_in_country_that_earn_greater_than_50k_to_people_in_country)
        if ((highest_earning_country_so_far == None) or 
            (percentage_of_people_in_country_that_earn_greater_than_50K > highest_earning_country_percentage_so_far)):
            highest_earning_country_so_far = country
            highest_earning_country_percentage_so_far = percentage_of_people_in_country_that_earn_greater_than_50K

    highest_earning_country = highest_earning_country_so_far
    highest_earning_country_percentage = highest_earning_country_percentage_so_far

    # Identify the most popular occupation for those who earn >50K in India.
    native_country_india_boolean_series = (df['native-country'] == 'India')
    native_country_india_and_earn_more_than_50K_boolean_series = (native_country_india_boolean_series & salary_greater_than_50K_boolean_series)
    native_country_india_and_earn_more_than_50K_series = df[native_country_india_and_earn_more_than_50K_boolean_series]
    native_country_india_and_earn_more_than_50K_occupation_series = native_country_india_and_earn_more_than_50K_series['occupation']
    native_country_india_and_earn_more_than_50K_occupation_series_value_counts = native_country_india_and_earn_more_than_50K_occupation_series.value_counts()
    occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K = None
    occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K_count = None
    for occupation_value, count_with_occupation_value in native_country_india_and_earn_more_than_50K_occupation_series_value_counts.items():
        if ((occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K == None) or
            (count_with_occupation_value > occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K_count)):
            occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K = occupation_value
            occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K_count = count_with_occupation_value            
        
    top_IN_occupation = occupation_with_most_occurrences_among_native_country_india_and_earn_more_than_50K

    # DO NOT MODIFY BELOW THIS LINE

    if print_data:
        print("Number of each race:\n", race_count) 
        print("Average age of men:", average_age_men)
        print(f"Percentage with Bachelors degrees: {percentage_bachelors}%")
        print(f"Percentage with higher education that earn >50K: {higher_education_rich}%")
        print(f"Percentage without higher education that earn >50K: {lower_education_rich}%")
        print(f"Min work time: {min_work_hours} hours/week")
        print(f"Percentage of rich among those who work fewest hours: {rich_percentage}%")
        print("Country with highest percentage of rich:", highest_earning_country)
        print(f"Highest percentage of rich people in country: {highest_earning_country_percentage}%")
        print("Top occupations in India:", top_IN_occupation)

    return {
        'race_count': race_count,
        'average_age_men': average_age_men,
        'percentage_bachelors': percentage_bachelors,
        'higher_education_rich': higher_education_rich,
        'lower_education_rich': lower_education_rich,
        'min_work_hours': min_work_hours,
        'rich_percentage': rich_percentage,
        'highest_earning_country': highest_earning_country,
        'highest_earning_country_percentage':
        highest_earning_country_percentage,
        'top_IN_occupation': top_IN_occupation
    }

calculate_demographic_data(print_data=True)
