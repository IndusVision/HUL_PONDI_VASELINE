import subprocess
import time
import os
import signal
import shutil
PYTHON_PATH = r"C:/Users/pc/miniconda3/envs/yolo/python.exe"

PID_FILE = "line_2_workers.pid"  # Stores worker PIDs
STOP_FILE = "stop_line_2.flag"    # Signal file to stop monitoring

ROOT_DIR=os.path.abspath(os.path.join(os.path.dirname(__file__),".."))

DETACHED_PROCESS = subprocess.DETACHED_PROCESS
CREATE_NO_WINDOW = subprocess.CREATE_NO_WINDOW

PARENT_PID = os.getpid()

def stop_all_workers(signum=None, frame=None):
    # 1️ Create stop flag to tell spawn script to exit
    print('INTERRUPT Received !!!!')
    with open(STOP_FILE, "w") as f:
        f.write("stop")

    # 2️ Kill all running workers
    if os.path.exists(PID_FILE):
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

def start_worker(script, active_process_ids= None):
    """Start a worker subprocess and log its PID."""
    proc = subprocess.Popen(
        [PYTHON_PATH, script, str(PARENT_PID)],  # No shell=True for clean PIDs
        # stdout=subprocess.DEVNULL,
        # stderr=subprocess.DEVNULL,
        # creationflags=CREATE_NO_WINDOW | DETACHED_PROCESS
    )
    if active_process_ids is None:
        with open(PID_FILE, "a") as f:
            f.write(f"{proc.pid}\n")
    else:
        with open(PID_FILE, "w") as f:
                active_process_ids = map(str, active_process_ids)
                pid_string = "\n".join(active_process_ids)
                pid_string = pid_string + "\n" + str(proc.pid)
                f.write(pid_string)
    return proc

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def terminate_all_workers(processes):
    """Terminate all workers gracefully."""
    for script, process in processes.items():
        if process.poll() is None:
            try:
                process.terminate()
                process.wait(timeout=3)
            except:
                process.kill()
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)

def monitor_workers(scripts):
    # Clean up old PID file
    if os.path.exists(PID_FILE):
        os.remove(PID_FILE)
    if os.path.exists(STOP_FILE):
        os.remove(STOP_FILE)
    
    processes = {script: start_worker(script) for script in scripts}
    print(f"Initial processes started: {processes}")

    try:
        while True:
            # Check for stop signal
            if os.path.exists(STOP_FILE):
                print("Stop signal received. Shutting down workers...")
                break

            clear_terminal()
            print(f"Monitoring {len(processes)} workers... (Press CTRL+C to exit manually)")
            for script, process in list(processes.items()):
                if process.poll() is not None:  # If worker stopped/crashed
                    print(f"[{time.strftime('%H:%M:%S')}] {script} crashed. Restarting...")
                    process_ids = [process.pid for _, process in list(processes.items())]
                    process_ids.remove(process.pid)
                    processes[script] = start_worker(script, active_process_ids=process_ids)

            time.sleep(1)

    except KeyboardInterrupt:
        print("Manual interrupt detected. Shutting down...")

    finally:
        terminate_all_workers(processes)
        if os.path.exists(STOP_FILE):
            os.remove(STOP_FILE)  # Remove stop flag after exit
        print("All workers have been terminated.")


if __name__ == '__main__':
   

    # pyinstaller --onefile -c your_script_name.py
    signal.signal(signal.SIGINT, stop_all_workers)
    

    worker_scripts = [
         os.path.join(ROOT_DIR, "vaseline_line_2","src", "ocr.py"),
        os.path.join(ROOT_DIR, "vaseline_line_2","src","after_filling.py"),
        os.path.join(ROOT_DIR, "vaseline_line_2","src", "before_filling.py"),
    ]

    monitor_workers(worker_scripts)
