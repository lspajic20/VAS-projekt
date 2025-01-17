import asyncio
from threading import Thread
from agent_light import LightAgent
from agent_person import PersonAgent
from dashboard import RealTimeDashboard
from agent_monitor import EnergyMonitorAgent

async def run_agents(light_agent):
    person_agent = PersonAgent("agent2osoba@jabber.cz", "agent22025")
    energy_monitor_agent = EnergyMonitorAgent("agent3osoba2@jabber.cz", "agent32025")

    await light_agent.start()
    await person_agent.start()
    await energy_monitor_agent.start()

    print("Agents are running. Press Ctrl+C to stop.")

    try:
        while light_agent.is_alive() and person_agent.is_alive() and energy_monitor_agent.is_alive():
            await asyncio.sleep(1)
    finally:
        print("Stopping agents...")
        await light_agent.stop()
        await person_agent.stop()
        await energy_monitor_agent.stop()


if __name__ == "__main__":
    light_agent = LightAgent("agent1svjetlo@jabber.cz", "agent12025")

    # Start the agents in a separate thread
    agent_thread = Thread(target=lambda: asyncio.run(run_agents(light_agent)), daemon=True)
    agent_thread.start()

    # Start the Tkinter dashboard in the main thread
    try:
        dashboard = RealTimeDashboard(light_agent)
        dashboard.start()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")