import asyncio
from threading import Thread
from agent_light import LightAgent
from agent_person import PersonAgent
from dashboard import RealTimeDashboard

async def main():
    light_agent = LightAgent("agent1svjetlo@jabber.cz", "agent12025")
    person_agent = PersonAgent("agent2osoba@jabber.cz", "agent22025")

    await light_agent.start()
    await person_agent.start()

    print("Agents are running. Press Ctrl+C to stop.")

    try:
        loop = asyncio.get_event_loop()
        dashboard = RealTimeDashboard(light_agent)
        Thread(target=dashboard.start, args=(loop,), daemon=True).start()

        while light_agent.is_alive() and person_agent.is_alive():
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down gracefully...")
    finally:
        print("Stopping agents...")
        await light_agent.stop()
        await person_agent.stop()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")