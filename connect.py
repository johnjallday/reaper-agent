import subprocess

def is_connected(url='http://localhost:2307/', timeout=5):
    """
    Check HTTP connectivity to the given URL.
    Returns a tuple (success, status_code).
    success is True if the HTTP status code is 200.
    status_code is the HTTP status code returned, or None on error.
    """
    cmd = ['curl', '-s', '-o', '/dev/null', '-w', '%{http_code}', url]
    try:
        output = subprocess.check_output(cmd, stderr=subprocess.DEVNULL, timeout=timeout)
        status_str = output.decode().strip()
        try:
            status_code = int(status_str)
        except ValueError:
            return False, None
        return (status_code == 200), status_code
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return False, None



