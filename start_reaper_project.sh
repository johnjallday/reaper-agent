#!/bin/bash

# orchestrator.sh
# 1. Checks if REAPER is running.
# 2. If not, runs reascripts.py to register scripts.
# 3. Then runs launch.py to start REAPER.
# 4. Runs main.py.

# --- Configuration ---
# Adjust this to how REAPER's process name appears on your system.
# Common patterns: "REAPER", "reaper", or part of the full path.
# Using a pattern that matches the .app name is often reliable on macOS.
# For example, if your REAPER.app is in /Applications/REAPER.app,
# its process might be identified by "REAPER.app/Contents/MacOS/REAPER" or just "REAPER".
# 'pgrep -l -f REAPER' in terminal while REAPER is running can help find the name.
REAPER_PROCESS_PATTERN="REAPER" # Try "REAPER.app" if "REAPER" is too generic

# Python interpreter command (e.g., python3, python)
PYTHON_CMD="python3"

# Paths to your Python scripts (assuming they are in the same directory as this shell script)
REASCRIPTS_PY_SCRIPT="./reascripts.py" # Script to register custom ReaScripts
LAUNCH_PY_SCRIPT="./launch.py"
MAIN_PY_SCRIPT="./main.py"

# Time to wait (in seconds) after launching REAPER for it to initialize
WAIT_AFTER_LAUNCH=5
# --- End Configuration ---

echo "------------------------------------"
echo "Starting REAPER Management Script"
echo "------------------------------------"

# Function to check if a process is running
is_process_running() {
  # pgrep -f matches against the full command line
  if pgrep -f "$1" >/dev/null; then
    return 0 # Process is running
  else
    return 1 # Process is not running
  fi
}

# 1. Check if REAPER is running
echo "[INFO] Checking if REAPER (matching pattern: '$REAPER_PROCESS_PATTERN') is running..."
if is_process_running "$REAPER_PROCESS_PATTERN"; then
  echo "[INFO] REAPER is already running."
else
  echo "[INFO] REAPER is not running."

  # 2. Run reascripts.py if REAPER is not running
  echo "[ACTION] Attempting to register ReaScripts using '$REASCRIPTS_PY_SCRIPT'..."
  if [ ! -f "$REASCRIPTS_PY_SCRIPT" ]; then
    echo "[WARNING] '$REASCRIPTS_PY_SCRIPT' not found. Skipping ReaScript registration."
  else
    "$PYTHON_CMD" "$REASCRIPTS_PY_SCRIPT"
    if [ $? -eq 0 ]; then
      echo "[INFO] '$REASCRIPTS_PY_SCRIPT' executed successfully."
    else
      echo "[ERROR] '$REASCRIPTS_PY_SCRIPT' failed to execute properly (exit code $?)."
      # Decide if you want to continue or exit if reascripts.py fails
      # For now, we'll continue and try to launch REAPER anyway.
    fi
  fi

  # 3. Launch REAPER using launch.py
  echo "[ACTION] Attempting to launch REAPER using '$LAUNCH_PY_SCRIPT'..."
  if [ ! -f "$LAUNCH_PY_SCRIPT" ]; then
    echo "[ERROR] '$LAUNCH_PY_SCRIPT' not found. Cannot launch REAPER."
    # Decide if you want to exit or try to run main.py anyway
    # exit 1
  else
    "$PYTHON_CMD" "$LAUNCH_PY_SCRIPT"

    if [ $? -eq 0 ]; then
      echo "[INFO] '$LAUNCH_PY_SCRIPT' executed. Waiting $WAIT_AFTER_LAUNCH seconds for REAPER to initialize..."
      sleep "$WAIT_AFTER_LAUNCH"

      # Optional: Re-check if REAPER started successfully
      if is_process_running "$REAPER_PROCESS_PATTERN"; then
        echo "[SUCCESS] REAPER appears to have started successfully."
      else
        echo "[WARNING] REAPER does not appear to be running after launch attempt via '$LAUNCH_PY_SCRIPT'."
        echo "[WARNING] '$MAIN_PY_SCRIPT' will still be attempted, but may not function correctly."
      fi
    else
      echo "[ERROR] '$LAUNCH_PY_SCRIPT' failed to execute properly (exit code $?)."
      echo "[WARNING] '$MAIN_PY_SCRIPT' will still be attempted, but REAPER is likely not running."
    fi
  fi
fi

# 4. Run main.py
echo "[ACTION] Proceeding to run '$MAIN_PY_SCRIPT'..."
if [ ! -f "$MAIN_PY_SCRIPT" ]; then
  echo "[ERROR] '$MAIN_PY_SCRIPT' not found. Cannot run main application."
  exit 1
fi

"$PYTHON_CMD" "$MAIN_PY_SCRIPT"

if [ $? -eq 0 ]; then
  echo "[SUCCESS] '$MAIN_PY_SCRIPT' executed successfully."
else
  echo "[ERROR] '$MAIN_PY_SCRIPT' exited with an error (exit code $?)."
fi

echo "------------------------------------"
echo "REAPER Management Script Finished"
echo "------------------------------------"
