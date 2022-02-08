"""
Created on Tue, Feb 08 13:58:00 2022
@license: MIT License
@author: eiproject (https://github.com/eiproject)

"""
import os
import subprocess as sp

try:
    from subprocess import DEVNULL    # Python 3
except ImportError:
    DEVNULL = open(os.devnull, 'wb')  # Python 2

    
def try_cmd(cmd):
    try:
        popen_params = {
            "stdout": sp.PIPE,
            "stderr": sp.PIPE,
            "stdin": DEVNULL
        }

        # This was added so that no extra unwanted window opens on windows
        # when the child process is created
        if os.name == "nt":
            popen_params["creationflags"] = 0x08000000

        proc = sp.Popen(cmd, **popen_params)
        proc.communicate()
    except Exception as err:
        return False, err
    else:
        return True, None
    
    
def subprocess_call(cmd:str):
    '''Subprocess calling a command and give error logs'''
    is_errors = False
    try:
        p = sp.Popen(cmd, stdout=sp.PIPE, stderr=sp.PIPE, shell=True)
        stdoutdata, stderrdata = p.communicate()
        if p.wait() != 0:
            stderrmsg = cmd.split(' ')[0] + " > " + str(stderrdata).split('\\r\\n')[-2]
            is_errors = True
            print("Error: " + stderrmsg)
            return stderrdata, is_errors
        # no error
        return stderrdata, is_errors
    except OSError as e:
        is_errors = True
        return e.strerror, is_errors