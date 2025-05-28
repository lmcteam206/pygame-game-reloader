import os
import time
import subprocess
import sys
import traceback
import pygetwindow as gw
import pyautogui
from screeninfo import get_monitors

# Your target script
script_name = r'tests/t1.py'

# Which monitor (0 = primary, 1 = secondary, etc.)
target_monitor_index = 1

# Window title that your GUI script creates
WINDOW_TITLE = "big"  # For Pygame, match with set_caption(); for Dear PyGui, match viewport title

# To remember the last position
last_position = (0, 0)

def get_window_position(window_title=WINDOW_TITLE):
    global last_position
    try:
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            win = windows[0]
            last_position = (win.left, win.top)
            return last_position
    except Exception as e:
        print(f"Error getting window position: {e}")
    return last_position

def move_window_to_position():
    try:
        windows = gw.getWindowsWithTitle(WINDOW_TITLE)
        if windows:
            win = windows[0]
            win.moveTo(*last_position)
    except Exception as e:
        print(f"Error moving window: {e}")

def get_monitor_position(monitor_index=target_monitor_index):
    monitors = get_monitors()
    if monitor_index < len(monitors):
        monitor = monitors[monitor_index]
        return monitor.x, monitor.y
    return 0, 0  # default to primary

def reload_script():
    try:
        print(f"Launching: {script_name}")
        return subprocess.Popen(
            [sys.executable, script_name],
            stdout=None, stderr=None
        )
    except Exception as e:
        print(f"Failed to launch script: {e}")
        return None

def monitor_script():
    if not os.path.exists(script_name):
        print(f"Script {script_name} does not exist.")
        return

    last_modified_time = os.path.getmtime(script_name)
    process = reload_script()

    while True:
        try:
            current_modified_time = os.path.getmtime(script_name)
            if current_modified_time != last_modified_time:
                print("Change detected. Restarting...")

                if process:
                    process.terminate()
                    process.wait()
                    print("Previous process terminated.")

                time.sleep(1)  # short delay before restarting
                get_window_position()
                process = reload_script()

                monitor_position = get_monitor_position()
                pyautogui.moveTo(*monitor_position)
                time.sleep(1)  # give time for the window to appear
                move_window_to_position()

                last_modified_time = current_modified_time

            time.sleep(1)

        except Exception as e:
            print(f"Monitoring error: {e}")
            traceback.print_exc()

def run():
    print(f"Watching: {script_name}")
    monitor_script()

if __name__ == "__main__":
    run()
