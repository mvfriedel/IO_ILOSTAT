import pandas as pd
import urllib
import json
from bs4 import BeautifulSoup

# (0) get all the hyperlinks to the .csv.gz files
URL = 'https://ilo.org/ilostat-files/WEB_bulk_download/html/bulk_indicator.html'
overview = pd.read_html(URL)  # links are not present here so we need to parse the actual webpage

# get the html code of the table from URL
page = urllib.request.urlopen(URL).read()

# parse that page
soup = BeautifulSoup(page, "html.parser")

# find all hyperlinks in the table
all_hrefs = [tag.find("a")["href"] for tag in soup.select("td:has(a)")]

# keep only those that have ".csv.gz" ending
# looking at the table, we instead simply could drop the first three entries of the list
all_csvgz_files = [link.rstrip() for link in all_hrefs if link.endswith(".csv.gz ")]

# Example to lazily load a single row from that dataframe - without downloading the entire thing
file = all_csvgz_files[0]
textfilereader = pd.read_csv(f'https://www.ilo.org{file}', chunksize=2, nrows=6)
# textfilereader is a generator object
df = next(textfilereader)

# classif1 --> id
classif_id = {}

# id ---> classif1
id_classif = {}
for file in all_csvgz_files:
    textfilereader = pd.read_csv(f'https://www.ilo.org{file}', chunksize=1, nrows=1)
    df = next(textfilereader)

    if 'classif1' in df.keys():
        k = '_'.join(df['classif1'][0].split('_')[:2])
        v = file.split('/')[-1][:-len('.csv.gz')]

        if k not in classif_id.keys():
            classif_id[k] = [v]
        else:
            classif_id[k].append(v)

        if v not in id_classif.keys():
            id_classif[v] = [k]
        else:
            id_classif[v].append(k)

    if 'classif2' in df.keys():
        k = '_'.join(df['classif2'][0].split('_')[:2])
        v = file.split('/')[-1][:-len('.csv.gz')]

        if k not in classif_id.keys():
            classif_id[k] = [v]
        else:
            classif_id[k].append(v)

        if v not in id_classif.keys():
            id_classif[v] = [k]
        else:
            id_classif[v].append(k)

# writing the json file to with. 'With' is a context manager.
with open("../data/results/classif_to_id.json", "w") as outfile:
    json.dump(classif_id, outfile)

with open("../data/results/id_to_classif.json", "w") as outfile:
    json.dump(id_classif, outfile)


pattern = 'https://www.ilo.org/ilostat-files/WEB_bulk_download/indicator/{id}.csv.gz'
id_classif_href = {k: [pattern.format(id=v) for v in list_of_ids] for k, list_of_ids in id_classif.items()}
classif_id_href = {k: [pattern.format(id=v) for v in list_of_ids] for k, list_of_ids in classif_id.items()}

with open("../data/results/id_to_classif_href.json", "w") as outfile:
    json.dump(id_classif_href, outfile)

with open("../data/results/to_classif_id_href.json", "w") as outfile:
    json.dump(classif_id_href, outfile)






# id of a table -- organizing label
# keywords of the already existing table --> build a new label based on that

# each dataset has one or two variable classif1 / 2: they are interested in the unique values of this column.
# --> can we actually get a single column from the dataframe?
# labeling of the tables, based on the values in classif1 and or classif2
# interested in the first two parts of the value in classif
# e.g. AGE_YTHADULT_YGE15 only age_ythadult is relevant
# ---> they are satisfied finding the first
