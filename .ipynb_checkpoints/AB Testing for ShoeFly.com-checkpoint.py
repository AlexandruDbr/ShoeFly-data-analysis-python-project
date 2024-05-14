

# 8. Using the column is_click that we defined earlier, check to see which percentage of users clicked on Ad A or Ad B.

# 9.The Product Manager for the A/B test thinks that the clicks might have changed by day of the week.

# Start by creating two DataFrames: a_clicks and b_clicks, which contain only the results for A group and B group, respectively.

# 10.For each group (a_clicks and b_clicks), calculate the percent of users who clicked on the ad by day.

# 11.Compare the results for A and B. What happened over the course of the week?
# Do you recommend that your company use Ad A or Ad B?


import pandas as pd
import os
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# -- Part 1: Data wrangling

script_path = os.path.curdir #directory where the script is run.
rel_path = "ad_clicks.txt"
filepath = os.path.join(script_path, rel_path) #create file path

ad_clicks = pd.read_csv(filepath) # store df in a file

#1. Inspect the first 10 lines of the csv
print(ad_clicks.head(10))
print(ad_clicks.columns.tolist()) # print all the headers of this file


#2. Count the number of users per platform
views_per_utm_source = ad_clicks.groupby('utm_source').user_id.count().reset_index()
views_per_utm_source.rename(columns={'user_id':'count_user'}, inplace=True)

print(views_per_utm_source)


#3. Add a new column "day number" based on "day" column and delete anything before day name
ad_clicks['day_nr'] = ad_clicks['day'].str.split('-').str[0] #add new column
ad_clicks['day'] = ad_clicks['day'].str.split(' -').str[-1] #get the day name
print(ad_clicks.head(10))


#4. Create a new column called "is_click" to check the nr. of users who clicked the ad. If ad_click_timestamp is not null, True, else False.
ad_clicks['is_click'] = ad_clicks.ad_click_timestamp.isnull()


# 5. Management team wants to know the percent of people who clicked on ads from each utm_source.
# Group utm_source and is_click and count the adds on which users clicked or not. Save your answer to the variable clicks_by_source.
clicks_by_source = ad_clicks.groupby(['utm_source','is_click']).user_id.count().reset_index()
clicks_by_source.rename(columns={'user_id':'count_user_id'}, inplace=True) # change user_id column name

print(clicks_by_source)


#6. Create a new dataframe with rows as "utm_source", columns "is_click" and count_user_id as values
# Save the results to the variable clicks_pivot.
clicks_pivot = clicks_by_source.pivot(columns='is_click', index='utm_source', values='count_user_id').reset_index()
print(clicks_pivot)


#7. Create a column to show the percentage of users who clicked the ad per utm_source.
clicks_pivot['percent_clicked'] = round((clicks_pivot[True]/(clicks_pivot[True]+clicks_pivot[False]) * 100), 2)
print("\n", clicks_pivot)




# -- Part 2: Analyzing an A/B Test

#7. Create a table to show the number of users who were targeted for add A and add B
# Answer: There are the same number of people targeted in both adds
check_experimental = ad_clicks.groupby('experimental_group').is_click.count().reset_index()
print(check_experimental)


#8. Create 2 tables: a_clicks and b_clicks by filtering column 'experimental_group' (target group)
a_clicks = ad_clicks[ad_clicks.experimental_group == 'A'].reset_index()
b_clicks = ad_clicks[ad_clicks.experimental_group == "B"].reset_index()
print(a_clicks, '\n')
print(b_clicks)


#9. Group the a_clicks and b_clicks by day and count the total users
a_clicks_grouped = a_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()
b_clicks_grouped = b_clicks.groupby(['day', 'is_click']).user_id.count().reset_index()


#11. Rename user_id column as count_clicks
a_clicks_grouped.rename(columns= {'user_id':'count_clicks'},inplace=True)
b_clicks_grouped.rename(columns= {'user_id':'count_clicks'},inplace=True)


#12. Pivot is_click as columns and count(user_id) as values
a_clicks_pivot = a_clicks_grouped.pivot(columns = 'is_click', values ='count_clicks', index ='day').reset_index()
b_clicks_pivot = b_clicks_grouped.pivot(columns = 'is_click', values ='count_clicks', index ='day').reset_index()


#13. Add percentage column, check final result and save the files last 4 dataframes locally
a_clicks_pivot['percentage_clicked'] = round(a_clicks_pivot[True]/(a_clicks_pivot[False] + a_clicks_pivot[True])*100)
b_clicks_pivot['percentage_clicked'] = round(b_clicks_pivot[True]/(b_clicks_pivot[False] + b_clicks_pivot[True])*100)


# Check final result
print(a_clicks_pivot,"\n")
print(b_clicks_pivot)

# Save csv files
a_clicks.to_csv(os.curdir + r"\a_clicks.csv")
b_clicks.to_csv(os.curdir + r"\b_clicks.csv")

a_clicks_pivot.to_csv(os.curdir +r"\a_clicks_by_day_final.csv")
b_clicks_pivot.to_csv(os.curdir + r"\b_clicks_by_day_final.csv")
