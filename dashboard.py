import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk


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
        # Calculate dynamic window height based on the number of rows
        num_rows = len(self.light_agent.behaviours[0].room_states) if self.light_agent and self.light_agent.behaviours else 6
        window_height = max(400, 100 + num_rows * 30)  # Adjust as needed

        self.root.geometry(f"700x{window_height}")  # Adjust width and height dynamically

        # Room state table header
        tk.Label(self.root, text="Room", font=("Helvetica", 10)).grid(row=0, column=0, sticky="w")
        tk.Label(self.root, text="State", font=("Helvetica", 10)).grid(row=0, column=1, sticky="w")
        tk.Label(self.root, text="Total Energy (W)", font=("Helvetica", 10)).grid(row=0, column=2, sticky="w")
        tk.Label(self.root, text="Total ON Time (s)", font=("Helvetica", 10)).grid(row=0, column=3, sticky="w")

        # Create a frame for room data
        self.table_frame = tk.Frame(self.root)
        self.table_frame.grid(row=1, column=0, columnspan=4, sticky="nw")

        # Canvas for room visualization
        self.canvas = tk.Canvas(self.root, width=600, height=300, bg="white")
        self.canvas.grid(row=1, column=4, padx=10, pady=10)

        # Chart area for energy visualization
        self.chart_frame = tk.Frame(self.root)
        self.chart_frame.grid(row=2, column=4, padx=10, pady=10)


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
            self.update_energy_chart()

        # Schedule the next update
        self.root.after(1000, self.update_ui)
        
    def add_room_to_ui(self, idx, room):
        room_label = tk.Label(self.root, text=room, font=("Helvetica", 10))
        room_label.grid(row=idx, column=0, sticky="w", pady=1)  # Minimal padding

        self.labels[room] = {
            "state": tk.Label(self.root, text="OFF", font=("Helvetica", 10)),
            "energy": tk.Label(self.root, text="0.00", font=("Helvetica", 10)),
            "time": tk.Label(self.root, text="0.00", font=("Helvetica", 10)),
        }

        self.labels[room]["state"].grid(row=idx, column=1, sticky="w", pady=1)
        self.labels[room]["energy"].grid(row=idx, column=2, sticky="w", pady=1)
        self.labels[room]["time"].grid(row=idx, column=3, sticky="w", pady=1)




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

    def create_energy_usage_chart(self, energy_data):
        try:
            print("Creating energy chart with data:", energy_data)  # Debugging line
            rooms = list(energy_data.keys())
            energy_values = list(energy_data.values())

            plt.figure(figsize=(6, 4))
            plt.bar(rooms, energy_values, color="skyblue")
            plt.title("Energy Usage by Room")
            plt.xlabel("Rooms")
            plt.ylabel("Total Energy (W)")
            plt.tight_layout()
            plt.savefig("energy_chart.png")  # Save the chart as an image
            print("Chart successfully created and saved as 'energy_chart.png'")  # Debugging line
        except Exception as e:
            print("Error while creating the chart:", str(e))  # Debugging line

        
    def update_energy_chart(self):
        try:
            print("Updating energy chart...")

            # Call the function to create the chart
            self.create_energy_usage_chart(self.light_agent.behaviours[0].energy_usage)

            # Load the saved chart
            img = Image.open("energy_chart.png")
            img = img.resize((300, 300))  # Resize to fit in the chart frame
            chart_image = ImageTk.PhotoImage(img)

            # Display the chart in the Tkinter chart frame
            if hasattr(self, "chart_label"):
                self.chart_label.config(image=chart_image)
                self.chart_label.image = chart_image
            else:
                self.chart_label = tk.Label(self.chart_frame, image=chart_image)
                self.chart_label.image = chart_image
                self.chart_label.pack()

            print("Energy chart updated successfully!")
        except Exception as e:
            print("Error while updating the energy chart:", str(e))


