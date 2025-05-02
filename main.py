import asyncio
from manager import ReaperManager

async def main() -> None:
    # instantiate and print available tools up front
    mgr = ReaperManager()
    # now prompt the user
    query = input("Enter a Reaper task: ")
    await mgr.run(query)

if __name__ == "__main__":
    asyncio.run(main())
