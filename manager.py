from rich.console import Console
from rich.table import Table
import launch
import requests
import subprocess
from connect import WEB_INTERFACE_PORT

from agents import Agent, Runner, function_tool

class ReaperManager:
    """
    """
    def __init__(self) -> None:
        self.console = Console()
        self.track_agent = Agent(
            name="Reaper Track Manager",
            instructions="you are a Reaper DAW expert specialized in handling tracks",
            tools=[self.get_track, self.render_track, self.mute_track]
        )
        self.print_tools()

    def print_tools(self) -> None:
        """
        List available function tools in a table.
        """
        table = Table(title="Available Tools")
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="magenta")

        for tool in self.track_agent.tools:
            # unwrap FunctionTool to real function if needed
            name = tool.name
            desc = (tool.description or "").strip().splitlines()[0]
            table.add_row(name, desc)

        self.console.print(table)

    async def run(self, query: str) -> None:
        print("Running ReaperManager")
        print(query)
        result = await Runner.run(self.track_agent, input=query)

    async def launch_reaper(self, mode: str) -> None:
        REAPER_PATH="/Applications/REAPER.app/Contents/MacOS/REAPER"
        cmd = [REAPER_PATH]

        if mode:
            cmd.append(mode)
        else:
            print("plain launch")
        subprocess.run(cmd, check=True)

    @function_tool
    def get_track():
        """
        Fetch the list of tracks from the Reaper HTTP API and print the track names.
        """
        url = f"http://localhost:{WEB_INTERFACE_PORT}/_/TRACK"
        response = requests.get(url)
        response.raise_for_status()
        content = response.content.decode("utf-8")
        track_names = []
        for line in content.strip().splitlines():
            parts = line.split("\t")
            # parts: ["TRACK", idx, name, ...]
            if parts[0] == "TRACK" and len(parts) >= 3 and parts[2]:
                track_names.append(parts[2])
        print(track_names)
        return track_names

    @function_tool
    def render_track() -> None:
        """
        Trigger a project render via the Reaper HTTP API using code 41824.
        """
        url = f"http://localhost:{WEB_INTERFACE_PORT}/_/_RSe49ecb0e365cca5871337e8d657ab98a3197a6b2"
        response = requests.get(url)
        response.raise_for_status()
        print(f"Render command sent, status={response.status_code}")

    @function_tool
    def set_track_volume():
        "http://localhost:2307/_/SET/TRACK/2/VOL/{volume}"

    @function_tool
    def mute_track(track_id: int) -> None:
        """
        Mute the specified track via the Reaper HTTP API.
        """
        url = f"http://localhost:{WEB_INTERFACE_PORT}/_/SET/TRACK/{track_id}/MUTE/-2"
        response = requests.get(url)
        response.raise_for_status()
        print(f"Muted track {track_id}, status={response.status_code}")

    @function_tool
    def change_track_color():
        print("change track color")



