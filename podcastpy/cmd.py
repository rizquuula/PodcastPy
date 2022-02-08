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