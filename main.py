import asyncio
from agent_light import LightAgent
from agent_person import PersonAgent

async def main():
    # Initialize agents
    light_agent = LightAgent("agent1svjetlo@jabber.cz", "agent12025")
    person_agent = PersonAgent("agent2osoba@jabber.cz", "agent22025")

    # Start agents
    await light_agent.start()
    await person_agent.start()

    print("Agents are running. Press Ctrl+C to stop.")
    try:
        while light_agent.is_alive() and person_agent.is_alive():
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        print("Shutting down gracefully...")
    finally:
        print("Stopping agents...")
        await light_agent.stop()
        await person_agent.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
