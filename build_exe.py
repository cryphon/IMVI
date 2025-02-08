# build_exe.py
import os
import subprocess
import sys

# Paths
src_dir = os.path.join("src")
dist_dir = os.path.join("dist")

# Ensure the dist directory exists
if not os.path.exists(dist_dir):
    os.makedirs(dist_dir)

try:
    # Run PyInstaller using python -m method
    result = subprocess.run(
        [
            sys.
            executable,  # This ensures we use the correct Python interpreter
            "-m",
            "PyInstaller",
            "--onefile",
            "--distpath",
            dist_dir,
            "--workpath",
            "build",
            "--specpath",
            "build",
            os.path.join(src_dir, "IMVI.py")
        ],
        check=True,
        capture_output=True,
        text=True)

    print("PyInstaller stdout:", result.stdout)
    print("PyInstaller stderr:", result.stderr)
    print("PyInstaller build complete! Executable is in the 'dist' folder.")

except subprocess.CalledProcessError as e:
    print("PyInstaller build failed!")
    print("Error output:", e.stderr)
    sys.exit(1)
