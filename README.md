# 🌀 Pygame Auto Reloader with Window Memory and Multi-Monitor Support

This Python script automatically monitors and reloads your Pygame development script when changes are detected. It remembers the window position, supports multi-monitor setups, and runs in a debug-safe environment that doesn’t crash on script errors.

---

## 🔧 Features

- ✅ **Automatic Reloading**: Detects file changes and restarts your Pygame script.
- ✅ **Multi-Monitor Support**: Opens the game window on your desired monitor.
- ✅ **Window Position Memory**: Remembers and restores the last window position.
- ✅ **Safe Debugging**: Does not exit on Python script errors—prints traceback instead.
- ✅ **2-Second Restart Delay**: Ensures your changes save properly before reload.

---

## 🚀 Requirements

Install the dependencies using pip:

```bash
pip install pygetwindow pyautogui screeninfo
