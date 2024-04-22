import os
import psutil

script_name = "main.py"

# Get a list of all running Python processes
for process in psutil.process_iter(["name", "cmdline"]):
    print("process:",process)
    if "python3" in process.info["name"].lower():# and script_name in process.info["cmdline"]:
        # Get the PID of the process
        pid = process.pid
        print("PID:", pid)

        # Terminate the process
        process = psutil.Process(pid)
        process.terminate()
