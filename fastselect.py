#!/usr/bin/python3
import pandas as pd
import numpy as np
# Define a function to operate on elements

combinations = dict()
hosts = set()
disktypes = set()
disks = {}
disksinfo = {}
count = 0 
mindisksize = 0 
diskscat = {}

def norm(val):
 units={'B':1/1024**2,'K':1/1024, 'M': 1, 'G':1024 , 'T': 1024**2 }
 if type(val)==float:
  return val
 if val[-1] != 'B':
  return float(val)
 else:
  if val[-2] in list(units.keys()):
   return float(val[:-2])*float(units[val[-2]])/1024   # returning in GB
  else:
   return float(val[:-1])*float(units['B'])

def operate(df1row,df2row):
 res = []
 for i in df1row:
    if len(i) < 1:
        continue
    try:
        for k in df2row:
            res.append(feature_calc(i,k))
    except:
        continue
 return res   

def feature_calc(i, k):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude
    lendisks = len(disksinfo)
    combineddisks = i[0]+','+k[0]
    toprint = 0 
    res = []
    if i[3] not in k[3]:
        combinedhosts = i[3]+','+k[3]
    else:
        combinedhosts = k[3]
    if  i[4] >= k[4] or i[0] == k[0] or i[0] in k[0] or k[0] in i[0] or i[2] == float('inf') or k[2] == float('inf'): # less matrix calcs
        if toprint:
            print('iam here 1')
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
    elif ('ree' not in disksinfo[i[0]]['pool']) or (i[0] in mustinclude) or (',' not in k[0] and 'ree' not in disksinfo[k[0]]['pool'] and k[0] not in mustinclude): # the disks belong to pools except if we are optimizing the raid they could be online in this mustinclude 
        if toprint:
            print('iam here 2')
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
    elif disksinfo[i[0]]['size'] < mindisksize:
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
        if toprint:
            print('iam here 3')
         
    elif ',' not in k[0] and disksinfo[k[0]]['size'] < mindisksize:
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
        if toprint:
            print('iam here 4')
    else:
        if toprint:
            print('iam here 5')
        if i[1] < lendisks+1:  # disk hosts test
            disksn = combineddisks.count(',')+1
            hostsn = combinedhosts.count(',')+1
            if toprint:
                print('iam here 6')
            if hostsn < disksn:
                if toprint:
                    print('iam here 7')
                if ',' not in k[0]:
                    res =  [combineddisks,i[1],lendisks,combinedhosts]
                    if toprint:
                        print('iam here 8')
                else: 
                    res =  [combineddisks,i[1],k[2]+lendisks,combinedhosts]
                    if toprint:
                        print('iam here 9')
            else:
                    res =  [combineddisks,i[1],0,combinedhosts] # hosts equal or higher than the disks so still 0
                    if toprint:
                        print('iam here 10')
        elif i[1] < (2*lendisks)+1: # disk type
            if toprint:
               print('iam here 11')
            disktypes.add(0)  # let all disktypes be 0 till we change them later
            if ',' not in k[0]:
                disktypes.add(0)
                if toprint:
                    print('iam here 12')
            if len(disktypes) > 1:
                  res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
                  if toprint:
                    print('iam here 13')
            else:
                  res =  [i[0]+','+k[0],i[1],0,combinedhosts]
                  if toprint:
                    print('iam here 14')
        elif i[1] < (3*lendisks)+1: # disk sizes test 
            if toprint:
               print('iam here 15')
            if disksinfo[i[0]]['size'] == mindisksize: 
                if toprint:
                    print('iam here 16')
                if ',' not in k[0] and disksinfo[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],0,combinedhosts]
                if toprint:
                    print('iam here 17')
                elif ',' not in k[0] and disksinfo[k[0]]['size'] > mindisksize:
                    if toprint:
                        print('iam here 18')
                    res =  [i[0]+','+k[0],i[1],1,combinedhosts]
                elif ',' in k[0]:
                    if toprint:
                        print('iam here 19')
                    res =  [i[0]+','+k[0],i[1],k[2],combinedhosts]
            elif disksinfo[i[0]]['size'] > mindisksize:
                if toprint:
                    print('iam here 20')
                if ',' not in k[0] and disksinfo[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],1,combinedhosts]
                    if toprint:
                        print('iam here 21')
                elif ',' not in k[0] and disksinfo[k[0]]['size'] > mindisksize:   # both disks are higher than minimum -- it is not allowed
                    if toprint:
                        print('iam here 22')
                    if count  == 2:
                        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
                        if toprint:
                            print('iam here 23')
                    else: 
                        res =  [i[0]+','+k[0],i[1],2,combinedhosts]
                        if toprint:
                            print('iam here 24')

                elif ',' in k[0] and k[2]+1 < count :
                    res =  [i[0]+','+k[0],i[1],k[2]+1,combinedhosts]
                    if toprint:
                        print('iam here 25')
                else:
                    res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
                    if toprint:
                        print('iam here 26')
            elif disksinfo[i[0]]['size'] < mindisksize:
                if toprint:
                    print('iam here 27')
                res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
            elif ',' not in k[0] and disksinfo[k[0]]['size'] < mindisksize:
                res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
                if toprint:
                    print('iam here 28')
            else:
                if toprint:
                    print('iam here 29')
                res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
    if len(res) < 3:
        if toprint:
           print('iam here 30')
        return []
    if toprint:
        print('iam here 31')
    res = res + [i[4]]
    if res[0] not in combinations:
        if toprint:
            print('iam here 32')
        combinations[res[0]] = res[2]
        if toprint:
            print('iam here 33')
            print('comb0',combinations[res[0]])
    else:
        if toprint:
            print('iam here 34')
            print('comb1',combinations[res[0]])
        combinations[res[0]] = combinations[res[0]]+res[2]
        if toprint: 
            print('iam here 35')
            print('comb2',combinations[res[0]])
    if toprint:
        print('iam here 36')
        printlist = [{x:combinations[x]} for x in combinations if combinations[x] != float('inf')]
        print('still feasible',printlist)
    return res   
                
def combine_features(column_values):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat
    ccolumn_values = column_values.tolist()
    return (ccolumn_values[0][0],ccolumn_values[0][1],float(ccolumn_values[0][2])+float(ccolumn_values[1][2])+float(ccolumn_values[2][2]))

def fastdiskselect(elements):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude
    df = pd.DataFrame(elements)

    result_df = df
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    for c in range(1,count):
        result_data = [operate(row1, row2) for row1, row2 in zip(df.values, result_df.values)]
        result_df = pd.DataFrame(result_data) 
    if count == 1:
        result_data = [operate(row1, row2) for row1, row2 in zip(df.values, result_df.values)]
        result_df = pd.DataFrame(result_data) 
    keytodel = set()
    
    for key in combinations:
         if(key.count(',')+1 <  count):
            keytodel.add(key)
    for key in keytodel:
         del combinations[key]
    best_value = min(combinations.items(), key=lambda x: x[1])[1]
    best_disk = [x for x in combinations.items() if x[1] == best_value and x[1] != float('inf')]
    print('---------------------------------------------------')
    print('diskscat',len(diskscat),diskscat.keys())
    print('computed combinations',len(combinations))
    print('to delete combinations', len(keytodel))
    print('number of best disk combinations',len(best_disk))
    print('the best disk list', best_disk)
    print('---------------------------------------------------')
    combinations = dict()
    hosts = set()
    mindisksize = 0
    count = 0 
    mindisksize = 0 
    mustinclude = ''
    return best_disk

def optimizedisks(fraid, fdisksinfo):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude
    raid, disksinfo = fraid, fdisksinfo
    count = len(raid['disklist'])
    mindisksize = min([ norm(x['size']) for x in raid['disklist'] if x['changeop'] in ['ONLINE']])
    print(mindisksize,count)
    mustinclude = ''
    for disk in raid['disklist']:
        if len(mustinclude) == 0:
            mustinclude = disk['name']
        else:
            mustinclude = disk['name']+','+mustinclude
    if 'mirror' in raid['name'] and count == 1:
        count = 2
    disks = {'diskcount':count , 'disk': mindisksize }
    with open('/TopStordata/fastselectopt','w') as f:
        f.write(str(count)+' '+str(mindisksize)+' '+str(disks)+' '+str(mustinclude)+'\n')
    combinations = dict()
    hosts = set()
    #disktypes = set()
    #disks = {}
    #disksinfo = {}
    #count = 0 
    #mindisksize = 0 
    return selectdisks(disks, disksinfo)

def featuring():
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat
    counter = 1
    print('current', disks)
#{'name': 'scsi-3600140544acffed7e3b4d78899970462', 'zname': 'sdt', 'actualdisk': 'sdt', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdt', 'silvering': 'no', 'replacingroup': ''}
    feature1 = []   # hosts , identity of column < len(disks), penalty step = len(disk)+1
    feature2 = []   # disk type (sata, sas,..etc0 identity of column len(disks),2len(disks, penalty step = inf (cannot mix)
    feature3 = []   # disk sizes, identity of column 2len(disks), 3len(disks), penalty  = 1 
    lendisks = len(disksinfo)
    counter = 1 
    elements = []
    for disk in disksinfo:
        if 'pdhcp' in disksinfo[disk]['pool'] or norm(disksinfo[disk]['size']) < norm(disks['disk']) or disksinfo[disk]['changeop'] != 'free':
            print('pdhcp' in disksinfo[disk]['pool'], norm(disksinfo[disk]['size']) < norm(disks['disk']), disksinfo[disk]['changeop'] )
            continue
        key = f"{disksinfo[disk]['host']}_{disksinfo[disk]['size']}"
        if key not in diskscat:
            diskscat[key] = dict()
            diskscat[key]['host'] = disksinfo[disk]['host']
            diskscat[key]['size'] = disksinfo[disk]['size']
            diskscat[key]['diskcount'] = 0 
            diskscat[key]['disks'] = []
            feature1.append([key,counter,0,disksinfo[disk]['host'],counter])
            feature2.append([key,lendisks+counter,0,disksinfo[disk]['host'],counter])
            feature3.append([key,(2*lendisks)+counter,0,disksinfo[disk]['host'],counter])
            counter +=1
        diskscat[key]['disks'].append(disk)
        diskscat[key]['diskcount'] += 1
    
    print(diskscat)
    elements.append(feature1)
    elements.append(feature2)
    elements.append(feature3)
    return elements 
def selectdisks(fdisks,fdisksinfo,addtopool=''):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat
    disks, disksinfo = fdisks, fdisksinfo
    with open('/TopStordata/fastselect','w') as f:
        f.write(str(fdisks)+'\n'+str(fdisksinfo)+'/n')
    count = disks['diskcount']
    print('count',count)
    #if count ==1:
    #    count = disks['diskcount'] + 1
    if len(addtopool) > 0 :
        pooldisks = [x for x in disksinfo if addtopool in disksinfo[x]['pool']]
        mustinclude = ','.join(pooldisks)
    ####################################
    ### need to optimize in case of adding single disks to the single .. no parity.. 
    ######### it shoudl return non-inf
    mindisksize = disks['disk'] 
    elements = []
    elements = featuring()
    combinations = dict()
    hosts = set()

    return fastdiskselect(elements)

if __name__=='__main__':
    import sys
    combinations = dict()
    hosts = set()
    disktypes = set()
    mustinclude = 'NoDisk'
##### get the following variables from /TopStordata/fastselect if you need to troubleshoot, then wirte down the right addtopool from the zpool status
    disks = {'disk': 10.7, 'diskcount': 5, 'others': [], 'hosts': ['dhcp222552', 'dhcp932129'], 'othershosts': []}
    disksinfo = {'scsi-3600140544acffed7e3b4d78899970462': {'name': 'scsi-3600140544acffed7e3b4d78899970462', 'zname': 'sdt', 'actualdisk': 'sdt', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdt', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405e39d18ee7e1942e3b75b90c68': {'name': 'scsi-36001405e39d18ee7e1942e3b75b90c68', 'zname': 'sdu', 'actualdisk': 'sdu', 'changeop': 'NA', 'pool': 'pdhcp218059142', 'raid': 'stripe-0_pdhcp218059142', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdu', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014054fbe0063b83a431ca7e678014': {'name': 'scsi-360014054fbe0063b83a431ca7e678014', 'zname': 'sdv', 'actualdisk': 'sdv', 'changeop': 'ONLINE', 'pool': 'pdhcp218059142', 'raid': 'stripe-0_pdhcp218059142', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdv', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405df397c33cff3489aa666ff549': {'name': 'scsi-36001405df397c33cff3489aa666ff549', 'zname': 'sdw', 'actualdisk': 'sdw', 'changeop': 'ONLINE', 'pool': 'pdhcp218059142', 'raid': 'stripe-0_pdhcp218059142', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdw', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014058db527f660a04f7cbf15fdf4d': {'name': 'scsi-360014058db527f660a04f7cbf15fdf4d', 'zname': 'sdx', 'actualdisk': 'sdx', 'changeop': 'ONLINE', 'pool': 'pdhcp218059142', 'raid': 'stripe-0_pdhcp218059142', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdx', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405b534d57064f544388376535ce': {'name': 'scsi-36001405b534d57064f544388376535ce', 'actualdisk': 'scsi-36001405b534d57064f544388376535ce', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '14', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdy', 'silvering': 'no'}, 'scsi-3600140550043b7aa92840219de85ba5c': {'name': 'scsi-3600140550043b7aa92840219de85ba5c', 'actualdisk': 'scsi-3600140550043b7aa92840219de85ba5c', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '15', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdz', 'silvering': 'no'}, 'scsi-36001405be40cec3db634479a75e4fe6a': {'name': 'scsi-36001405be40cec3db634479a75e4fe6a', 'actualdisk': 'scsi-36001405be40cec3db634479a75e4fe6a', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '16', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdaa', 'silvering': 'no'}, 'scsi-360014057baf353790434718bbbd5c47d': {'name': 'scsi-360014057baf353790434718bbbd5c47d', 'zname': 'sdab', 'actualdisk': 'sdab', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdab', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405f31ae4281209471b9ea93b289': {'name': 'scsi-36001405f31ae4281209471b9ea93b289', 'zname': 'sdac', 'actualdisk': 'sdac', 'changeop': 'ONLINE', 'pool': 'pdhcp218059142', 'raid': 'stripe-0_pdhcp218059142', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'sdac', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014050a0e856622284c119a708de6e': {'name': 'scsi-360014050a0e856622284c119a708de6e', 'actualdisk': 'scsi-360014050a0e856622284c119a708de6e', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdk', 'silvering': 'no'}, 'scsi-3600140529153582a13144b48e8d85733': {'name': 'scsi-3600140529153582a13144b48e8d85733', 'actualdisk': 'scsi-3600140529153582a13144b48e8d85733', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '1', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdl', 'silvering': 'no'}, 'scsi-3600140574da01bf7e294e25b9604704d': {'name': 'scsi-3600140574da01bf7e294e25b9604704d', 'actualdisk': 'scsi-3600140574da01bf7e294e25b9604704d', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '2', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdm', 'silvering': 'no'}, 'scsi-36001405af07e05fc1594194a6d7ba050': {'name': 'scsi-36001405af07e05fc1594194a6d7ba050', 'actualdisk': 'scsi-36001405af07e05fc1594194a6d7ba050', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '3', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdn', 'silvering': 'no'}, 'scsi-36001405bafebcf5e27049c490990131a': {'name': 'scsi-36001405bafebcf5e27049c490990131a', 'actualdisk': 'scsi-36001405bafebcf5e27049c490990131a', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '4', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdo', 'silvering': 'no'}, 'scsi-3600140506dddf04843445fcb095c0a1e': {'name': 'scsi-3600140506dddf04843445fcb095c0a1e', 'actualdisk': 'scsi-3600140506dddf04843445fcb095c0a1e', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '5', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdp', 'silvering': 'no'}, 'scsi-360014056d13305a7afe47f591f19d643': {'name': 'scsi-360014056d13305a7afe47f591f19d643', 'actualdisk': 'scsi-360014056d13305a7afe47f591f19d643', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '6', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdq', 'silvering': 'no'}, 'scsi-360014056192b958012f432293f7ef26d': {'name': 'scsi-360014056192b958012f432293f7ef26d', 'actualdisk': 'scsi-360014056192b958012f432293f7ef26d', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '7', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdr', 'silvering': 'no'}, 'scsi-360014054ddc3a36fbb34136bd487474b': {'name': 'scsi-360014054ddc3a36fbb34136bd487474b', 'actualdisk': 'scsi-360014054ddc3a36fbb34136bd487474b', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '8', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sds', 'silvering': 'no'}}
    addtopool = 'pdhcp218059142'
    if sys.argv[1] == 'select':
        selectdisks(disks,disksinfo)
    elif sys.argv[1] == 'addtopool':
        selectdisks(disks,disksinfo, addtopool)
    else:
        optimizedisks(raid, disksinfo)

