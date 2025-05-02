# reaper-agent

A small CLI & agent framework for launching REAPER on macOS and managing tracks via the Reaper HTTP API.

## Features

- Launch the REAPER application (with optional flags or project file)
- List all tracks in the current project
- Mute tracks
- Trigger a full project render

## Requirements

- macOS with [REAPER](https://www.reaper.fm/) installed under `/Applications/REAPER.app`  
- Python 3.13+
- uv

## Installation
```bash
# Using pip to install uv
pip install uv 
# Verify the installation
uv --version


1. Clone the repo:
   ```bash
   git clone https://github.com/johnjallday/reaper-agent.git
   cd reaper-agent
2. Run
   uv run main.py 

just type away
