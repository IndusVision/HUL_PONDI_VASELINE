import os
import subprocess

PID_FILE = "workers.pid"
STOP_FILE = "stop.flag"

def stop_all_workers():
    # 1️ Create stop flag to tell spawn script to exit
    

    # 2️ Kill all running workers
    if os.path.exists(PID_FILE):
        with open(STOP_FILE, "w") as f:
            f.write("stop")
        with open(PID_FILE, "r") as f:
            pids = f.readlines()

        for pid in pids:
            pid = pid.strip()
            if pid:
                subprocess.run(f"taskkill /F /T /PID {pid}", shell=True)
                print(f"Killed worker with PID {pid}")

        os.remove(PID_FILE)
    else:
        print("No PID file found. Workers might not be running.")

if __name__ == "__main__":
    stop_all_workers()
