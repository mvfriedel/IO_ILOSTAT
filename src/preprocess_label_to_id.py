# open the excelfile and two different tabs
import json
import pandas as pd

# load the entire excel including all sheets
xlxs = pd.ExcelFile('../data/raw/Training_set_full.xlsx')

# read out the sheets
df1 = pd.read_excel(xlxs, 'table_of_contents_en-2')
df2 = pd.read_excel(xlxs, 'Training')

# Join id from d1 to df2 by using join function
mapping = pd.merge(df1, df2, on="indicator.label")

# write out to csv for a closer look
mapping.to_csv('../data/results/mapping.csv')

# relevant variables
mapping[['id', 'Identification term']]

# create mapping
# https://www.geeksforgeeks.org/how-to-list-values-for-each-pandas-group/
groups = mapping[['id', 'Identification term']].groupby('Identification term')['id'].apply(list)
listgroups = groups.reset_index(name='listvalues') # series object: index: label, value: list of csv_ids

# dictionary comprehension to assign every ID to an Identification term--> key value pair
# label ---> csv_id
label_to_id = {k: v for k, v in listgroups.values}

# Serializing json
json_object = json.dumps(label_to_id, indent = 4)
print(json_object)

# json_object with hrefs:
pattern = 'https://www.ilo.org/ilostat-files/WEB_bulk_download/indicator/{id}.csv.gz'
label_to_id_href = {k: [pattern.format(id=v) for v in list_of_ids] for k, list_of_ids in label_to_id.items()}


#writing the json file to with. 'With' is a context manager.
with open("../data/results/IO_Labels.json", "w") as outfile:
    json.dump(label_to_id, outfile)


print()

#writing the json file to with. 'With' is a context manager including hyperreference
with open("../data/results/label_to_id_href.json", "w") as outfile:
    json.dump(label_to_id_href, outfile)
