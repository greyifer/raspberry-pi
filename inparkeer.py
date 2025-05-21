import tkinter as tk

def rgb_to_hex(r, g, b):
    return f"#{r:02x}{g:02x}{b:02x}"

def button_clicked(name):
    print(f"{name} clicked!")

def create_button(parent, text, row, col, color):
    btn = tk.Button(parent,
                    text=text,
                    command=lambda: button_clicked(text),
                    bg=color,
                    fg="black",
                    font=("Arial", 12, "bold"),
                    width=15,
                    height=7,
                    cursor="hand2")
    btn.grid(row=row, column=col, padx=5, pady=5)

root = tk.Tk()
root.title("Simple Grid")

frame = tk.Frame(root)
frame.pack(padx=20, pady=20)

buttons = [
    [("Surveillance", rgb_to_hex(135, 255, 94)),
     ("Home", rgb_to_hex(43, 146, 255)),
     ("Aan/Uit", rgb_to_hex(245, 64, 64))],

    [("Distance", rgb_to_hex(255, 146, 43)),
     ("Licht", rgb_to_hex(255, 239, 97)),
     ("Sensors", rgb_to_hex(255, 77, 201))],
]

for row_index, row in enumerate(buttons):
    for col_index, (label, color) in enumerate(row):
        create_button(frame, label, row_index, col_index, color)

root.mainloop()
