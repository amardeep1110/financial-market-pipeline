import os
import subprocess
import sys


project_root = os.path.dirname(os.path.abspath(__file__))

env = os.environ.copy()
env["PYTHONPATH"] = project_root


subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        "dashboard/app.py",
    ],
    env=env,
)
