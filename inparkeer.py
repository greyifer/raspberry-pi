import os
import tkinter as tk
from datetime import datetime

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def lighten_color(hex_color, factor=0.3):
    hex_color = hex_color.lstrip('#')
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    r = min(int(r + (255 - r) * factor), 255)
    g = min(int(g + (255 - g) * factor), 255)
    b = min(int(b + (255 - b) * factor), 255)
    return rgb_to_hex(r, g, b)

# button function

def screen_off():
    os.system("vcgencmd display_power 0")
    print("screen off")

def screen_on():
    os.system("vcgencmd display_power 1")
    print("screen on")

# button assign
def power_button():
    screen_off()

def setting_button():
    print("Home button pressed.")

def surveillance_button():
    print("Surveillance mode activated.")

def light_button():
    print("Lights toggled.")

def distance_button():
    print("Distance sensor reading...")

def sensors_button():
    print("Other sensors triggered.")

# Create a button with a custom command
def create_button(parent, text, x, y, width, height, color, command):
    lighter_color = lighten_color(color, 0.3)
    btn = tk.Button(parent,
                    text=text,
                    command=command,
                    bg=color,
                    activebackground=lighter_color,
                    fg="black",
                    font=("Arial", 16, "bold"),
                    cursor="hand2")
    btn.place(x=x, y=y, width=width, height=height)
    return btn

def update_clock():
    now = datetime.now().strftime("%H:%M:%S")
    clock_label.config(text=now)
    root.after(1000, update_clock)

root = tk.Tk()
root.title("Simple Grid")
root.attributes("-fullscreen", True)
root.configure(bg="black")

# Clock in top-right
clock_label = tk.Label(root, fg="white", bg="black", font=("Arial", 20, "bold"))
clock_label.place(relx=1.0, y=10, anchor="ne")

# Buttons: (label, color, assignment)
buttons_data = [
    ("Aan/uit",         rgb_to_hex(135, 255, 94),   power_button),
    ("Settings",        rgb_to_hex(43, 146, 255),   setting_button),
    ("Surveillance",    rgb_to_hex(245, 64, 64),    surveillance_button),
    ("Licht",           rgb_to_hex(255, 146, 43),   light_button),
    ("Distance",        rgb_to_hex(255, 239, 97),   distance_button),
    ("Sensors",         rgb_to_hex(255, 77, 201),   sensors_button),
]

# (x, y, width, height)
buttons_positions_sizes = [
    (50,    50,     180,    80),
    (250,   50,     180,    80),
    (450,   50,     180,    80),
    (50,    140,    180,    80),
    (250,   140,    180,    80),
    (450,   140,    180,    80),
]

for (label, color, command), (x, y, w, h) in zip(buttons_data, buttons_positions_sizes):
    create_button(root, label, x, y, w, h, color, command)

root.bind("<Button-1>", lambda event: screen_on())    

update_clock()
root.mainloop()