import os
import asyncio
from connect import is_connected, add_web_interface, WEB_INTERFACE_PORT
from manager import ReaperManager

async def main() -> None:
    # ensure the Reaper HTTP interface is running (or install it)
    connected, code = is_connected()
    if not connected:
        print(f"Reaper HTTP interface not reachable (code={code}), installing…")
        add_web_interface(os.getcwd(), WEB_INTERFACE_PORT)

    # now instantiate and print available tools up front
    mgr = ReaperManager()

    # now prompt the user
    query = input("Enter a Reaper task: ")
    await mgr.run(query)

if __name__ == "__main__":
    asyncio.run(main())
