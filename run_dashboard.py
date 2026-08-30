import os
import sys
import subprocess


PROJECT_ROOT = os.path.dirname(
    os.path.abspath(__file__)
)

sys.path.insert(0, PROJECT_ROOT)


dashboard_path = os.path.join(
    PROJECT_ROOT,
    "dashboard",
    "app.py",
)


subprocess.run(
    [
        sys.executable,
        "-m",
        "streamlit",
        "run",
        dashboard_path,
    ],
    check=True,
)
