import asyncio
from manager import ReaperManager

async def main() -> None:
    query = input("Enter a Reaper task: ")

    mgr = ReaperManager()
    await mgr.run(query)

if __name__ == "__main__":
    asyncio.run(main())
