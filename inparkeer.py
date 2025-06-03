import os
import tkinter as tk
from datetime import datetime
import threading
import time
from translations import translations

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return int(hex_color[0:2],16), int(hex_color[2:4],16), int(hex_color[4:6],16)

def lighten_color(hex_color, factor=0.3):
    r, g, b = hex_to_rgb(hex_color)
    r = min(int(r + (255 - r) * factor), 255)
    g = min(int(g + (255 - g) * factor), 255)
    b = min(int(b + (255 - b) * factor), 255)
    return rgb_to_hex(r, g, b)

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
        self.geometry("1024x786")

        self.dark_mode = tk.BooleanVar(value=True)
        self.language = tk.StringVar(value="English")
        self.preset = tk.IntVar(value=1)

        self.configure(bg=self.get_bg_color())

        container = tk.Frame(self, bg=self.get_bg_color())
        container.pack(fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.clock_label = tk.Label(self, fg=self.get_fg_color(), bg=self.get_bg_color(), font=("Arial", 20, "bold"))
        self.clock_label.place(relx=1.0, y=10, anchor="ne")
        self.clock_label.lift()

        self.update_clock()

        self.frames = {}
        for F in (HomePage, SettingsPage, SurveillancePage, DistancePage, SensorsPage):
            frame = F(parent=container, controller=self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("HomePage")

        # Start the distance import in a separate thread after GUI loads
        threading.Thread(target=self.import_distances, daemon=True).start()
        # Start a thread to check distances
        threading.Thread(target=self.check_distances, daemon=True).start()

    def import_distances(self):
        # Delay to simulate load time or wait for app fully ready
        time.sleep(5)
        # Import here so it doesn't block initial GUI load
        from sensor import distances  # Import the distances dict dynamically
        print("Distances imported:", self.distances)

    def check_distances(self):
        while True:
            # Check if any distance is 15 cm or less
            for key, value in self.distances.items():
                if value <= 15:
                    self.play_alert_sound()
            time.sleep(1)  # Check every second

    def play_alert_sound(self):
        # Play a sound alert (you can use any sound file you have)
        os.system("aplay /path/to/alert_sound.wav &")  # Replace with your sound file path

    def get_bg_color(self):
        return "black" if self.dark_mode.get() else "white"

    def get_fg_color(self):
        return "white" if self.dark_mode.get() else "black"

    def toggle_dark_mode(self):
        self.dark_mode.set(not self.dark_mode.get())
        bg, fg = self.get_bg_color(), self.get_fg_color()
        self.configure(bg=bg)
        self.clock_label.config(bg=bg, fg=fg)
        for frame in self.frames.values():
            frame.update_colors(bg, fg)

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()
        frame.update_language()
        frame.update_colors(self.get_bg_color(), self.get_fg_color())

    def update_clock(self):
        now = datetime.now().strftime("%H:%M:%S")
        self.clock_label.config(text=now)
        self.after(1000, self.update_clock)

    def update_button_layout(self):
        self.frames["HomePage"].update_button_positions(self.preset.get())


class HomePage(tk.Frame):
    ORIGINAL_COLORS = {
        "screen_off": "#87ff5e",
        "settings": "#2b92ff",
        "surveillance": "#f54040",
        "light": "#ff922b",
        "distance": "#ffef61",
        "sensors": "#ff4dcc",
    }
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.get_bg_color())
        self.buttons = []
        self.icons = []

        self.buttons_data = [
            ("screen_off",   "icons/screen_off.png",    self.ORIGINAL_COLORS["screen_off"],   screen_off),
            ("settings",     "icons/settings.png",      self.ORIGINAL_COLORS["settings"],  lambda: controller.show_frame("SettingsPage")),
            ("surveillance", "icons/surveillance.png",  self.ORIGINAL_COLORS["surveillance"],   lambda: controller.show_frame("SurveillancePage")),
            ("light",        "icons/light.png",         self.ORIGINAL_COLORS["light"],  light_button),
            ("distance",     "icons/distance.png",      self.ORIGINAL_COLORS["distance"],  lambda: controller.show_frame("DistancePage")),
            ("sensors",      "icons/sensors.png",       self.ORIGINAL_COLORS["sensors"],  lambda: controller.show_frame("SensorsPage")),
        ]
        self.buttons_positions_sizes_preset1 = [
            (30,  140, 308, 270),
            (358, 140, 308, 270),
            (686, 140, 308, 270),
            (30,  440, 308, 270),
            (358, 440, 308, 270),
            (686, 440, 308, 270),
        ]
        self.buttons_positions_sizes_preset2 = [
            (30,  440, 308, 270),
            (358, 440, 308, 270),
            (686, 440, 308, 270),
            (30,  140, 308, 270),
            (358, 140, 308, 270),
            (686, 140, 308, 270),
        ]
        for key, icon_path, color, cmd in self.buttons_data:
            icon = tk.PhotoImage(file=icon_path)
            self.icons.append(icon)
        self.create_buttons()
        self.update_button_positions(controller.preset.get())

    def create_buttons(self):
        self.buttons.clear()
        for i, (key, _, color, cmd) in enumerate(self.buttons_data):
            btn = tk.Button(self,
                            text=translations[self.controller.language.get()][key],
                            image=self.icons[i],
                            compound="top",
                            command=cmd,
                            bg=color,
                            activebackground=lighten_color(color, 0.3),
                            fg="black",
                            font=("Arial", 16, "bold"),
                            cursor="hand2",
                            wraplength=280,
                            justify="center",
                            pady=10)
            self.buttons.append(btn)

    def update_button_positions(self, preset):
        positions = self.buttons_positions_sizes_preset1 if preset == 1 else self.buttons_positions_sizes_preset2
        for btn, pos in zip(self.buttons, positions):
            btn.place(x=pos[0], y=pos[1], width=pos[2], height=pos[3])

    def update_language(self):
        lang = self.controller.language.get()
        for btn, (key, _, _, _) in zip(self.buttons, self.buttons_data):
            btn.config(text=translations[lang][key])

    def update_colors(self, bg, fg):
        self.configure(bg=bg)
        for btn, (_, _, color, _) in zip(self.buttons, self.buttons_data):
            btn.config(bg=color, fg="black", activebackground=lighten_color(color, 0.3))

class SettingsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.get_bg_color())
        self.color_change_label = tk.Label(self, fg=controller.get_fg_color(), bg=controller.get_bg_color(), font=("Arial", 20, "bold"))
        self.color_change_label.place(x=700, y=50)
        self.color_buttons = []
        self.button_labels_keys = ["screen_off", "settings", "surveillance", "light", "distance", "sensors"]
        self.label = tk.Label(self, fg=controller.get_fg_color(), bg=controller.get_bg_color(), font=("Arial", 24))
        self.label.place(x=50, y=50)
        self.dark_mode_button = tk.Button(self, text="", command=self.toggle_dark_mode,
                                          font=("Arial", 16, "bold"), cursor="hand2")
        self.dark_mode_button.place(x=50, y=130, width=280, height=50)
        self.preset_label = tk.Label(self, fg=controller.get_fg_color(), bg=controller.get_bg_color(), font=("Arial", 16))
        self.preset_label.place(x=50, y=210)
        self.preset1_button = tk.Button(self, text="", command=lambda: self.change_preset(1),
                                       font=("Arial", 14), cursor="hand2")
        self.preset1_button.place(x=50, y=250, width=100, height=40)
        self.preset2_button = tk.Button(self, text="", command=lambda: self.change_preset(2),
                                       font=("Arial", 14), cursor="hand2")
        self.preset2_button.place(x=180, y=250, width=100, height=40)
        self.lang_label = tk.Label(self, fg=controller.get_fg_color(), bg=controller.get_bg_color(), font=("Arial", 16))
        self.lang_label.place(x=50, y=320)
        # Language buttons for touchscreen
        self.language_buttons = []
        self.languages = list(translations.keys())
        self.create_language_buttons()
        self.back_button = create_button(self, "", 30, 500, 160, 60,
                                         rgb_to_hex(135, 255, 94), lambda: controller.show_frame("HomePage"))
        self.create_color_change_buttons()
        reset_y = self.color_button_positions[-1][1] + 60
        self.reset_button = tk.Button(self,
                                      text=translations[self.controller.language.get()].get("reset_colors", "Reset Colors"),
                                      command=self.reset_colors,
                                      font=("Arial", 14, "bold"),
                                      cursor="hand2",
                                      fg="white",
                                      bg=rgb_to_hex(200, 50, 50),
                                      activebackground=lighten_color(rgb_to_hex(200, 50, 50), 0.3))
        self.reset_button.place(x=self.color_button_positions[-1][0], y=reset_y, width=200, height=50)
        # Embedded color picker frame - initially hidden offscreen
        self.color_picker_frame = tk.Frame(self, bg=self.controller.get_bg_color(), borderwidth=2, relief="groove")
        self.color_picker_frame.place(x=10000, y=100, width=580, height=350)  # bigger and hidden initially
        self.current_picker_key = None  # To track which button color is being edited
        self.create_embedded_color_picker_widgets()
        self.update_language()
        self.update_dark_mode_button()

    def create_language_buttons(self):
        start_x = 50
        start_y = 360
        button_width = 120
        button_height = 50
        spacing_x = 10
        for i, lang_key in enumerate(self.languages):
            lang_name = translations[self.controller.language.get()]["language_names"].get(lang_key, lang_key)
            btn = tk.Button(self, text=lang_name,
                            font=("Arial", 14, "bold"),
                            cursor="hand2",
                            command=lambda k=lang_key: self.set_language(k))
            btn.place(x=start_x + i * (button_width + spacing_x), y=start_y,
                      width=button_width, height=button_height)
            self.language_buttons.append(btn)

    def set_language(self, lang_key):
        self.controller.language.set(lang_key)
        self.update_language()
        for frame in self.controller.frames.values():
            frame.update_language()

    def toggle_dark_mode(self):
        self.controller.toggle_dark_mode()
        self.update_colors(self.controller.get_bg_color(), self.controller.get_fg_color())
        self.update_dark_mode_button()

    def create_color_change_buttons(self):
        self.color_buttons.clear()
        start_x = 700
        start_y = 100
        button_width = 200
        button_height = 40
        spacing_y = 50
        self.color_button_positions = []
        for i, key in enumerate(self.button_labels_keys):
            btn = tk.Button(self, text="", command=lambda k=key: self.show_embedded_color_picker(k),
                            font=("Arial", 14), cursor="hand2")
            y = start_y + i * spacing_y
            btn.place(x=start_x, y=y, width=button_width, height=button_height)
            self.color_buttons.append(btn)
            self.color_button_positions.append((start_x, y, button_width, button_height))

    def show_embedded_color_picker(self, key):
        # Show color picker frame and initialize sliders to current button color
        self.current_picker_key = key
        home_page = self.controller.frames["HomePage"]
        current_color = "#ffffff"
        for i, (btn_key, _, color, _) in enumerate(home_page.buttons_data):
            if btn_key == key:
                current_color = color
                break
        r, g, b = hex_to_rgb(current_color)
        self.r_slider.set(r)
        self.g_slider.set(g)
        self.b_slider.set(b)
        self.update_color_preview()
        # Place color picker frame onscreen at bigger size and moved more left
        self.color_picker_frame.place(x=150, y=100, width=650, height=370)
        self.color_picker_frame.lift()

    def create_embedded_color_picker_widgets(self):
        label_font = ("Arial", 18)
        slider_width = 490

        label_x = 25  # X position for labels
        slider_x = 130  # X position for sliders
        label_slider_gap = 10  # Gap between label and slider vertically
        base_y = 30  # Starting y position for first slider and label
        vertical_spacing = 70  # Vertical spacing between sliders

        # Red label and slider
        self.red_label = tk.Label(self.color_picker_frame, text="", font=label_font,
                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color())
        self.red_label.place(x=label_x, y=base_y, anchor="w")
        self.r_slider = tk.Scale(self.color_picker_frame, from_=0, to=255, orient="horizontal",
                                 length=slider_width, command=lambda e: self.update_color_preview(),
                                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color(), highlightthickness=0)
        self.r_slider.place(x=slider_x, y=base_y - 10)  # Align slider y with label, minor offset for look

        # Green label and slider
        green_y = base_y + vertical_spacing
        self.green_label = tk.Label(self.color_picker_frame, text="", font=label_font,
                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color())
        self.green_label.place(x=label_x, y=green_y, anchor="w")
        self.g_slider = tk.Scale(self.color_picker_frame, from_=0, to=255, orient="horizontal",
                                 length=slider_width, command=lambda e: self.update_color_preview(),
                                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color(), highlightthickness=0)
        self.g_slider.place(x=slider_x, y=green_y - 10)

        # Blue label and slider
        blue_y = green_y + vertical_spacing
        self.blue_label = tk.Label(self.color_picker_frame, text="", font=label_font,
                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color())
        self.blue_label.place(x=label_x, y=blue_y, anchor="w")
        self.b_slider = tk.Scale(self.color_picker_frame, from_=0, to=255, orient="horizontal",
                                 length=slider_width, command=lambda e: self.update_color_preview(),
                                 bg=self.controller.get_bg_color(), fg=self.controller.get_fg_color(), highlightthickness=0)
        self.b_slider.place(x=slider_x, y=blue_y - 10)

        # Color preview box bigger
        self.color_preview = tk.Label(self.color_picker_frame, text="", bg="#ffffff", borderwidth=2, relief="sunken")
        self.color_preview.place(x=20, y=blue_y + vertical_spacing - 20, width=610, height=70)

        # OK and Cancel buttons bigger and repositioned
        self.ok_btn = tk.Button(self.color_picker_frame, text="", command=self.embedded_color_picker_ok,
                           font=("Arial", 16, "bold"), cursor="hand2")
        self.ok_btn.place(x=180, y=blue_y + vertical_spacing + 60, width=120, height=45)

        self.cancel_btn = tk.Button(self.color_picker_frame, text="", command=self.embedded_color_picker_cancel,
                               font=("Arial", 16, "bold"), cursor="hand2")
        self.cancel_btn.place(x=360, y=blue_y + vertical_spacing + 60, width=120, height=45)

    def update_color_preview(self):
        color = rgb_to_hex(self.r_slider.get(), self.g_slider.get(), self.b_slider.get())
        self.color_preview.config(bg=color)

    def embedded_color_picker_ok(self):
        color = rgb_to_hex(self.r_slider.get(), self.g_slider.get(), self.b_slider.get())
        if self.current_picker_key is None:
            return
        home_page = self.controller.frames["HomePage"]
        for i, (btn_key, icon, _, cmd) in enumerate(home_page.buttons_data):
            if btn_key == self.current_picker_key:
                home_page.buttons[i].config(bg=color, activebackground=lighten_color(color, 0.3))
                home_page.buttons_data[i] = (btn_key, icon, color, cmd)
                break
        for btn in self.color_buttons:
            if btn.cget("text") == translations[self.controller.language.get()][self.current_picker_key]:
                btn.config(bg=color, activebackground=lighten_color(color, 0.3))
                break
        # Move color picker offscreen after OK
        self.color_picker_frame.place(x=10000, y=100, width=580, height=350)
        self.current_picker_key = None

    def embedded_color_picker_cancel(self):
        # Move color picker offscreen after Cancel
        self.color_picker_frame.place(x=10000, y=100, width=580, height=350)
        self.current_picker_key = None

    def reset_colors(self):
        home_page = self.controller.frames["HomePage"]
        for i, (key, icon, _, cmd) in enumerate(home_page.buttons_data):
            original_color = HomePage.ORIGINAL_COLORS.get(key, "#ffffff")
            home_page.buttons_data[i] = (key, icon, original_color, cmd)
            home_page.buttons[i].config(bg=original_color, activebackground=lighten_color(original_color, 0.3))
        for btn in self.color_buttons:
            key = None
            for lang_key in HomePage.ORIGINAL_COLORS.keys():
                if btn.cget("text") == translations[self.controller.language.get()][lang_key]:
                    key = lang_key
                    break
            if key:
                original_color = HomePage.ORIGINAL_COLORS[key]
                btn.config(bg=original_color, activebackground=lighten_color(original_color, 0.3))

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["settings_page"])
        self.preset_label.config(text=translations[lang].get("choose_preset", "Choose Layout Preset:"))
        self.lang_label.config(text=translations[lang]["language"])
        self.back_button.config(text=translations[lang]["back"])
        self.color_change_label.config(text=translations[lang].get("color_change", "Color Change"))
        self.reset_button.config(text=translations[lang].get("reset_colors", "Reset Colors"))
        for i, key in enumerate(self.button_labels_keys):
            self.color_buttons[i].config(text=translations[lang][key])
            color = self.controller.frames["HomePage"].buttons_data[i][2]
            self.color_buttons[i].config(bg=color, activebackground=lighten_color(color, 0.3))
        self.preset1_button.config(text=translations[lang].get("preset_1", "Preset 1"))
        self.preset2_button.config(text=translations[lang].get("preset_2", "Preset 2"))
        for i, lang_key in enumerate(self.languages):
            lang_name = translations[lang]["language_names"].get(lang_key, lang_key)
            self.language_buttons[i].config(text=lang_name)
        self.update_dark_mode_button()
        # Update embedded color picker labels and buttons texts
        self.red_label.config(text=translations[lang].get("red", "Red"))
        self.green_label.config(text=translations[lang].get("green", "Green"))
        self.blue_label.config(text=translations[lang].get("blue", "Blue"))
        self.ok_btn.config(text=translations[lang].get("ok", "OK"))
        self.cancel_btn.config(text=translations[lang].get("cancel", "Cancel"))

    def update_dark_mode_button(self):
        lang = self.controller.language.get()
        if self.controller.dark_mode.get():
            self.dark_mode_button.config(text=translations[lang].get("switch_to_light_mode", "Switch to Light Mode"))
        else:
            self.dark_mode_button.config(text=translations[lang].get("switch_to_dark_mode", "Switch to Dark Mode"))

    def change_preset(self, preset_num):
        self.controller.preset.set(preset_num)
        self.controller.update_button_layout()

    def update_colors(self, bg, fg):
        self.configure(bg=bg)
        self.label.config(bg=bg, fg=fg)
        self.preset_label.config(bg=bg, fg=fg)
        self.lang_label.config(bg=bg, fg=fg)
        self.back_button.config(bg=lighten_color(rgb_to_hex(135, 255, 94), 0.3), fg="black")
        self.dark_mode_button.config(bg=lighten_color(rgb_to_hex(43, 146, 255), 0.3), fg="black")
        self.preset1_button.config(bg=lighten_color(rgb_to_hex(245, 64, 64), 0.3), fg="black")
        self.preset2_button.config(bg=lighten_color(rgb_to_hex(255, 146, 43), 0.3), fg="black")
        self.reset_button.config(bg=rgb_to_hex(200, 50, 50), fg="white")
        for btn in self.language_buttons:
            btn.config(bg=bg, fg=fg, activebackground=bg)
        self.lang_label.config(bg=bg, fg=fg)
        # Update embedded color picker colors
        self.color_picker_frame.config(bg=bg)
        for widget in self.color_picker_frame.winfo_children():
            if isinstance(widget, tk.Label):
                widget.config(bg=bg, fg=fg)
            elif isinstance(widget, tk.Scale):
                widget.config(bg=bg, fg=fg)
            elif isinstance(widget, tk.Button):
                widget.config(bg=bg, fg=fg)

class SurveillancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.get_bg_color())
        label = tk.Label(self, text="", font=("Arial", 24))
        label.place(x=50, y=50)
        self.label = label
        back_button = create_button(self, "", 30, 500, 160, 60, rgb_to_hex(135, 255, 94),
                                    lambda: controller.show_frame("HomePage"))
        self.back_button = back_button
        self.update_language()
        self.update_colors(controller.get_bg_color(), controller.get_fg_color())

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["surveillance_page"])
        self.back_button.config(text=translations[lang]["back"])

    def update_colors(self, bg, fg):
        self.configure(bg=bg)
        self.label.config(bg=bg, fg=fg)
        self.back_button.config(bg=lighten_color(rgb_to_hex(135, 255, 94), 0.3), fg="black")

class DistancePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg=controller.get_bg_color())
        
        self.label = tk.Label(self, text="", font=("Arial", 24))
        self.label.place(x=50, y=50)
        
        # Create labels for each sensor distance
        self.distance_labels = {}
        for i in range(1, 6):
            sensor_label = tk.Label(self, text="", font=("Arial", 20))
            sensor_label.place(x=50, y=100 + (i * 30))  # Adjust y position for each sensor
            self.distance_labels[f"sensor{i}"] = sensor_label
        
        back_button = create_button(self, "", 30, 500, 160, 60, rgb_to_hex(135, 255, 94),
                                    lambda: controller.show_frame("HomePage"))
        self.back_button = back_button
        
        self.update_language()
        self.update_colors(controller.get_bg_color(), controller.get_fg_color())
        
        # Start a thread to check distances
        threading.Thread(target=self.check_distances, daemon=True).start()

    def update_language(self):
        lang = self.controller.language.get()
        self.label.config(text=translations[lang]["distance_page"])
        self.back_button.config(text=translations[lang]["back"])

    def update_colors(self, bg, fg):
        self.configure(bg=bg)
        self.label.config(bg=bg, fg=fg)
        self.back_button.config(bg=lighten_color(rgb_to_hex(135, 255, 94), 0.3), fg="black")

    def check_distances(self):
        while True:
            # Access the distances from the imported sensor module
            distances = self.controller.distances  # Assuming distances is stored in the controller
            for i in range(1, 6):
                distance_value = distances[f"sensor{i}"]
                self.distance_labels[f"sensor{i}"].config(text=f"Sensor {i}: {distance_value} cm")
                
                # Check if the distance is 15 cm or less
                if distance_value <= 15:
                    self.play_alert_sound()
            
            time.sleep(1)  # Check every second

    def play_alert_sound(self):
        # Play a sound alert (you can use any sound file you have)
        os.system("mpg123 sound.mp3 &")  # Replace with your sound file path

        def rgb_to_hex(r, g, b):
            return f"#{r:02x}{g:02x}{b:02x}"
        r, g, b = hex_to_rgb(hex_color)
        r = min(int(r + (255 - r) * factor), 255)
        g = min(int(g + (255 - g) * factor), 255)
        b = min(int(b + (255 - b) * factor), 255)
        return rgb_to_hex(r, g, b)
    def check_distances_loop(self):
        # Map each box index 0..4 to sensor keys sensor1..sensor5
        box_sensor_map = {
            0: "sensor1",  # left top box
            1: "sensor2",  # left bottom box
            2: "sensor3",  # right top box
            3: "sensor4",  # right bottom box
            4: "sensor5"   # center back box
        }
        while True:
            distances = getattr(self.controller, "distances", None)
            if distances is None:
                time.sleep(1)
                continue
            # Update sensor labels with current distances
            for i in range(1, 6):
                sensor_key = f"sensor{i}"
                dist_value = distances.get(sensor_key, None)
                if dist_value is not None:
                    self.distance_labels[sensor_key].config(text=f"Sensor {i}: {dist_value} cm")
            # Update box colors according to distance thresholds
            for idx, sensor_key in box_sensor_map.items():
                dist_value = distances.get(sensor_key, 999)
                if dist_value <= 15:
                    self.canvas.itemconfig(self.boxes[idx], fill="red")
                else:
                    self.canvas.itemconfig(self.boxes[idx], fill="white")
            time.sleep(1)

class SensorsPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        # Background color - dark neutral
        self.configure(bg="#121212")

        self.canvas_width = 800
        self.canvas_height = 400
        self.canvas = tk.Canvas(self, bg="#121212", highlightthickness=0)
        self.canvas.place(relx=0.03, rely=0.05, anchor="nw", width=self.canvas_width, height=self.canvas_height)

        # Ship polygon: rectangle + elongated bow triangle at right side
        rect_x0 = 50   # Moved closer to the left
        rect_y0 = 25   # Moved closer to the top
        rect_x1 = 500  # rectangle width
        rect_y1 = 175

        ship_points = [
            rect_x0, rect_y0,                     # rear top-left corner of rectangle
            rect_x1, rect_y0,                     # front top-right corner (start bow)
            rect_x1 + 160, (rect_y0 + rect_y1) // 2,  # tip of bow triangle
            rect_x1, rect_y1,                     # front bottom-right corner of rectangle
            rect_x0, rect_y1                      # rear bottom-left corner of rectangle
        ]
        self.canvas.create_polygon(ship_points, fill="navy", outline="white", width=4)

        box_w, box_h = 30, 30
        spacing_back = 15  # distance from rear edge for boxes
        spacing_between = 30  # spacing between boxes horizontally

        # Rear side is left side (x = rect_x0)
        # Boxes on top side near rear
        top_y = rect_y0 - box_h + 10  # above rectangle top edge
        top_x1 = rect_x0 + spacing_back + 150      # left top box 1 (closest to rear)
        top_x2 = rect_x0 + spacing_back + box_w + spacing_between + 330 # left top box 2

        # Boxes on bottom side near rear
        bottom_y = rect_y1 - 10  # below rectangle bottom edge
        bottom_x1 = top_x1  # same x as top_x1
        bottom_x2 = top_x2  # same x as top_x2

        # Box centered vertically on rear edge (between top and bottom boxes)
        center_x = rect_x0 + spacing_back
        center_y = (rect_y0 + rect_y1) // 2 - box_h // 2

        self.box_positions = [
            (bottom_x2, bottom_y),  # sensor1 in the position of sensor4 (bottom right)
            (bottom_x1, bottom_y),  # sensor2 in the position of sensor3 (bottom left)
            (center_x, center_y),   # sensor3 in the position of sensor5 (centered on rear edge)
            (top_x1, top_y),        # sensor4 in the position of sensor1 (top left)
            (top_x2, top_y)         # sensor5 in the position of sensor2 (top right)
        ]

        self.boxes = []
        for (x, y) in self.box_positions:
            box = self.canvas.create_rectangle(x, y, x + box_w, y + box_h, fill="white", outline="black", width=2)
            self.boxes.append(box)

        self.sensor_labels = {}
        label_font = ("Arial", 14, "bold")
        for i, (x, y) in enumerate(self.box_positions, start=1):
            label_x = x + box_w // 2
            label_y = y + box_h + 20
            label = self.canvas.create_text(label_x, label_y, text=f"Sensor {i}: -- cm", fill="white", font=label_font)
            self.sensor_labels[f"sensor{i}"] = label

        self.back_button = create_button(self, "", 30, 500, 160, 60,
                                         rgb_to_hex(135, 255, 94),
                                         lambda: controller.show_frame("HomePage"))

        self.update_language()
        self.update_colors(controller.get_bg_color(), controller.get_fg_color())

        threading.Thread(target=self.update_sensor_display_loop, daemon=True).start()

    def update_language(self):
        lang = self.controller.language.get()
        self.back_button.config(text=translations[lang]["back"])

    def update_colors(self, bg, fg):
        self.configure(bg="#121212")
        self.canvas.config(bg="#121212")
        self.back_button.config(bg=lighten_color(rgb_to_hex(135, 255, 94), 0.3), fg="black")

    def update_sensor_display_loop(self):
        while True:
            distances = getattr(self.controller, "distances", None)
            if not distances:
                time.sleep(1)
                continue
            for i in range(1, 6):
                key = f"sensor{i}"
                dist_value = distances.get(key, None)
                label_id = self.sensor_labels.get(key)
                if label_id is not None:
                    display_text = f"Sensor {i}: {dist_value} cm" if dist_value is not None else f"Sensor {i}: -- cm"
                    self.canvas.itemconfig(label_id, text=display_text)

                box_id = self.boxes[i - 1]
                if dist_value is not None and dist_value <= 15:
                    self.canvas.itemconfig(box_id, fill="red")
                else:
                    self.canvas.itemconfig(box_id, fill="white")

            time.sleep(1)

if __name__ == "__main__":
    app = MultiPageApp()
    app.mainloop()