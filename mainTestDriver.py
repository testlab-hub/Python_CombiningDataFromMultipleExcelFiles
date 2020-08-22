import pandas as pd
import numpy as np
import glob

# https://pbpython.com/excel-file-combine.html
# Use the python glob module to easily list out the files we need
# print(glob.glob("sales*.xlsx"))

# The code snippet below will initialize a blank DataFrame then append all of the individual files into the all_data DataFrame
all_data = pd.DataFrame ( )
for f in glob.glob ("sales*.xlsx"):
    df = pd.read_excel (f)
    all_data = all_data.append (df, ignore_index=True)

# Now we have all the data in our all_data DataFrame. You can use describe to look at it and make sure you data looks good.
all_data.describe ( )
all_data.head ( )
# convert the date column to a date time object
all_data['date'] = pd.to_datetime (all_data['date'])

status = pd.read_excel ("customer-status.xlsx")

# merge this data with our concatenated data set of sales
all_data_st = pd.merge (all_data, status, how='left')
all_data_st.head ( )

all_data_st[all_data_st["account number"] == 737550].head ( )

all_data_st['status'].fillna ('bronze', inplace=True)
console_1 = all_data_st.head ( )
print (console_1)
print ("Console 1 \END ===========================================================\n")

console_2 = all_data_st[all_data_st["account number"] == 737550].head ( )
print (console_2)
print ("Console 2 \END ===========================================================\n")

# USING CATEGORIES
all_data_st["status"] = all_data_st["status"].astype ("category")
all_data_st.head ( )
# print(all_data_st.dtypes)

# Categories get more interesting when you assign order to the categories.
# Right now, if we call sort on the column, it will sort alphabetically
all_data_st.sort_values (by="status").head ( )

all_data_st["status"].cat.set_categories (["gold", "silver", "bronze"], inplace=True)
console_3 = all_data_st.sort_values (by="status").head ( )
print (console_3)
print ("Console 3 \END ===========================================================\n")

# Quick look
all_data_st["status"].describe ( )
all_data_st.groupby (["status"])[["quantity", "unit price", "ext price"]].mean ( )

# multiple aggregation functions on the data to get really useful information
console_4 = all_data_st.groupby (["status"])[["quantity", "unit price", "ext price"]].agg ([np.sum, np.mean, np.std])
print (console_4)
print ("Console 4 \END ===========================================================\n")

console_5 = all_data_st.drop_duplicates (subset=["account number", "name"]).iloc[:, [0, 1, 7]].groupby (["status"])[
    "name"].count ( )
print (console_5)
print ("Console 5 \END ===========================================================\n")
