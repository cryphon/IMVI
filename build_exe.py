# build_exe.py
import os
import platform
import shutil
import subprocess
import sys

# Paths
src_dir = os.path.join("src")
dist_dir = os.path.join("dist")
build_dir = os.path.join("build")
source_qss = os.path.join("css", "style.qss")
build_css_dir = os.path.join(build_dir, "css")

# Platform-specific path separator for PyInstaller
# On Windows, it needs to be ';' and on Unix-like systems ':'
separator = ';' if platform.system() == 'Windows' else ':'

os.makedirs(build_dir, exist_ok=True)
os.makedirs(dist_dir, exist_ok=True)
os.makedirs(build_css_dir, exist_ok=True)

try:
    shutil.copy2(source_qss, build_css_dir)
    print(f"Copied {source_qss} to {build_css_dir}")
except Exception as e:
    print(f"Error copying QSS file: {e}")
    sys.exit(1)

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
            f"--add-data={source_qss}{';' if sys.platform == 'win32' else ':'}css",
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
