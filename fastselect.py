#!/usr/bin/python3
import pandas as pd
import numpy as np
from etcdgetpy import etcdget as get
from itertools import combinations_with_replacement as combine
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
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude,diskscat, redundancy
    lendisks = len(disksinfo)
    combineddisks = i[0]+','+k[0]
    toprint = 0 
    res = []
    if i[3] not in k[3]:
        combinedhosts = i[3]+','+k[3]
    else:
        combinedhosts = k[3]
    if  i[4] >= k[4] or  i[2] == float('inf') or k[2] == float('inf'): # less matrix calcs
        if toprint:
            print('iam here 1')
        res =  [i[0]+','+k[0],i[1],float('inf'),combinedhosts]
         
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
            if diskscat[i[0]]['size'] == mindisksize: 
                if toprint:
                    print('iam here 16')
                if ',' not in k[0] and diskscat[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],0,combinedhosts]
                if toprint:
                    print('iam here 17')
                elif ',' not in k[0] and diskscat[k[0]]['size'] > mindisksize:
                    if toprint:
                        print('iam here 18')
                    res =  [i[0]+','+k[0],i[1],1,combinedhosts]
                elif ',' in k[0]:
                    if toprint:
                        print('iam here 19')
                    res =  [i[0]+','+k[0],i[1],k[2],combinedhosts]
            elif diskscat[i[0]]['size'] > mindisksize:
                if toprint:
                    print('iam here 20')
                if ',' not in k[0] and diskscat[k[0]]['size'] == mindisksize:
                    res =  [i[0]+','+k[0],i[1],1,combinedhosts]
                    if toprint:
                        print('iam here 21')
                elif ',' not in k[0] and diskscat[k[0]]['size'] > mindisksize:   # both disks are higher than minimum -- it is not allowed
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

def calc_size(comb):
    sizepenalty = 0
    for com in comb:
        size = norm(com.split('_')[1])
        sizepenalty += (size - mindisksize)
    return sizepenalty/(mindisksize * count)  #  the dividend is to limit even the sizes could be in the range of 10x


def calc_host(comb):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat, redundancy
    
    combset = set(comb)
   # if the this disk combinations between hosts is larger than the number of disks in this host
    for host in combset:
        hostcount =  " ".join(comb).count(host)
        if hostcount > len(diskscat[host]['disks']):
            return float('inf') 
    hostcounts = []
    for host in hosts:
        hostcounts.append( " ".join(comb).count(host))
    nphostcounts = np.array(hostcounts)
    hostcalc = np.sum(np.abs(nphostcounts[:,np.newaxis]-nphostcounts)) // 2
    return hostcalc

def veryfastselect(elements):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat, redundancy
    diskcomb = combine(diskscat.keys(),count)
    minweight = float('inf')
    bestcomb = [] 
    #overallcalc = []    # uncomment in case you want to see all the weights 
    for comb in diskcomb:
        calchost = calc_host(comb)
        calcsize = calc_size(comb)
        calctotal = (1000 * calchost) + calcsize
        if calctotal < minweight:
            minweight = calctotal
            bestcomb = [comb]
        elif calctotal == minweight:
            bestcomb.append(comb)
    #    overallcalc.append([comb,calctotal])
    #print('overcalc', overallcalc)
    print('best comb:',bestcomb, minweight)
    allbests = []
    print('bestcomb are',bestcomb)
    for bestcom in bestcomb:
        bests = []
        for com in bestcom:
            host = com.split('_')[0]
            if 'hcounter' not in diskscat[com]:
                diskscat[com]['hcounter'] = 0
            diskscat[com]['hcounter'] += 1
        for com in bestcom:
            bests += diskscat[com]['disks'][:diskscat[com]['hcounter']]
            diskscat[com]['hcounter'] = 0
        allbests.append(bests)  
    print('best disks',allbests) 
    best_disk = allbests[0]
    print('the best disk', allbests[0])
    combinations = dict()
    hosts = set()
    mindisksize = 0
    count = 0 
    mindisksize = 0 
    mustinclude = ''
    with open('/TopStordata/resfastselect','w') as f:
        f.write(",".join(best_disk)+'\n')
    return ",".join(best_disk)




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
    print(combinations)
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

def optimizedisks(leaderip, fraid, fdisksinfo):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, redundancy, diskscat
    raid, disksinfo = fraid, fdisksinfo
    with open('/TopStordata/fastselectopt','w') as f:
        f.write(str(fraid)+'\n'+str(fdisksinfo)+'\n')
    count = len(raid['disklist'])
    mindisksize = min([ norm(x['size']) for x in raid['disklist'] if x['changeop'] in ['ONLINE']])
    mustinclude = ''
    for disk in raid['disklist']:
        if len(mustinclude) == 0:
            mustinclude = disk['name']
        else:
            mustinclude = disk['name']+','+mustinclude
    if 'mirror' in raid['name'] and count == 1:
        count = 2
    disks = {'diskcount':count , 'disk': mindisksize }
    print('mustinclude', mustinclude)
    #with open('/TopStordata/fastselectopt','w') as f:
    #    f.write(str(count)+' '+str(mindisksize)+' '+str(disks)+' '+str(mustinclude)+'\n')
    combinations = dict()
    hosts = set()
    #disktypes = set()
    #disks = {}
    #disksinfo = {}
    #count = 0 
    #mindisksize = 0 
    return selectdisks(leaderip, disks, disksinfo)

def featuring(leaderip):
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
    needtoreplacelst = get(leaderip,'needto','--prefix')
    needtoreplace = str(needtoreplacelst)
    for disk in disksinfo:
        if norm(disksinfo[disk]['size']) < norm(disks['disk']) or disksinfo[disk]['changeop'] not in [ 'free', 'ONLINE' ] or ( disksinfo[disk]['changeop'] in 'ONLINE' and disk not in mustinclude) or disk in needtoreplace:
            continue
        else:
            key = f"{disksinfo[disk]['host']}_{disksinfo[disk]['size']}"
            if key not in diskscat:
                diskscat[key] = dict()
                diskscat[key]['host'] = disksinfo[disk]['host']
                diskscat[key]['size'] = disksinfo[disk]['size']
                diskscat[key]['diskcount'] = 0 
                diskscat[key]['disks'] = []
                hosts.add(disksinfo[disk]['host'])
                feature1.append([key,counter,0,disksinfo[disk]['host'],counter])
                feature2.append([key,lendisks+counter,0,disksinfo[disk]['host'],counter])
                feature3.append([key,(2*lendisks)+counter,0,disksinfo[disk]['host'],counter])
                counter +=1
            diskscat[key]['disks'].append(disk)
            diskscat[key]['diskcount'] += 1
    
    elements.append(feature1)
    elements.append(feature2)
    elements.append(feature3)
    return elements 


def selectdisks(leaderip, fdisks,fdisksinfo,addtopool=''):
    global hosts, disktypes, mindisksize, count, combinations, disks, disksinfo, mustinclude, diskscat, redundancy
    disks, disksinfo = fdisks, fdisksinfo
    with open('/TopStordata/fastselect','w') as f:
        f.write('fdisks: '+str(fdisks.keys())+'\n'+str(fdisks)+'\n'+str(fdisksinfo)+'/n')
    count = disks['diskcount']
    hosts = set()
    mustinclude = ''
    print('count',count)
    #if count ==1:
    #    count = disks['diskcount'] + 1
    #if len(addtopool) > 0 :
    #    pooldisks = [x for x in disksinfo if addtopool in disksinfo[x]['pool']]
    #    mustinclude = ','.join(pooldisks)
    ####################################
    ### need to optimize in case of adding single disks to the single .. no parity.. 
    ######### it shoudl return non-inf
    mindisksize = disks['disk'] 
    elements = []
    elements = featuring(leaderip)
    combinations = dict()
    res = veryfastselect(elements)
    disksinfo = []
    disks = {} 
    hosts = {}
    diskscat = {}
    mustinclude = ''

    return res 

if __name__=='__main__':
    import sys
    combinations = dict()
    hosts = set()
    disktypes = set()
    mustinclude = 'NoDisk'
##### get the following variables from /TopStordata/fastselect if you need to troubleshoot, then wirte down the right addtopool from the zpool status
    disks = {'disk': 10.7, 'diskcount': 7, 'others': [], 'hosts': ['dhcp932129'], 'othershosts': []}
    disksinfo = {'scsi-360014055e15ae2781224b7c9ab26d356': {'name': 'scsi-360014055e15ae2781224b7c9ab26d356', 'zname': 'scsi-360014055e15ae2781224b7c9ab26d356', 'actualdisk': 'scsi-360014055e15ae2781224b7c9ab26d356', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-360014055e15ae2781224b7c9ab26d356', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014055b5283bfdd2043a3bf1971b82': {'name': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'zname': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'actualdisk': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405038e27e5dd114fd38c6aaf158': {'name': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'zname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'actualdisk': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-0_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405dc3f57843b554367aaf5c8e71': {'name': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'zname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'actualdisk': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-1_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014056eb348c244a842cbaccea920d': {'name': 'scsi-360014056eb348c244a842cbaccea920d', 'zname': 'scsi-360014056eb348c244a842cbaccea920d', 'actualdisk': 'scsi-360014056eb348c244a842cbaccea920d', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-2_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014056eb348c244a842cbaccea920d', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405792a4b8e191e402eaf40f90fb': {'name': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'zname': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'actualdisk': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-3_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405b9087d0db6ed42a19a3784e6e': {'name': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'zname': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'actualdisk': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-4_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405e62beb80184f49efb21123eee': {'name': 'scsi-36001405e62beb80184f49efb21123eee', 'zname': 'scsi-36001405e62beb80184f49efb21123eee', 'actualdisk': 'scsi-36001405e62beb80184f49efb21123eee', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-5_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405e62beb80184f49efb21123eee', 'silvering': 'no', 'replacingroup': ''}, 'scsi-3600140516dbfaa69ed049b6a88d687d0': {'name': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'zname': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'actualdisk': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-6_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'silvering': 'no', 'replacingroup': ''}, 'scsi-3600140541aec64bf17e4fbcb6fa45a1e': {'name': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'zname': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'actualdisk': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-7_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014050f892602c68449c2ae1a86d02': {'name': 'scsi-360014050f892602c68449c2ae1a86d02', 'zname': 'scsi-360014050f892602c68449c2ae1a86d02', 'actualdisk': 'scsi-360014050f892602c68449c2ae1a86d02', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-8_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014050f892602c68449c2ae1a86d02', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405f7a3fb55b4f7491ab01efe331': {'name': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'zname': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'actualdisk': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'changeop': 'NA', 'pool': 'pdhcp2543526283', 'raid': 'stripe-9_pdhcp2543526283', 'status': 'NA', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405ac355cf3bb19410f952d8979c': {'name': 'scsi-36001405ac355cf3bb19410f952d8979c', 'actualdisk': 'scsi-36001405ac355cf3bb19410f952d8979c', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '11', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdv', 'silvering': 'no'}, 'scsi-36001405a6768a927f724550adee6c274': {'name': 'scsi-36001405a6768a927f724550adee6c274', 'actualdisk': 'scsi-36001405a6768a927f724550adee6c274', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '12', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdw', 'silvering': 'no'}, 'scsi-36001405920b4cbfb9e646e4afc206a21': {'name': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'actualdisk': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '13', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdx', 'silvering': 'no'}, 'scsi-36001405b34fc2b3ebe74a298f7cf7935': {'name': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'actualdisk': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '14', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdz', 'silvering': 'no'}, 'scsi-36001405ad86692168a942ffacdd3ff7b': {'name': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'actualdisk': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '15', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdy', 'silvering': 'no'}, 'scsi-36001405b0c5bd83eed14a7f8faf2e52b': {'name': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'actualdisk': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '16', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdaa', 'silvering': 'no'}, 'scsi-36001405506f53be9fe64694b0182e2eb': {'name': 'scsi-36001405506f53be9fe64694b0182e2eb', 'actualdisk': 'scsi-36001405506f53be9fe64694b0182e2eb', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '17', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdab', 'silvering': 'no'}}
    addtopool = 'pdhcp2543526283'
    leaderip = '10.11.11.100'
    redundancy = 'stripe' 
    raid = {'name': 'mirror-0_pdhcp11175852', 'changeop': 'ONLINE', 'status': 'ONLINE', 'pool': 'pdhcp11175852', 'host': 'dhcp222552', 'disklist': [{'name': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'zname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'actualdisk': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-0', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'silvering': 'no', 'replacingroup': ''}, {'name': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'zname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'actualdisk': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-0', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'silvering': 'no', 'replacingroup': ''}], 'silvering': 'no', 'missingdisks': [0], 'raidrank': (2, 0), 'disks': ['scsi-36001405038e27e5dd114fd38c6aaf158', 'scsi-36001405dc3f57843b554367aaf5c8e71']}
    disksinfo = {'scsi-36001405038e27e5dd114fd38c6aaf158': {'name': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'zname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'actualdisk': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-0_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405038e27e5dd114fd38c6aaf158', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405dc3f57843b554367aaf5c8e71': {'name': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'zname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'actualdisk': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-0_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405dc3f57843b554367aaf5c8e71', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405792a4b8e191e402eaf40f90fb': {'name': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'zname': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'actualdisk': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-1_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405792a4b8e191e402eaf40f90fb', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405a6768a927f724550adee6c274': {'name': 'scsi-36001405a6768a927f724550adee6c274', 'zname': 'scsi-36001405a6768a927f724550adee6c274', 'actualdisk': 'scsi-36001405a6768a927f724550adee6c274', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-1_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405a6768a927f724550adee6c274', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405b9087d0db6ed42a19a3784e6e': {'name': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'zname': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'actualdisk': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-2_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405b9087d0db6ed42a19a3784e6e', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405920b4cbfb9e646e4afc206a21': {'name': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'zname': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'actualdisk': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-2_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405920b4cbfb9e646e4afc206a21', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405e62beb80184f49efb21123eee': {'name': 'scsi-36001405e62beb80184f49efb21123eee', 'zname': 'scsi-36001405e62beb80184f49efb21123eee', 'actualdisk': 'scsi-36001405e62beb80184f49efb21123eee', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-3_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-36001405e62beb80184f49efb21123eee', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405b34fc2b3ebe74a298f7cf7935': {'name': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'zname': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'actualdisk': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-3_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405b34fc2b3ebe74a298f7cf7935', 'silvering': 'no', 'replacingroup': ''}, 'scsi-3600140516dbfaa69ed049b6a88d687d0': {'name': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'zname': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'actualdisk': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-4_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-3600140516dbfaa69ed049b6a88d687d0', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405ad86692168a942ffacdd3ff7b': {'name': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'zname': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'actualdisk': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-4_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405ad86692168a942ffacdd3ff7b', 'silvering': 'no', 'replacingroup': ''}, 'scsi-3600140541aec64bf17e4fbcb6fa45a1e': {'name': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'zname': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'actualdisk': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-5_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-3600140541aec64bf17e4fbcb6fa45a1e', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405b0c5bd83eed14a7f8faf2e52b': {'name': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'zname': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'actualdisk': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-5_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405b0c5bd83eed14a7f8faf2e52b', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014050f892602c68449c2ae1a86d02': {'name': 'scsi-360014050f892602c68449c2ae1a86d02', 'zname': 'scsi-360014050f892602c68449c2ae1a86d02', 'actualdisk': 'scsi-360014050f892602c68449c2ae1a86d02', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-6_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014050f892602c68449c2ae1a86d02', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405506f53be9fe64694b0182e2eb': {'name': 'scsi-36001405506f53be9fe64694b0182e2eb', 'zname': 'scsi-36001405506f53be9fe64694b0182e2eb', 'actualdisk': 'scsi-36001405506f53be9fe64694b0182e2eb', 'changeop': 'ONLINE', 'pool': 'pdhcp11175852', 'raid': 'mirror-6_pdhcp11175852', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405506f53be9fe64694b0182e2eb', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014055e15ae2781224b7c9ab26d356': {'name': 'scsi-360014055e15ae2781224b7c9ab26d356', 'zname': 'scsi-360014055e15ae2781224b7c9ab26d356', 'actualdisk': 'scsi-360014055e15ae2781224b7c9ab26d356', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-360014055e15ae2781224b7c9ab26d356', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014055b5283bfdd2043a3bf1971b82': {'name': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'zname': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'actualdisk': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-0_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014055b5283bfdd2043a3bf1971b82', 'silvering': 'no', 'replacingroup': ''}, 'scsi-360014056eb348c244a842cbaccea920d': {'name': 'scsi-360014056eb348c244a842cbaccea920d', 'zname': 'scsi-360014056eb348c244a842cbaccea920d', 'actualdisk': 'scsi-360014056eb348c244a842cbaccea920d', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-1_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp222552', 'size': 10.7, 'devname': 'scsi-360014056eb348c244a842cbaccea920d', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405ac355cf3bb19410f952d8979c': {'name': 'scsi-36001405ac355cf3bb19410f952d8979c', 'zname': 'scsi-36001405ac355cf3bb19410f952d8979c', 'actualdisk': 'scsi-36001405ac355cf3bb19410f952d8979c', 'changeop': 'ONLINE', 'pool': 'pdhcp154702900', 'raid': 'mirror-1_pdhcp154702900', 'status': 'ONLINE', 'id': '0', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'scsi-36001405ac355cf3bb19410f952d8979c', 'silvering': 'no', 'replacingroup': ''}, 'scsi-36001405f7a3fb55b4f7491ab01efe331': {'name': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'actualdisk': 'scsi-36001405f7a3fb55b4f7491ab01efe331', 'zname': '', 'changeop': 'free', 'status': 'free', 'raid': 'free', 'pool': 'pree', 'id': '9', 'host': 'dhcp932129', 'size': 10.7, 'devname': 'sdt', 'silvering': 'no'}}
    if sys.argv[1] == 'select':
        selectdisks(leaderip, disks,disksinfo)
    elif sys.argv[1] == 'addtopool':
        selectdisks(leaderip, disks,disksinfo, addtopool)
    else:
        optimizedisks(leaderip, raid, disksinfo)

