from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message
import asyncio
import time
import csv

class LightAgent(Agent):
    class RespondBehaviour(CyclicBehaviour):
        def __init__(self):
            super().__init__()
            self.room_states = {}  # Track the state of lights (ON/OFF)
            self.energy_usage = {}  # Track energy consumption for each room
            self.light_on_times = {}  # Track when lights were turned ON
            self.total_on_time = {}  # Track cumulative ON time for each room

        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for a message
            if msg:
                    print(f"LightAgent received: {msg.body}")

                    if "entered" in msg.body:
                        room = msg.body.split(" ")[-1]
                        self.turn_on_light(room)

                    elif "exited" in msg.body:
                        room = msg.body.split(" ")[-1]
                        self.turn_off_light(room)

                    elif msg.body == "Request energy data":
                        # Send energy usage data to the requesting agent
                        response = Message(to=str(msg.sender))
                        response.body = str(self.energy_usage)
                        await self.send(response)
                        print("Energy data sent to EnergyMonitorAgent")

        def turn_on_light(self, room):
            if self.room_states.get(room) != "ON":
                self.room_states[room] = "ON"
                self.light_on_times[room] = time.time()  # Record when the light was turned ON
                print(f"Light in {room} turned ON.")

        def turn_off_light(self, room):
            if self.room_states.get(room) == "ON":
                self.room_states[room] = "OFF"

                # Calculate ON duration
                on_duration = time.time() - self.light_on_times.pop(room, time.time())
                self.total_on_time[room] = self.total_on_time.get(room, 0) + on_duration

                # Calculate energy usage
                energy_used = on_duration * 0.1  # Example: 0.1W per second
                self.energy_usage[room] = self.energy_usage.get(room, 0) + energy_used

                print(f"Light in {room} turned OFF. Duration ON: {on_duration:.2f}s, Energy used: {energy_used:.2f}W")

    class ReportBehaviour(CyclicBehaviour):
        async def run(self):
            await asyncio.sleep(30)  # Report every 30 seconds
            print("\n--- Energy and Time ON Report ---")
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")

            # Prepare data for saving
            report_data = []
            for room in self.agent.behaviours[0].energy_usage.keys():
                total_energy = self.agent.behaviours[0].energy_usage.get(room, 0)
                total_time = self.agent.behaviours[0].total_on_time.get(room, 0)
                report_data.append([timestamp, room, total_energy, total_time])
                print(f"Room: {room}, Total Energy: {total_energy:.2f}W, Total ON Time: {total_time:.2f}s")

            # Save to CSV
            with open("energy_log.csv", "a", newline="") as file:
                writer = csv.writer(file)
                if file.tell() == 0:  # Write header only if file is empty
                    writer.writerow(["Timestamp", "Room", "Total Energy (W)", "Total ON Time (s)"])
                writer.writerows(report_data)

            print("Report saved to energy_log.csv")

    async def setup(self):
        print(f"LightAgent {self.jid} is online.")
        respond_behaviour = self.RespondBehaviour()
        report_behaviour = self.ReportBehaviour()
        self.add_behaviour(respond_behaviour)
        self.add_behaviour(report_behaviour)