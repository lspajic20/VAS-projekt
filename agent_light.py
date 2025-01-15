from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class LightAgent(Agent):
    class RespondBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.room_states = {}  # Dictionary to track the state of lights in rooms

        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for a message
            if msg:
                print(f"LightAgent received: {msg.body}")
                if "entered" in msg.body:
                    room = msg.body.split(" ")[-1]
                    self.room_states[room] = "ON"
                    print(f"Light in {room} turned ON.")
                elif "exited" in msg.body:
                    room = msg.body.split(" ")[-1]
                    self.room_states[room] = "OFF"
                    print(f"Light in {room} turned OFF.")

    async def setup(self):
        print(f"LightAgent {self.jid} is online.")
        behaviour = self.RespondBehaviour()
        self.add_behaviour(behaviour)
