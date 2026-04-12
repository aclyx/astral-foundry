import asyncio

import httpx
from api.main import create_app


async def main() -> None:
    # Async pays for itself at I/O boundaries.
    # ASGITransport keeps the example runnable without a live server.
    transport = httpx.ASGITransport(app=create_app())
    async with httpx.AsyncClient(transport=transport, base_url="http://astral-foundry.local") as client:
        response = await client.get("/items", params={"limit": 2})
        response.raise_for_status()
        for item in response.json()["items"]:
            print(f"{item['id']}: {item['title']}")


# TODO: Add explicit timeout handling when you swap the in-memory app
# for a real network call.
if __name__ == "__main__":
    asyncio.run(main())
