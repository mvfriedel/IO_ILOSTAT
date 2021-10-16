# open the excelfile and two different tabs
import pandas as pd

# load the entire excel including all sheets
xlxs = pd.ExcelFile('data/Training_set_full.xlsx')

# read out the sheets
df1 = pd.read_excel(xlxs, 'table_of_contents_en-2')
df2 = pd.read_excel(xlxs, 'Training')

# Join id from d1 to df2 by using join function
mapping = pd.merge(df1, df2, on="indicator.label")

# write out to csv for a closer look
mapping.to_csv('data/mapping.csv')

# relevant variables
mapping[['id', 'Identification term']]

# create mapping
# https://www.geeksforgeeks.org/how-to-list-values-for-each-pandas-group/
groups = mapping[['id', 'Identification term']].groupby('Identification term')['id'].apply(list)
listgroups = groups.reset_index(name='listvalues') # series object: index: label, value: list of csv_ids

# dictionary comprehension to assign every ID to an Identification term--> key value pair
# label ---> csv_id
label_to_id = {k: v for k, v in listgroups.values}
