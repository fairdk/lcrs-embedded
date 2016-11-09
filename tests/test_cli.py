import shlex
import signal
import subprocess
import sys
import time

import pytest
from argh.exceptions import CommandError


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
    p = subprocess.Popen(
        shlex.split(interpreter + " -m lcrs_embedded {}".format(command_args)),
        stderr=subprocess.PIPE,
    )
    # Give the new process enough time to start, coverage is also started
    # Todo... how can we replace this with a better check? 0.8 is because of
    # Travis slowness..
    time.sleep(0.8)
    p.send_signal(signal.SIGINT)
    stdout, stderr = p.communicate()
    if p.returncode > 0:
        raise CommandError(
            (
                "Non-zero returncode. Returncode was {}.\n\nstdout:\n{}"
                "\n\nstderr:\n{}"
            ).format(
                p.returncode,
                stdout,
                stderr,
            )
        )
    return p


def test_cli():
    with lcrs_subprocess(" --port 42862"):
        time.sleep(0.1)


def test_invalid_cli():
    with pytest.raises(CommandError):
        with lcrs_subprocess("invalid arguments"):
            time.sleep(0.1)
