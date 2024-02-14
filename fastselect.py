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
    if  '767;' in k[0]+i[0] and '8a6' in k[0]+i[0] and '1d1' in k[0]+i[0] and ',' in  k[0] and k[2] != float('inf'):
        toprint = 1
        print('hellllllllllllllllllllo')
        print('kkkkkkkkkk',k)
        print('iiiiiiiiii',i)
        print(combineddisks)
        print('toprint', toprint) 
        print('mustinclude',mustinclude)
    res = []
    if i[3] not in k[3]:
        combinedhosts = i[3]+','+k[3]
    else:
        combinedhosts = k[3]
    if  i[4] >= k[4] or i[0] == k[0] or i[0] in k[0] or k[0] in i[0] or i[2] == float('inf') or k[2] == float('inf'): # less matrix calcs
        if toprint:
            print('iam here 1')
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
    elif ('ree' not in disksinfo[i[0]]['pool'] and i[0] not in mustinclude) or (',' not in k[0] and 'ree' not in disksinfo[k[0]]['pool'] and k[0] not in mustinclude): # the disks belong to pools except if we are optimizing the raid they could be online in this mustinclude 
        if toprint:
            print('iam here 2')
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
    elif disksinfo[i[0]]['size'] < mindisksize:
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
        if toprint:
            print('iam here 3')
            print(disksinfo[i[0]]['size'],mindisksize,i[0]) 
         
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
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude
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

    keytodel = set()
    
    for key in combinations:
         if(key.count(',')+1 <  count):
            keytodel.add(key)
    print('===================')
    print(type(combinations))
    print(len(combinations))
    print(len(keytodel))
    print('===================')
    for key in keytodel:
         del combinations[key]
    best_value = min(combinations.items(), key=lambda x: x[1])[1]
    best_disk = [x for x in combinations.items() if x[1] == best_value and x[1] != float('inf')]
    print(best_disk)
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
    with open('/root/fastselectopt','a') as f:
        f.write(str(count)+' '+str(mindisksize)+' '+str(disks)+' '+str(mustinclude)+'\n')
    combinations = dict()
    hosts = set()
    #disktypes = set()
    #disks = {}
    #disksinfo = {}
    #count = 0 
    #mindisksize = 0 
    return selectdisks(disks, disksinfo)

def selectdisks(fdisks,fdisksinfo,addtopool=''):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude
    disks, disksinfo = fdisks, fdisksinfo
    with open('/TopStordata/fastselect','w') as f:
        f.write(str(fdisks)+'\n'+str(fdisksinfo)+'/n')
    count = disks['diskcount']
    print('count',count)
    if addtopool != '' or count ==1:
        count = disks['diskcount'] + 1
    if len(addtopool) > 0 :
        pooldisks = [x for x in disksinfo if addtopool in disksinfo[x]['pool']]
        mustinclude = ','.join(pooldisks)
    ####################################
    ### need to optimize in case of adding single disks to the single .. no parity.. 
    ######### it shoudl return non-inf
    mindisksize = disks['disk'] 
    elements = []
    feature1 = []   # hosts , identity of column < len(disks), penalty step = len(disk)+1
    feature2 = []   # disk type (sata, sas,..etc0 identity of column len(disks),2len(disks, penalty step = inf (cannot mix)
    feature3 = []   # disk sizes, identity of column 2len(disks), 3len(disks), penalty  = 1 
    lendisks = len(disksinfo)
    counter = 1 
    for disk in disksinfo:
        info = disksinfo[disk]
        feature1.append([disk,counter,0,info['host'],counter])
        feature2.append([disk,lendisks+counter,0,info['host'],counter])
        feature3.append([disk,(2*lendisks)+counter,0,info['host'],counter])
        counter +=1
    elements.append(feature1)
    elements.append(feature2)
    elements.append(feature3)
    combinations = dict()
    hosts = set()
    return fastdiskselect(elements)

if __name__=='__main__':
    import sys
    combinations = dict()
    hosts = set()
    disktypes = set()
    mustinclude = 'NoDisk'
    disks = {'disk': 64.4, 'diskcount': 2, 'others': [], 'hosts': ['dhcp177929'], 'othershosts': []}
    diskinfo = {'scsi-36001405d5b48429b1a143769bf03ca77': {'name': 'scsi-36001405d5b48429b1a143769bf03ca77', 'zname': 'scsi-36001405d5b48429b1a143769bf03ca77', 'actualdisk': 'scsi-36001405d5b48429b1a143769bf03ca77', 'changeop': 'ONLINE', 'pool': 'pdhcp3199524969', 'raid': 'mirror-0_pdhcp3199524969', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp177929', 'size': 10.7, 'devname': 'scsi-36001405d5b48429b1a143769bf03ca77', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014059d54afe0ea104c68a1f39e0aa': {'name': 'scsi-360014059d54afe0ea104c68a1f39e0aa', 'zname': 'scsi-360014059d54afe0ea104c68a1f39e0aa', 'actualdisk': 'scsi-360014059d54afe0ea104c68a1f39e0aa', 'changeop': 'ONLINE', 'pool': 'pdhcp3199524969', 'raid': 'mirror-0_pdhcp3199524969', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp177929', 'size': 10.7, 'devname': 'scsi-360014059d54afe0ea104c68a1f39e0aa', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014059853393b27724feeb7ca9ab92': {'name': 'scsi-360014059853393b27724feeb7ca9ab92', 'actualdisk': 'scsi-360014059853393b27724feeb7ca9ab92', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '2', 'host': 'dhcp177929', 'size': 64.4, 'devname': 'sdh', 'silvering': 'no'}, 'scsi-36001405c03489b920e648239e99fd389': {'name': 'scsi-36001405c03489b920e648239e99fd389', 'actualdisk': 'scsi-36001405c03489b920e648239e99fd389', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '3', 'host': 'dhcp177929', 'size': 64.4, 'devname': 'sdi', 'silvering': 'no'}}
    raid = {'name': 'mirror-0', 'changeop': 'ONLINE', 'status': 'ONLINE', 'pool': 'pdhcp1133218265', 'host': 'dhcp273302', 'disklist': [{'name': 'scsi-360014050551bb921e8243629899640b0', 'actualdisk': 'scsi-360014050551bb921e8243629899640b0', 'changeop': 'ONLINE', 'pool': 'pdhcp1133218265', 'raid': 'mirror-0', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp876810', 'size': '64.4GB', 'devname': 'scsi-360014050551bb921e8243629899640b0', 'silvering': 'no'}, {'name': 'scsi-36001405762de08e97d94222915977e7b', 'actualdisk': 'sdd', 'changeop': 'ONLINE', 'pool': 'pdhcp1133218265', 'raid': 'mirror-0', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp273302', 'size': '64.4GB', 'devname': 'sdd', 'silvering': 'no'}], 'missingdisks': [0], 'raidrank': (2, 0)}
    disks = {'disk': 10.7, 'diskcount': 3, 'others': [], 'hosts': ['dhcp292043'], 'othershosts': []}
    disksinfo = {'dm-2': {'name': 'dm-2', 'zname': 'dm-2', 'actualdisk': 'dm-2', 'changeop': 'FAULT', 'pool': 'pdhcp1287810983', 'raid': 'mirror-0_pdhcp1287810983', 'status': 'OFFLINE', 'id': '0', 'host': 'dhcp292043', 'size': 0.0, 'devname': 'dm-2', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014050cab259baf414920a03736068': {'name': 'scsi-360014050cab259baf414920a03736068', 'zname': 'sdj', 'actualdisk': 'sdj', 'changeop': 'ONLINE', 'pool': 'pdhcp1287810983', 'raid': 'mirror-0_pdhcp1287810983', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp292043', 'size': 64.4, 'devname': 'sdj', 'silvering': 'no', 'replacingroup': ''}, 'dm-3': {'name': 'dm-3', 'zname': 'dm-3', 'actualdisk': 'dm-3', 'changeop': 'FAULT', 'pool': 'pdhcp1287810983', 'raid': 'mirror-1_pdhcp1287810983', 'status': 'OFFLINE', 'id': '0', 'host': 'dhcp292043', 'size': 0.0, 'devname': 'dm-3', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405a2f8fe63cf8142dab097f6726': {'name': 'scsi-36001405a2f8fe63cf8142dab097f6726', 'zname': 'sdi', 'actualdisk': 'sdi', 'changeop': 'ONLINE', 'pool': 'pdhcp1287810983', 'raid': 'mirror-1_pdhcp1287810983', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp292043', 'size': 64.4, 'devname': 'sdi', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405d14138232f8c4929abac7f1d1': {'name': 'scsi-36001405d14138232f8c4929abac7f1d1', 'actualdisk': 'scsi-36001405d14138232f8c4929abac7f1d1', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '0', 'host': 'dhcp292043', 'size': 10.7, 'devname': 'sdg', 'silvering': 'no'}, 'scsi-36001405a311ca17a258434cb2cfe3767': {'name': 'scsi-36001405a311ca17a258434cb2cfe3767', 'actualdisk': 'scsi-36001405a311ca17a258434cb2cfe3767', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '1', 'host': 'dhcp292043', 'size': 10.7, 'devname': 'sdk', 'silvering': 'no'}, 'scsi-360014056dd504fb98214b258c68368a6': {'name': 'scsi-360014056dd504fb98214b258c68368a6', 'actualdisk': 'scsi-360014056dd504fb98214b258c68368a6', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '4', 'host': 'dhcp292043', 'size': 10.7, 'devname': 'sdh', 'silvering': 'no'}}
    addtopool = 'pdhcp1102820153'
    if sys.argv[1] == 'select':
        selectdisks(disks,disksinfo)
    elif sys.argv[1] == 'addtopool':
        selectdisks(disks,disksinfo, addtopool)
    else:
        optimizedisks(raid, disksinfo)

