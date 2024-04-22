import subprocess
import sys
# Start the Python script as a background process
subprocess.Popen(["python3", "./main.py", sys.argv[1]])
