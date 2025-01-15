from spade.agent import Agent
from spade.behaviour import OneShotBehaviour, CyclicBehaviour
from spade.message import Message
import asyncio

class PersonAgent(Agent):
    class SendMessageBehaviour(OneShotBehaviour):
        async def run(self):
            print("Waiting for the agent to be ready...")
            while not self.agent.client.is_connected():  
                await asyncio.sleep(1)
            print("Agent is ready. Sending a message to LightAgent...")
            
            msg = Message(to="agent1svjetlo@jabber.cz") 
            msg.body = "Turn on the light"
            await self.send(msg)
            print("Message sent!")

    class ReceiveMessageBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10) 
            if msg:
                print(f"PersonAgent received: {msg.body}") 

    async def setup(self):
        print(f"PersonAgent {self.jid} is online.")
        send_behaviour = self.SendMessageBehaviour()
        self.add_behaviour(send_behaviour)
        receive_behaviour = self.ReceiveMessageBehaviour()
        self.add_behaviour(receive_behaviour)
