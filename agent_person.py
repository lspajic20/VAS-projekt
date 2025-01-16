from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import random

class PersonAgent(Agent):
    class RoutineBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            # Define multiple routines
            self.morning_routine = ["Bedroom", "Bathroom", "Kitchen", "LivingRoom"]
            self.evening_routine = ["LivingRoom", "DiningRoom", "Bathroom", "Bedroom"]
            self.random_routine = ["Office", "LivingRoom", "Bathroom", "Hallway"]


            # Start with a default routine
            self.current_routine = self.morning_routine
            self.current_step = 0  # Track the current step in the routine

        async def run(self):
            # Get the current room from the active routine
            current_room = self.current_routine[self.current_step]
            print(f"Person entered {current_room}")

            # Send "entered" message to LightAgent
            msg = Message(to="agent1svjetlo@jabber.cz")  
            msg.body = f"Person entered {current_room}"
            await self.send(msg)

            # Simulate staying in the room for a while
            await asyncio.sleep(random.randint(2, 5))

            # Send "exited" message to LightAgent
            print(f"Person exited {current_room}")
            msg.body = f"Person exited {current_room}"
            await self.send(msg)

            # Move to the next step in the routine
            self.current_step = (self.current_step + 1) % len(self.current_routine)

            # Dynamically switch routines
            if random.random() < 0.1:  # 10% chance to switch routine
                self.switch_routine()

        def switch_routine(self):
            # Switch to a different routine
            if self.current_routine == self.morning_routine:
                self.current_routine = self.evening_routine
                print("Switched to Evening Routine!")
            elif self.current_routine == self.evening_routine:
                self.current_routine = self.random_routine
                print("Switched to Random Routine!")
            else:
                self.current_routine = self.morning_routine
                print("Switched to Morning Routine!")

    async def setup(self):
        print(f"PersonAgent {self.jid} is online.")
        routine_behaviour = self.RoutineBehaviour()
        self.add_behaviour(routine_behaviour)
