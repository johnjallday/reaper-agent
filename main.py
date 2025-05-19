import os
import asyncio
from connect import is_connected, add_web_interface, WEB_INTERFACE_PORT
from manager import ReaperManager
from launch import launch_reaper
from reascripts import register_scripts

async def main() -> None:
    # ensure the Reaper HTTP interface is running (or install it)

    #launch_reaper()
    print("success")
    connected, code = is_connected()
    if not connected:
        print(f"Reaper HTTP interface not reachable (code={code}), installing…")
        #add_web_interface(os.getcwd(), WEB_INTERFACE_PORT)
        #launch_reaper()

    # now instantiate and print available tools up front
    mgr = ReaperManager()

    # simple REPL
    while True:
        query = input("Enter a Reaper task (or 'exit'): ")
        if query.strip().lower() in ("exit", "quit"):
            print("Goodbye!")
            break
        await mgr.run(query)

if __name__ == "__main__":
    asyncio.run(main())
