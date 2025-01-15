from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import random
import asyncio

class PersonAgent(Agent):
    class MoveBehaviour(CyclicBehaviour):
        async def run(self):
            rooms = ["Living Room", "Kitchen", "Hallway"]
            current_room = random.choice(rooms)
            print(f"Person entered {current_room}")

            # Send a message to LightAgent
            msg = Message(to="agent1svjetlo@jabber.cz")  
            msg.body = f"Person entered {current_room}"
            await self.send(msg)

            # Simulate staying in the room for a few seconds
            await asyncio.sleep(random.randint(2, 5))

            # Send a message about exiting the room
            print(f"Person exited {current_room}")
            msg.body = f"Person exited {current_room}"
            await self.send(msg)

            await asyncio.sleep(random.randint(2, 5))  # Wait before moving again

    async def setup(self):
        print(f"PersonAgent {self.jid} is online.")
        move_behaviour = self.MoveBehaviour()
        self.add_behaviour(move_behaviour)
