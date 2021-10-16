import pandas as pd
import urllib
from bs4 import BeautifulSoup

# (0) get all the hyperlinks to the .csv.gz files
URL = 'https://ilo.org/ilostat-files/WEB_bulk_download/html/bulk_indicator.html'
overview = pd.read_html(URL) # links are not present here so we need to parse the actual webpage

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

for file in all_csvgz_files[:2]:
    textfilereader = pd.read_csv(f'https://www.ilo.org{file}', chunksize=1, nrows=1)
    df = next(textfilereader)
    '_'.join(df['classif1'][0].split('_')[:2])


# inverse mapping variable ---> dataframes
d1 = {k:v} # k=id dataset, v:classiv
d2 = {k:[] for k in unique(d1.values) + unique(d0.values)} # key is classif # d0.values=classif2

for k, v in d1:
    d2[v].append(k)



# (1) content based sorting

# (2) create mapping df --> columnnames

# table id!

# (3) create mapping columnnames --> df



# id of a table -- organizing label
# keywords of the already existing table --> build a new label based on that

# each dataset has one or two variable classif1 / 2: they are interested in the unique values of this column.
# --> can we actually get a single column from the dataframe?
# labeling of the tables, based on the values in classif1 and or classif2
# interested in the first two parts of the value in classif
# e.g. AGE_YTHADULT_YGE15 only age_ythadult is relevant
# ---> they are satisfied finding the first