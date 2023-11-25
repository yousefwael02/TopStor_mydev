#!/usr/bin/python3
import pandas as pd

def feature_calc( i, j, k, row_element, df2_element):
    if k < j:
        return row_element + df2_element
    else:
        return 'inf'
# Define the 10 element
elements = []
result_df = pd.DataFrame()
val1 = []
val2 = []
val3 = []
for x in range(0,4):
  val1.append('x'+str(x))
  val2.append('y'+str(x))
  val3.append('z'+str(x))
elements.append(val1)
elements.append(val2)
elements.append(val3)
print(elements)
column_names=['d0','d1','d2','d3']
df = pd.DataFrame(elements,columns=column_names)
print(df.shape)
print(len(df))
# Enumerate over rows of df1
for i, row in df.iterrows():
    new_row_element = row.copy()
    # Add each element of the current row to each element of the corresponding row in df2
    for j in range(0,df.shape[1]):
        for k in range(0,df.shape[1]):
        # Apply specific functions based on element location
            new_row_element[k] = feature_calc( i, j , k, row[k], row[j])

        # Create a new row with the new element and append it to the result DataFrame
        result_df = result_df.append(new_row_element, ignore_index=True)

# Print the result DataFrame
print(df)
print(result_df)
