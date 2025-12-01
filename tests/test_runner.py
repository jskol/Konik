import subprocess
import sys
from pathlib import Path
import pytest


TESTS_DIR = Path(__file__).parent


def collect_scripts():
    # Collect all python files in tests/ except pytest tests themselves
    for p in TESTS_DIR.glob("*.py"):
        if p.name.startswith("test_"):
            continue
        if p.name == Path(__file__).name:
            continue
        yield p


@pytest.mark.parametrize("script_path", list(collect_scripts()))
def test_run_script(script_path):
    """Run every script in the tests/ directory as a separate process.

    This verifies scripts execute without raising exceptions and are CI-friendly.
    Note: these scripts may reach out to the network — running them in CI can
    fail if the network or remote site is unavailable.
    """
    cmd = [sys.executable, str(script_path)]
    print("Running:", cmd)
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Print output to help debugging in CI logs
    print(result.stdout)
    print(result.stderr)
    assert result.returncode == 0, f"Script {script_path} failed with exit code {result.returncode}"
