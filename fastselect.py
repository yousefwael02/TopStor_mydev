#!/usr/bin/python3
import pandas as pd
import numpy as np
# Define a function to operate on elements
def operate(df1row,df2row):
 res = []
 for i in df1row:
    for k in df2row:
        res.append(feature_calc(i,k))
 return res   

hosts = set()
disktypes = set()
mindisksize = 0
def feature_calc(i, k):
    global hosts, disktypes, mindisksize
    if i[1] > k[1] or i[0] == k[0] or i[0] in k[0] or k[0] in i[0] or i[2] == float('inf') or k[2] == float('inf'):
        return [i[0]+','+k[0],i[1],float('inf')]
    else:
        if i[1] > 9 and i[1] < 100:  # disk hosts test
            hosts.add(i[2])
            if ',' not in k[0]:
                hosts.add(k[2])
            combineddisks = k[0]+','+i[0]
            disksn = combineddisks.count(',')+1
            hostsn = len(hosts)
            if hostsn < disksn:
               return [combineddisks,i[1],i[1]+1]
            elif ',' in k[0]:
                if k[2] < i[1]:
                    return [combineddisks,i[1],i[1]+k[2]+1]
                else:
                    return [combineddisks,i[1],k[2]+1]
            else: 
                  return [combineddisks,i[1],0]
        if i[1] > 99 and i[1] < 1000:  # disk type
            disktypes.add(i[2])
            if ',' not in k[0]:
                disktypes.add(i[2])
            if len(disktypes) > 1:
                  return [i[0]+','+k[0],i[1],inf]
            else:
                  return [i[0]+','+k[0],i[1],0]
        if i[1] > 0 and i[1] < 11: # disk sizes test 
            if int(i[2]) == mindisksize: 
                if ',' not in k[0] and k[2] == mindisksize:
                    return [i[0]+','+k[0],i[1],0]
                elif ',' not in k[0] and k[2] > mindisksize:
                    return [i[0],','+k[0],i[1],i[1]+1]
                elif ',' in k[0]:
                    return [i[0],','+k[0],i[1],k[2]]
            elif i[2] > mindisksize:
                if ',' not in k[0] and k[2] == mindisksize:
                    return [i[0]+','+k[0],i[1],i[1]+1]
                elif ',' not in k[0] and k[2] > mindiskize:
                    return [i[0],','+k[0],i[1],float('inf')]
                elif ',' in k[0]:
                    return [i[0],','+k[0],i[1],k[2]+2]
            else:
                return [i[0],','+k[0],i[1],float('inf')]
            if ',' not in k[0] and k[2] < mindisksize:
                return [i[0],','+k[0],i[1],float('inf')]
            
                
def combine_features(column_values):
    ccolumn_values = column_values.tolist()
    return (ccolumn_values[0][0],ccolumn_values[0][1],float(ccolumn_values[0][2])+float(ccolumn_values[1][2])+float(ccolumn_values[2][2]))
# Define the 10 element
elements = []
result_df = pd.DataFrame()
val1 = []
val2 = []
val3 = []
for x in range(0,4):
  val1.append(['d'+str(x),x+1,0])
  val2.append(['d'+str(x),(x+1)*10,2])
  val3.append(['d'+str(x),(x+1)*100,0])
elements.append(val1)
elements.append(val2)
elements.append(val3)
column_names=['d0','d1','d2','d3']
df = pd.DataFrame(elements)
count = 3 
result_df = df
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print('#############################33')
print(df)
print('#############################33')
for c in range(1,count):
    result_data = [operate(row1, row2) for row1, row2 in zip(df.values, result_df.values)]
    result_df = pd.DataFrame(result_data) 
new_row = result_df.apply(lambda x: combine_features(x),axis=0)
print(new_row.apply(list))
exit()
result_df = pd.DataFrame(result_data,columns=result_df.columns)
print(result_df)
exit()
#filtered_df = result_df[result_df.apply(lambda x: any(str(item[2]) == 'inf' for item in x), axis=0)].dropna()
newdf  = result_df.apply(lambda x: [item[2] < float('inf') for item in x])
print(result_df[newdf])

# Print the result DataFrame
