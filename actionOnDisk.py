import sys, subprocess
from logmsg import sendlog, initlog
def control(argv):
    myhost = argv[1]
    leaderip = argv[4]
    request = argv[2]
    user = argv[3]
    action = argv[5]
    pool = argv[6]
    disk = argv[7]
    cmdline = ['zpool', action, pool, disk]
    result = subprocess.run(cmdline, capture_output=True)
    error = str(result.stderr.decode()).replace('\n\n','\n').split('\n')
    error = [i for i in error if i] 
    initlog(leaderip,myhost)
    if (not error or error[0] == ''):
        if (action == 'offline'):
            sendlog('Dist8:0', 'info', user, disk)
        else:
            sendlog('Dist10:0', 'info', user, disk)
        #return {'Status': 'Ok'}
    else:
        if (action == 'offline'):
            sendlog('Dist9', 'error', user, disk, error)
        else:
            sendlog('Dist11', 'error', user, disk, error)
        #return {'Status': 'ERROR', 'Error': error}
    
if __name__=='__main__':
    control(sys.argv)
