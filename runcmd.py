import subprocess


class CalledProcessError(SubprocessError):
    """This exception is raised when a process run by check_call() or
    check_output() returns a non-zero exit status.
    The exit status will be stored in the returncode attribute;
    check_output() will also store the output in the output attribute.
    """
    def __init__(self, returncode, cmd, output=None, error=None):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.error = error
    def __str__(self):
        return "Command '%s' returned non-zero exit status %d" % (self.cmd, self.returncode)


def check_cmd(*popenargs, **kwargs):
    """Run command with arguments.  Wait for command to complete.  If
    the exit code was zero then return, otherwise raise
    CalledProcessError.  The CalledProcessError object will have the
    return code in the returncode attribute.

    The arguments are the same as for the call function.  Example:

    check_call(["ls", "-l"])
    """
    if 'stdout' in kwargs:
        raise ValueError("cannot use argument stdout, it will be overwritten")
    if 'stderr' in kwargs:
        raise ValueError("cannot use argument stderr, it will be overwritten")
    proc = subprocess.Popen(*popenargs, stdout=subprocess.PIPE,
        stderr=subprocess.PIPE, **kwargs)
    out, err = proc.communicate()
    retcode = proc.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise CalledProcessError(retcode, cmd, out, err)
    return out, err

def runcmd(*popenargs, **kwargs):
    """Run command with check_call. If the command returns 1, print stdout and
    stderr. IF verbose, print the command, the stdout, else return the stdout
    for (probable) parsing.
    """
    if 'verbose' in kwargs:
        print(''.join(popenargs[0]))
        verbose = True
    else:
        verbose = False
    try:
        out, err = check_call(*popenargs, **kwargs)
    except CalledProcessError as e:
        print(e)
        print(e.output)
        print(e.error)
        exit(1)
    if verbose:
        print(out)
        print(err)
    return out, err

