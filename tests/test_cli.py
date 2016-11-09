import shlex
import signal
import subprocess
import sys
import time


def lcrs_subprocess(command_args=""):
    """
    Spawns a subprocess with the lcrs_embedded command, maintaining coverage
    metrics if coverage is installed.
    """
    try:
        import coverage  # @UnusedImport  # noqa
        interpreter = "coverage run -p"
    except ImportError:
        interpreter = sys.executable
    return subprocess.Popen(
        shlex.split(interpreter + " -m lcrs_embedded {}".format(command_args)),
    )


def test_cli():
    with lcrs_subprocess(" --port 42862") as p:
        # Give the new process enough time to start, coverage is also started
        time.sleep(0.5)
        p.send_signal(signal.SIGINT)
        p.communicate()
        time.sleep(1)
        assert p.returncode == 0, "Return code was {}".format(p.returncode)


def test_invalid_cli():
    with lcrs_subprocess("invalid arguments") as p:
        time.sleep(0.1)
        p.send_signal(signal.SIGINT)
        p.communicate()
        assert p.returncode != 0, "Return code was {}".format(p.returncode)
