#!/usr/bin/env python
#coding:utf8
import sys, os
import pexpect

def drozer_detect():
    packgename = 'com.kuaiche.freight.driver'
    components = ['activity', 'broadcast', 'service']
    #components = ['service']

    os.chdir('/home/drozer')
    os.system('adb forward tcp:31415 tcp:31415')
    child = pexpect.spawn("drozer console connect")
    child.expect('dz>')
    print child.before
    
    for component in components:
        command = 'run apksec.'+component+'.detect -a ' + packgename + '\n'
        child.sendline(command)
        child.expect('dz>')
        opening_brace_index = child.before.find('{')
        detect_result = child.before[opening_brace_index:]
        print detect_result #-->database
        child.expect('dz>')

    child.sendline('exit()')


def format_detect_result(expect_output):
    opening_brace_index = expect_output.find('{')
    detect_result = expect_output[opening_brace_index:]
    return detect_result


def main():
    """A demo daemon main routine, write a datestamp to
        /tmp/daemon-log every 10 seconds.
    """
    import time
    f = open("/tmp/daemon-log", "w")
    while 1:
        f.write('%s/n' % time.ctime(time.time()))
        f.flush()
        time.sleep(10)

if __name__ == "__main__":
    # do the UNIX double-fork magic, see Stevens' "Advanced
    # Programming in the UNIX Environment" for details (ISBN 0201563177)
    try:
        pid = os.fork()
        if pid > 0:
            # exit first parent
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #1 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    # decouple from parent environment
    #os.chdir("/")
    os.chdir('/home/drozer')
    os.setsid()
    os.umask(0)
    # do second fork
    try:
        pid = os.fork()
        if pid > 0:
            # exit from second parent, print eventual PID before
            print "Daemon PID %d" % pid
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, "fork #2 failed: %d (%s)" % (e.errno, e.strerror)
        sys.exit(1)
    # start the daemon main loop
    #main()
    drozer_detect()
