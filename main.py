import tkinter as tk
from tkinter import messagebox
from pynput import keyboard


class MyGUI:

    def __init__(self):

        self.root = tk.Tk()

        self.menubar = tk.Menu(self.root)

        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Close?", command=exit)
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Close Without Question", command=exit)

        self.actionmenu = tk.Menu(self.menubar, tearoff=0)

        self.menubar.add_cascade(menu=self.filemenu, label="File")
        self.menubar.add_cascade(menu=self.actionmenu, label="Actions")

        self.root.config(menu=self.menubar)

        self.label = tk.Label(self.root, text="Keystroke Recorder", font=("Arial", 18))
        self.label.pack(padx=10, pady=10)

        self.textbox = tk.Text(self.root, height=5, font=("Arial", 16))
        self.textbox.bind("<KeyPress>", self.shortcut)
        self.textbox.pack(padx=10, pady=10)

        self.check_state = tk.IntVar()

        self.check = tk.Checkbutton(self.root, text="Show Messagebox", font=("Arial", 18), variable=self.check_state)
        self.check.pack(padx=10, pady=10)

        self.recordKeystrokes = tk.Button(self.root, text="Record Keystrokes", font=("Arial", 18),
                                          command=self.record_keystrokes)
        self.recordKeystrokes.pack(padx=10,pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.root.mainloop()

    def shortcut(self, event):
        if event.state == 4 and event.keysym == "Return":
            self.show_message()

    def on_closing(self):
        if messagebox.askyesno(title="Quit?", message="Do you really want to quit?"):
            self.root.destroy()

    def record_keystrokes(self):
        self.listener = keyboard.Listener(on_press=self.on_key_press)
        self.listener.start()

    def on_key_press(self, key):
        if isinstance(key, keyboard.Key):
            if key == keyboard.Key.space:
                self.textbox.insert(tk.END, ' ')
                print('Key pressed: Spacebar')
            else:
                self.textbox.insert(tk.END, f'Key pressed: {key}\n')
                print(f'Key pressed: {key}')
        else:
            try:
                if key.char and key.char.isalnum():
                    self.textbox.insert(tk.END, key.char)
                    print(f'Alphanumeric Key pressed: {key.char}')
            except AttributeError:
                pass

MyGUI()
