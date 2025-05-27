import os
import tkinter as tk
from datetime import datetime
from translations import translations

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

# button functions
def screen_off():
    os.system("vcgencmd display_power 0")
    print("screen off")

def screen_on():
    os.system("vcgencmd display_power 1")
    print("screen on")

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

class MultiPageApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Multi-Page App")
        self.attributes("-fullscreen", True)
        self.configure(bg="black")

        container = tk.Frame(self, bg="black")
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.clock_label = tk.Label(self, fg="white", bg="black", font=("Arial", 20, "bold"))
        self.clock_label.place(relx=1.0, y=10, anchor="ne")
        self.clock_label.lift()

        self.update_clock()

        self.frames = {}

        self.brightness = tk.IntVar(value=50)
        self.language = tk.StringVar(value="English")

        for F in (HomePage, SettingsPage, SurveillancePage, DistancePage, SensorsPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        self.bind("<Button-1>", lambda event: screen_on())

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        frame.update_language()

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

class HomePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.buttons = []
        self.icons = []  # store PhotoImage references

        buttons_data = [
            ("screen_off",       "icons/screen_off.png",      rgb_to_hex(135, 255, 94),   screen_off),
            ("settings",         "icons/settings.png",        rgb_to_hex(43, 146, 255),   lambda: controller.show_frame("SettingsPage")),
            ("surveillance",     "icons/surveillance.png",    rgb_to_hex(245, 64, 64),    lambda: controller.show_frame("SurveillancePage")),
            ("light",            "icons/light.png",           rgb_to_hex(255, 146, 43),   light_button),
            ("distance",         "icons/distance.png",        rgb_to_hex(255, 239, 97),   lambda: controller.show_frame("DistancePage")),
            ("sensors",          "icons/sensors.png",         rgb_to_hex(255, 77, 201),   lambda: controller.show_frame("SensorsPage")),
        ]

        buttons_positions_sizes = [
            (350,    250,     360,    260),
            (750,    250,     360,    260),
            (1150,   250,     360,    260),
            (350,    540,    360,    260),
            (750,    540,    360,    260),
            (1150,   540,    360,    260),
        ]

        for (key, icon_path, color, command), (x, y, w, h) in zip(buttons_data, buttons_positions_sizes):
            icon = tk.PhotoImage(file=icon_path)
            self.icons.append(icon)  # keep reference
            btn = tk.Button(self,
                            text=translations[controller.language.get()][key],
                            image=icon,
                            compound="top",
                            command=command,
                            bg=color,
                            activebackground=lighten_color(color, 0.3),
                            fg="black",
                            font=("Arial", 16, "bold"),
                            cursor="hand2",
                            wraplength=w-20,
                            justify="center",
                            pady=10)  # <-- added padding here
            btn.place(x=x, y=y, width=w, height=h)
            self.buttons.append((btn, key, icon))

    def update_language(self):
        lang = self.controller.language.get()
        for btn, key, _ in self.buttons:
            btn.config(text=translations[lang][key])

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.label = tk.Label(self, fg="white", bg="black", font=("Arial", 24))
        self.label.place(x=50, y=150)

        self.bright_label = tk.Label(self, fg="white", bg="black", font=("Arial", 16))
        self.bright_label.place(x=50, y=220)

        self.brightness_slider = tk.Scale(self,
                                     from_=0, to=100,
                                     orient="horizontal",
                                     variable=controller.brightness,
                                     bg="black",
                                     fg="white",
                                     troughcolor="gray30",
                                     highlightthickness=0,
                                     length=600)
        self.brightness_slider.place(x=50, y=260)

        self.brightness_slider.config(command=self.brightness_changed)

        self.lang_label = tk.Label(self, fg="white", bg="black", font=("Arial", 16))
        self.lang_label.place(x=50, y=340)

        languages = list(translations.keys())
        self.lang_menu = tk.OptionMenu(self, controller.language, *languages, command=self.language_changed)
        self.lang_menu.config(bg="black", fg="white", highlightthickness=0, font=("Arial", 14))
        self.lang_menu["menu"].config(bg="black", fg="white")
        self.lang_menu.place(x=50, y=380)

        self.back_button = create_button(self, "", 50, 50, 180, 80, rgb_to_hex(135, 255, 94), lambda: controller.show_frame("HomePage"))

        self.update_language()

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["settings_page"])
        self.bright_label.config(text=translations[lang]["screen_brightness"])
        self.lang_label.config(text=translations[lang]["language"])
        self.back_button.config(text=translations[lang]["back"])

    def brightness_changed(self, val):
        print(f"Brightness changed to {val}")

    def language_changed(self, value):
        print(f"Language changed to {value}")
        self.controller.language.set(value)
        for frame in self.controller.frames.values():
            frame.update_language()

class SurveillancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.label = tk.Label(self, fg="white", bg="black", font=("Arial", 24))
        self.label.place(x=50, y=50)

        self.back_button = create_button(self, "", 50, 350, 180, 80, rgb_to_hex(135, 255, 94), lambda: controller.show_frame("HomePage"))
        self.update_language()

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["surveillance_page"])
        self.back_button.config(text=translations[lang]["back"])

class DistancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.label = tk.Label(self, fg="white", bg="black", font=("Arial", 24))
        self.label.place(x=50, y=50)

        self.back_button = create_button(self, "", 50, 350, 180, 80, rgb_to_hex(135, 255, 94), lambda: controller.show_frame("HomePage"))
        self.update_language()

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["distance_sensor_data"])
        self.back_button.config(text=translations[lang]["back"])

class SensorsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="black")
        self.controller = controller

        self.label = tk.Label(self, fg="white", bg="black", font=("Arial", 24))
        self.label.place(x=50, y=50)

        self.back_button = create_button(self, "", 50, 350, 180, 80, rgb_to_hex(135, 255, 94), lambda: controller.show_frame("HomePage"))
        self.update_language()

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["other_sensors"])
        self.back_button.config(text=translations[lang]["back"])

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()
