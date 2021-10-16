# open the excelfile and two different tabs
import pandas as pd

# load the entire excel including all sheets
xlxs = pd.ExcelFile('data/Training_set_full.xlsx')

# read out the sheets
df1 = pd.read_excel(xlxs,'table_of_contents_en-2')
df2 = pd.read_excel(xlxs, 'Training')

# Join id from d1 to df2 by using join function
# df.merge(df1,df2, how='right')
mapping = pd.merge(df1, df2, on="indicator.label")

mapping.to_csv('data/mapping.csv')

# relevant variables
mapping[['id', 'Identification term']]

