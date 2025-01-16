import tkinter as tk


class RealTimeDashboard:
    def __init__(self, light_agent):
        self.light_agent = light_agent
        self.root = tk.Tk()
        self.root.title("Real-Time Energy Analytics")
        self.labels = {}
        self.canvas = None
        self.rooms = {}  # For room visualization
        self.agent_marker = None
        self.create_ui()

    def create_ui(self):
        # Room state table
        tk.Label(self.root, text="Room", font=("Helvetica", 14)).grid(row=0, column=0)
        tk.Label(self.root, text="State", font=("Helvetica", 14)).grid(row=0, column=1)
        tk.Label(self.root, text="Total Energy (W)", font=("Helvetica", 14)).grid(row=0, column=2)
        tk.Label(self.root, text="Total ON Time (s)", font=("Helvetica", 14)).grid(row=0, column=3)

        # Canvas for room visualization
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.grid(row=0, column=4, rowspan=10)

    def update_ui(self):
        # Safely access LightAgent's behaviour data
        if self.light_agent and self.light_agent.behaviours:
            try:
                room_states = self.light_agent.behaviours[0].room_states
                energy_usage = self.light_agent.behaviours[0].energy_usage
                total_on_time = self.light_agent.behaviours[0].total_on_time
            except AttributeError:
                room_states = {}
                energy_usage = {}
                total_on_time = {}

            # Update room state table dynamically
            for idx, room in enumerate(room_states.keys(), start=1):
                if room not in self.labels:
                    self.add_room_to_ui(idx, room)

                state = room_states.get(room, "OFF")
                energy = energy_usage.get(room, 0)
                on_time = total_on_time.get(room, 0)

                # Update labels
                self.labels[room]["state"].config(text=state)
                self.labels[room]["energy"].config(text=f"{energy:.2f}")
                self.labels[room]["time"].config(text=f"{on_time:.2f}")

            # Update room visualization
            self.update_canvas(room_states)

        # Schedule the next update
        self.root.after(1000, self.update_ui)

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

    def update_canvas(self, room_states):
        # Clear previous visualization
        self.canvas.delete("all")

        # Define room positions (modify as needed)
        room_positions = {
            "Bedroom": (50, 50, 150, 150),
            "LivingRoom": (200, 50, 300, 150),
            "Kitchen": (50, 200, 150, 300),
            "Bathroom": (200, 200, 300, 300),
            "DiningRoom": (350, 50, 450, 150),
            "Hallway": (350, 200, 450, 300),
            "Office": (500, 50, 600, 150),
        }

        # Draw rooms
        for room, coords in room_positions.items():
            color = "lightgreen" if room_states.get(room) == "ON" else "lightgray"
            self.canvas.create_rectangle(*coords, fill=color, outline="black")
            x, y = (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2
            self.canvas.create_text(x, y, text=room, font=("Helvetica", 10))

        # Draw agent position
        for room, state in room_states.items():
            if state == "ON" and room in room_positions:
                coords = room_positions[room]
                x, y = (coords[0] + coords[2]) // 2, (coords[1] + coords[3]) // 2
                self.agent_marker = self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill="red")

    def start(self):
        self.update_ui()  # Start periodic updates
        self.root.mainloop()
