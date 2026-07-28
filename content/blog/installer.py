import os
import platform
import subprocess
import time
import urllib.request
from pathlib import Path

# ---- Configuration ----
RECORDER_URL_WINDOWS = os.environ.get("WINDOWS_RECORDING_URL")
RECORDER_URL_MAC = os.environ.get("MAC_RECORDING_URL")
SEB_URL = os.environ.get("SEB_URL")

WORK_DIR = Path.home() / "icpc_exam_session"
EXAM_DURATION_SECONDS = 4 * 3600 + 10 * 60  # 4h10m
RECORDER_PORT = 23456
if platform.system() == "Windows":
    WORK_DIR = Path(os.environ["PROGRAMDATA"]) / "ICPC" / "exam_session"
else:
    WORK_DIR = Path("/Library/Application Support/ICPC/exam_session")
WORK_DIR.mkdir(parents=True, exist_ok=True)
WORK_DIR.mkdir(parents=True, exist_ok=True)


def download(url, dest):
    print(f"Downloading {url} -> {dest}")
    urllib.request.urlretrieve(url, dest)
    return dest


def kill_process_on_port(port):
    system = platform.system()
    if system == "Windows":
        result = subprocess.run(
            ["netstat", "-ano"], capture_output=True, text=True
        )
        for line in result.stdout.splitlines():
            if f":{port}" in line:
                parts = line.split()
                pid = parts[-1]
                print(f"Killing PID {pid} on port {port}")
                subprocess.run(["taskkill", "/F", "/PID", pid], check=False)
    else:
        result = subprocess.run(
            ["lsof", "-t", f"-i:{port}"], capture_output=True, text=True
        )
        pids = result.stdout.split()
        for pid in pids:
            print(f"Killing PID {pid} on port {port}")
            subprocess.run(["kill", "-9", pid], check=False)

def remove_quarantine(path):
    subprocess.run(["xattr", "-dr", "com.apple.quarantine", str(path)], check=False)


def run_recorder(system):
    if system == "Windows":
        recorder_path = download(RECORDER_URL_WINDOWS, WORK_DIR / "recorder.exe")
        proc = subprocess.Popen([str(recorder_path)])
    else:
        zip_path = download(RECORDER_URL_MAC, WORK_DIR / "recorder.app.zip")
        subprocess.run(["unzip", "-o", str(zip_path), "-d", str(WORK_DIR)], check=True)
        app_path = WORK_DIR / "recorder.app"
        remove_quarantine(app_path)
        proc = subprocess.Popen(["open", "-W", str(app_path)])
    return proc


def open_seb():
    seb_path = download(SEB_URL, WORK_DIR / "exam.seb")
    system = platform.system()
    if system == "Windows":
        os.startfile(str(seb_path))
    elif system == "Darwin":
        subprocess.run(["open", str(seb_path)], check=True)
    else:
        subprocess.run(["xdg-open", str(seb_path)], check=True)


def cleanup():
    print("Exam period ended. Cleaning up files")
    for f in WORK_DIR.glob("*"):
        try:
            if f.is_dir():
                for sub in f.rglob("*"):
                    sub.unlink(missing_ok=True)
                f.rmdir()
            else:
                f.unlink()
        except Exception as e:
            print(f"Failed to delete {f}: {e}")
    try:
        WORK_DIR.rmdir()
    except Exception:
        pass


def main():
    system = platform.system()

    kill_process_on_port(RECORDER_PORT)

    recorder_proc = run_recorder(system)
    time.sleep(5)  # allow recorder to initialize before exam browser starts

    open_seb()

    print(f"Exam session running for {EXAM_DURATION_SECONDS} seconds.")
    time.sleep(EXAM_DURATION_SECONDS)

    if recorder_proc.poll() is None:
        recorder_proc.terminate()

    kill_process_on_port(RECORDER_PORT)
    cleanup()


if __name__ == "__main__":
    main()