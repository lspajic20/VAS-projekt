import tkinter as tk
from threading import Thread
import asyncio

class RealTimeDashboard:
    def __init__(self, light_agent):
        self.light_agent = light_agent
        self.root = tk.Tk()
        self.root.title("Real-Time Energy Analytics")
        self.labels = {}
        self.create_ui()

    def create_ui(self):
        tk.Label(self.root, text="Room", font=("Helvetica", 14)).grid(row=0, column=0)
        tk.Label(self.root, text="State", font=("Helvetica", 14)).grid(row=0, column=1)
        tk.Label(self.root, text="Total Energy (W)", font=("Helvetica", 14)).grid(row=0, column=2)
        tk.Label(self.root, text="Total ON Time (s)", font=("Helvetica", 14)).grid(row=0, column=3)

        for idx, room in self.light_agent.behaviours[0].room_states.keys():
            self.add_room_to_ui(idx, room)

    def add_room_to_ui(self, idx, room):
        tk.Label(self.root, text=room, font=("Helvetica", 12)).grid(row=idx, column=0)
        self.labels[room] = {
            "state": tk.Label(self.root, text="OFF", font=("Helvetica", 12)),
            "energy": tk.Label(self.root, text="0.00", font=("Helvetica", 12)),
            "time": tk.Label(self.root, text="0.00", font=("Helvetica", 12)),
        }
        self.labels[room]["state"].grid(row=idx, column=1)
        self.labels[room]["energy"].grid(row=idx, column=2)
        self.labels[room]["time"].grid(row=idx, column=3)

    async def update_ui(self):
        while True:
            for room in list(self.light_agent.behaviours[0].room_states.keys()):
                if room not in self.labels:
                    idx = len(self.labels) + 1
                    self.add_room_to_ui(idx, room)

                # Update room state
                state = self.light_agent.behaviours[0].room_states.get(room, "OFF")
                if room in self.labels:
                    self.labels[room]["state"].config(text=state)

                # Update energy and ON time
                energy = self.light_agent.behaviours[0].energy_usage.get(room, 0)
                on_time = self.light_agent.behaviours[0].total_on_time.get(room, 0)
                if room in self.labels:
                    self.labels[room]["energy"].config(text=f"{energy:.2f}")
                    self.labels[room]["time"].config(text=f"{on_time:.2f}")

            self.root.update_idletasks()
            self.root.update()
            await asyncio.sleep(1)

    def start(self, loop):
        asyncio.ensure_future(self.update_ui(), loop=loop)
        self.root.mainloop()
