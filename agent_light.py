from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class LightAgent(Agent):
    class RespondBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for a message
            if msg:
                print(f"LightAgent received: {msg.body}")
                # Respond based on the message body
                if "Turn on the light" in msg.body:
                    reply = Message(to=str(msg.sender))
                    reply.body = "The light is now ON!"
                    await self.send(reply)
                elif "Turn off the light" in msg.body:
                    reply = Message(to=str(msg.sender))
                    reply.body = "The light is now OFF!"
                    await self.send(reply)

    async def setup(self):
        print(f"LightAgent {self.jid} is online.")
        behaviour = self.RespondBehaviour()
        self.add_behaviour(behaviour)
