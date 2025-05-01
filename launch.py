import subprocess
import sys
import asyncio

from agents import Agent, Runner, function_tool

#!/usr/bin/env python3
"""
launch.py

A small utility to launch the Reaper app on macOS.
"""

@function_tool
def launch_reaper(mode: str) -> None:
    REAPER_PATH="/Applications/REAPER.app/Contents/MacOS/REAPER"
    """
    Launch Reaper. If path is provided, open that file in Reaper.
    """
    cmd = [REAPER_PATH]

    if mode:
        cmd.append(mode)
    else:
        print("plain launch")
    subprocess.run(cmd, check=True)


agent = Agent(
    name="Reaper",
    instructions="You are a Reaper Launch Agent.",
    tools=[launch_reaper],
)


async def main():
    # pick up a single optional path from the command line
    result = await Runner.run(agent, input="launch reaper mode nosplash")
    

if __name__ == "__main__":
    asyncio.run(main())


