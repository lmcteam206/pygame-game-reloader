import os
import time
import subprocess
import sys
import signal
import traceback
import pygetwindow as gw
import pyautogui
from screeninfo import get_monitors

# The script you want to reload (replace with your script's filename)
script_name = 't.py'

# Store the monitor index you want the window to appear on (e.g., 1 for the second monitor)
target_monitor_index = 1  # Change this to the monitor you want (0 is primary, 1 is secondary, etc.)

# Save the last known position of the window
last_position = (0, 0)

def get_window_position(window_title="Pygame"):
    """Get the position of the window if it's open."""
    global last_position
    try:
        # Try to find the window with the title 'Pygame'
        windows = gw.getWindowsWithTitle(window_title)
        if windows:
            win = windows[0]
            last_position = (win.left, win.top)
            return last_position
    except Exception as e:
        print(f"Error getting window position: {e}")
    return last_position

def move_window_to_position():
    """Move the window to the saved position."""
    try:
        windows = gw.getWindowsWithTitle("Pygame")
        if windows:
            win = windows[0]
            win.moveTo(last_position[0], last_position[1])
    except Exception as e:
        print(f"Error moving window: {e}")

def get_monitor_position(monitor_index=target_monitor_index):
    """Get the position of the monitor to place the window."""
    monitors = get_monitors()
    if monitor_index < len(monitors):
        monitor = monitors[monitor_index]
        return monitor.x, monitor.y
    return 0, 0  # Default to the primary monitor

def reload_script():
    """Reload the Pygame script."""
    try:
        # Start the script as a subprocess in a new window
        process = subprocess.Popen([sys.executable, script_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"Error launching the Pygame script: {e}")
        return None

def monitor_script():
    """Monitors the script for changes and reloads it."""
    last_modified_time = os.path.getmtime(script_name)
    process = None
    
    while True:
        current_modified_time = os.path.getmtime(script_name)
        
        if current_modified_time != last_modified_time:
            print(f"Change detected in {script_name}, restarting the script...")
            
            # If there is a running process, terminate it
            if process:
                process.terminate()
                process.wait()
                print("Old script process closed.")
            
            # Wait for 2 seconds before restarting
            time.sleep(2)
            
            # Save the position of the window before restarting
            get_window_position()
            
            # Reload the script
            process = reload_script()
            
            # Get the target monitor position and move the new window there
            monitor_position = get_monitor_position()
            pyautogui.moveTo(monitor_position[0], monitor_position[1])
            move_window_to_position()
            
            last_modified_time = current_modified_time
        
        # Check every 1 second
        time.sleep(1)

def run_with_debugger():
    """Run the script with a debugger that doesn't stop on errors."""
    try:
        # Ensure your script is executed
        monitor_script()
    except Exception as e:
        # Catch any exceptions and continue running the script
        print(f"Error occurred: {e}")
        print("Continuing without closing the program.")
        traceback.print_exc()

if __name__ == "__main__":
    print(f"Monitoring {script_name} for changes and running in debug mode...")
    run_with_debugger()
