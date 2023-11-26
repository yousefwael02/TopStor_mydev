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

combinations = dict()
hosts = set()
disktypes = set()
disks = {'disk': 10.7, 'diskcount': 2, 'others': [64.4], 'hosts': ['dhcp876810'], 'othershosts': ['dhcp876810', 'dhcp273302']}
singles = {64.4: ['scsi-360014055908817040aa494cad2a26f03', 'scsi-36001405a430c5a307ff4cb99fea2c1f7'], 10.7: ['scsi-3600140538872a6d8e85460999d74f2ad', 'scsi-36001405b319164f4d1841e585cd61bc0']}
disksinfo = {'scsi-36001405cbd12826748b4091aa5d856ea': {'name': 'scsi-36001405cbd12826748b4091aa5d856ea', 'actualdisk': 'scsi-36001405cbd12826748b4091aa5d856ea', 'changeop': 'ONLINE', 'pool': 'pdhcp728726367', 'raid': 'mirror-0_pdhcp728726367', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp876810', 'size': 64.4, 'devname': 'scsi-36001405cbd12826748b4091aa5d856ea', 'silvering': 'no'}, 'scsi-36001405596cc7d753b1400291ebbb673': {'name': 'scsi-36001405596cc7d753b1400291ebbb673', 'actualdisk': 'sdd', 'changeop': 'ONLINE', 'pool': 'pdhcp728726367', 'raid': 'mirror-0_pdhcp728726367', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp273302', 'size': 64.4, 'devname': 'sdd', 'silvering': 'no'}, 'scsi-360014055908817040aa494cad2a26f03': {'name': 'scsi-360014055908817040aa494cad2a26f03', 'actualdisk': 'scsi-360014055908817040aa494cad2a26f03', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '1', 'host': 'dhcp273302', 'size': 64.4, 'devname': 'sdg', 'silvering': 'no'}, 'scsi-3600140538872a6d8e85460999d74f2ad': {'name': 'scsi-3600140538872a6d8e85460999d74f2ad', 'actualdisk': 'scsi-3600140538872a6d8e85460999d74f2ad', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '2', 'host': 'dhcp876810', 'size': 10.7, 'devname': 'sdh', 'silvering': 'no'}, 'scsi-36001405b319164f4d1841e585cd61bc0': {'name': 'scsi-36001405b319164f4d1841e585cd61bc0', 'actualdisk': 'scsi-36001405b319164f4d1841e585cd61bc0', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '3', 'host': 'dhcp876810', 'size': 10.7, 'devname': 'sdi', 'silvering': 'no'}, 'scsi-36001405a430c5a307ff4cb99fea2c1f7': {'name': 'scsi-36001405a430c5a307ff4cb99fea2c1f7', 'actualdisk': 'scsi-36001405a430c5a307ff4cb99fea2c1f7', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '4', 'host': 'dhcp876810', 'size': 64.4, 'devname': 'sdj', 'silvering': 'no'}}
count = disks['diskcount']
mindisksize = disks['disk'] 
def feature_calc(i, k):
    global hosts, disktypes, mindisksize, count, combinations, disks, singles, disksinfo
    lendisks = len(disksinfo)
    if  i[3] >= k[3] or i[0] == k[0] or i[0] in k[0] or k[0] in i[0] or i[2] == float('inf') or k[2] == float('inf'): # less matrix calcs
        res =  [i[0]+','+k[0],i[1],float('inf')]
    elif 'ree' not in disksinfo[i[0]]['pool'] or (',' not in k[0] and 'ree' not in disksinfo[k[0]]['pool']): # the disks belong to pools 
        res =  [i[0]+','+k[0],i[1],float('inf')]
    else:
        if i[1] < lendisks+1:  # disk hosts test
            hosts.add(disksinfo[i[0]]['host'])
            if ',' not in k[0]:
                hosts.add(disksinfo[k[0]]['host'])
            combineddisks = i[0]+','+k[0]
            disksn = combineddisks.count(',')+1
            hostsn = len(hosts)
            if hostsn < disksn:
                if ',' not in k[0]:
                    res =  [combineddisks,i[1],lendisks]
                else: 
                    res =  [combineddisks,i[1],k[2]+lendisks]
            else:
                    res =  [combineddisks,i[1],0] # hosts equal or higher than the disks so still 0
        elif i[1] < (2*lendisks)+1: # disk type
            disktypes.add(0)  # let all disktypes be 0 till we change them later
            if ',' not in k[0]:
                disktypes.add(0)
            if len(disktypes) > 1:
                  res =  [i[0]+','+k[0],i[1],float('inf')]
            else:
                  res =  [i[0]+','+k[0],i[1],0]
        elif i[1] < (3*lendisks)+1: # disk sizes test 
            if disksinfo[i[0]]['size'] == mindisksize: 
                if ',' not in k[0] and disksinfo[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],0]
                elif ',' not in k[0] and disksinfo[k[0]]['size'] > mindisksize:
                    res =  [i[0]+','+k[0],i[1],1]
                elif ',' in k[0]:
                    res =  [i[0]+','+k[0],i[1],k[2]]
            elif disksinfo[i[0]]['size'] > mindisksize:
                if ',' not in k[0] and disksinfo[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],1]
                elif ',' not in k[0] and disksinfo[k[0]]['size'] > mindisksize:   # both disks are higher than minimum -- it is not allowed
                    if count  == 2:
                        res =  [i[0]+','+k[0],i[1],float('inf')]
                    else: 
                        res =  [i[0]+','+k[0],i[1],2]

                elif ',' in k[0] and k[2]+1 < count :
                    res =  [i[0]+','+k[0],i[1],k[2]+1]
                else:
                    res =  [i[0]+','+k[0],i[1],float('inf')]
            elif ',' not in k[0] and k[2] < mindisksize:
                res =  [i[0]+','+k[0],i[1],float('inf')]
            else:
                res =  [i[0]+','+k[0],i[1],float('inf')]
    res = res + [i[3]]
    if res[2] < float('inf'):
        if res[0] not in combinations:
            combinations[res[0]] = res[2]
        else:
            combinations[res[0]] = combinations[res[0]]+res[2]
            print(res)        
    return res   
                
def combine_features(column_values):
    ccolumn_values = column_values.tolist()
    return (ccolumn_values[0][0],ccolumn_values[0][1],float(ccolumn_values[0][2])+float(ccolumn_values[1][2])+float(ccolumn_values[2][2]))

def fastdiskselect(elements):
    global hosts, disktypes, mindisksize, count, combinations, disks, singles, disksinfo
    df = pd.DataFrame(elements)
    result_df = df
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    #print('#############################33')
    #print(df)
    #print('#############################33')
    for c in range(1,count):
        result_data = [operate(row1, row2) for row1, row2 in zip(df.values, result_df.values)]
        result_df = pd.DataFrame(result_data) 
    keytodel = set()
    for key in combinations:
         if(key.count(',')+1 <  count):
            keytodel.add(key)
    for key in keytodel:
         del combinations[key]
    best_disk = sorted(combinations.items(), key=lambda x: x[1])
            
    print(best_disk)
    exit()
    new_row = result_df.apply(lambda x: combine_features(x),axis=0)
    #print(new_row.loc[1,:])
    filtered_df = result_df.loc[:, result_df.apply(lambda col: 'd0,d1,d2'in str(col[0]))]
    print(filtered_df)
    exit()
    filtered_df = new_row.loc[:,new_row.iloc[2] == 23.0]
    #newdf  = result_df.apply(lambda x: [item[2] < float('inf') for item in x])
    newdf  = result_df[filtered_df]
    #print(filtered_df)

if __name__=='__main__':
    # Define the 10 element
    elements = []
    result_df = pd.DataFrame()
    feature1 = []   # hosts , identity of column < len(disks), penalty step = len(disk)+1
    feature2 = []   # disk type (sata, sas,..etc0 identity of column len(disks),2len(disks, penalty step = inf (cannot mix)
    feature3 = []   # disk sizes, identity of column 2len(disks), 3len(disks), penalty  = 1 
    lendisks = len(disksinfo)
    counter = 1 
    for disk in disksinfo:
        info = disksinfo[disk]
        feature1.append([disk,counter,0,counter])
        feature2.append([disk,lendisks+counter,0,counter])
        feature3.append([disk,(2*lendisks)+counter,0,counter])
        counter +=1
    elements.append(feature1)
    elements.append(feature2)
    elements.append(feature3)
    
    fastdiskselect(elements)

