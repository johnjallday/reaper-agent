import subprocess
import os
import sys
import asyncio

from agents import Agent, Runner, function_tool

#!/usr/bin/env python3
"""
launch.py

A small utility to launch the Reaper app on macOS.
"""


#@function_tool
def launch_reaper(project_path: str = None) -> None:
    """
    Launch Reaper. If project_path is provided, open that file in Reaper.
    """
    REAPER_PATH = os.getenv("REAPER_PATH") or "/Applications/REAPER.app/Contents/MacOS/REAPER"
    cmd = [REAPER_PATH]

    if project_path:
        cmd.append(project_path)
    else:
        cmd.append("-new")
        print("plain launch")
    # detach so Python keeps running
    subprocess.Popen(cmd)




async def main():
    # pick up a single optional path from the command line
    #result = await Runner.run(agent, input="launch reaper /Users/jj/Workspace/Allday-Music/ichillin/ichillin_Title/ichillin_Title.RPP")
    project_path = '/Users/jj/Workspace/Allday-Music/music_production/on-going/waterfall/waterfall.RPP'

    launch_reaper(project_path)
    

if __name__ == "__main__":
    asyncio.run(main())


