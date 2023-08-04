import sys, subprocess
from logmsg import sendlog, initlog
def control(argv):
    myhost = argv[1]
    leaderip = argv[3]
    user = argv[2]
    action = argv[4]
    pool = argv[5]
    disk = argv[6]
    cmdline = ['zpool', action, pool, disk]
    result = subprocess.run(cmdline, capture_output=True)
    error = str(result.stderr.decode()).replace('\n\n','\n').split('\n')
    error = [i for i in error if i] 
    initlog(leaderip,myhost)
    if (not error or error[0] == ''):
        if (action == 'offline'):
            sendlog('Dist8', 'info', user, disk)
        else:
            sendlog('Dist10', 'info', user, disk)
    else:
        if (action == 'offline'):
            sendlog('Dist9', 'error', user, disk)
        else:
            sendlog('Dist11', 'error', user, disk)
    
if __name__=='__main__':
    control(sys.argv)
