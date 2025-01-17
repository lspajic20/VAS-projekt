from spade.agent import Agent
from spade.behaviour import PeriodicBehaviour
from spade.message import Message

class EnergyMonitorAgent(Agent):
    class MonitorBehaviour(PeriodicBehaviour):
        def __init__(self, light_agent_jid, threshold=1):
            super().__init__(period=10)  # Check every 10 seconds
            self.light_agent_jid = light_agent_jid
            self.threshold = threshold

        async def run(self):
            # Request energy usage from LightAgent
            msg = Message(to=self.light_agent_jid)
            msg.body = "Request energy data"
            await self.send(msg)

            # Wait for the response
            response = await self.receive(timeout=5)
            if response:
                energy_data = eval(response.body)  # Assume LightAgent sends data as a dictionary
                for room, energy in energy_data.items():
                    if energy > self.threshold:
                        print(f"⚠️ Alert: {room} exceeded energy threshold with {energy:.2f}W.")
                        # Optionally send a message to LightAgent to take action
                        action_msg = Message(to=self.light_agent_jid)
                        action_msg.body = f"Alert: Reduce energy in {room}"
                        await self.send(action_msg)

    async def setup(self):
        print(f"EnergyMonitorAgent {self.jid} is online.")
        behaviour = self.MonitorBehaviour(light_agent_jid="agent1svjetlo@jabber.cz", threshold=1)
        self.add_behaviour(behaviour)
